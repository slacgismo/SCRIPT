import pandas as pd
import numpy as np
from datetime import datetime
import boto3
import os


def get_csv(path, file, nrows):
    print("Reading {} rows of dataframe".format(nrows if nrows is not None else "ALL"))
    return pd.read_csv(path + file, index_col=False, nrows=nrows)  # , low_memory=False)


def remove_less_than(data, col, threshold):
    print("removing {} occurences of {} of less than {}".format(sum(data[col] < threshold), col, threshold))
    return data[data[col] >= threshold]


def session_data_remove_connector(data, conn1='Type 2 Cable', conn2 = 'Type 2 Socket'):
    """Remove sessions with “Connector Type” - Type 2 Cable & Type 2 Socket"""
    print("Remove sessions with “Connector Type” - Type 2 Cable & Type 2 Socket")
    data_clean = data[~((data['Connector Type'] == conn1) | (data['Connector Type'] == conn2))]
    print("Number of values removed: ", len(data) - len(data_clean))
    return data_clean


def session_data_split_fleet(data, session_type_name="FLEET"):
    """separate fleet from non fleet"""
    data_clean = data[data['Session Type'] != session_type_name]
    data_clean_fleet = data[data['Session Type'] == session_type_name]
    print("Split into {} NON-{} and {} {}".format(
        len(data_clean), session_type_name, len(data_clean_fleet), session_type_name))
    return data_clean, data_clean_fleet


def session_data_other_limit_kwh(data, session_type_name="OTHER", max_kwh=100):
    """ ignore sessions with Energy(kWh) greater than 100 kWh for “Session Type” OTHER"""
    is_other = data['Session Type'] == session_type_name
    is_over_max = data['Energy (kWh)'] > 100
    data_clean = data[~(is_other & is_over_max)]
    print("removed {} sessions with Energy(kWh) greater than 100 kWh for “Session Type” OTHER".format(len(data) - len(data_clean)))
    return data_clean


def to_datetime(x):
    return datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")


def to_seconds(x):
    """seconds in current day since midnight"""
    return 60*60*x.hour + 60*x.minute + x.second


def to_year(x):
    return x.year


def to_month(x):
    return x.month


def to_day(x):
    """day of year, [1, 366]"""
    return x.timetuple().tm_yday


def to_weekday(x):
    """weekday, [0, 6]"""
    return x.weekday()


def apply_transforms(data, col, transforms, names, drop_col=False):
    """apply multiple transforms"""
    for n, t in zip(names, transforms):
        print("applying transfrom {} to {}".format(n, col))
        data[n] = data[col].apply(t)
    if drop_col:
        print("dropping {}".format(col))
        data = data.drop(columns=[col])
    return data


def transform_start_datetimes(data):
    col = "Station Start Time (Local)"

    # remove sessions where timestamp is not a string
    data_clean = data[data[col].apply(lambda x: type(x)) == type("")]
    print("removed {} sessions where timestamp was not a string".format(len(data) - len(data_clean)))

    transforms = [to_datetime, to_seconds, to_year, to_month, to_day, to_weekday]
    names = ["datetime", "seconds", "year", "month", "day", "weekday"]
    names = ["start_{}".format(x) for x in names]

    # create datetime object from string
    data_clean = apply_transforms(data_clean, col, [transforms[0]], [names[0]], drop_col=False)
    # all other transfroms are applied to datetime object
    data_clean = apply_transforms(data_clean, names[0], transforms[1:], names[1:], drop_col=False)

    # check
    #     for n in names:
    #         print(df_clean_5[n].head(1))

    return data_clean


def remove_out_of(data, col, legit_values, keep_nan=True):
    """Helper function: Remove all rows that are not legit values for a column"""
    print("There are {} NAN entries in column {}".format(data[col].isnull().sum(), col))
    legit = data[col].apply(lambda x: x in legit_values)
    is_nan = keep_nan & data[col].isnull()
    data_clean = data[legit | is_nan]
    print("Removed {} entries for variable {} of values {}".format(
        len(data)-len(data_clean), col, set(data[col].unique()) - set(legit_values + [np.nan])))
    if not keep_nan:
        print("dropped nans")
    return data_clean


def clean_session_data(df, optional=True, transform_datetimes=True):
    """
    * 1) Eliminate sessions that have 0 kWh Energy
    * 2) Eliminate sessions where total session time is less than 120 seconds (probably driver never really charged his car)
    * 3) Ignore sessions with “Connector Type” -  Type 2 Cable & Type 2 Socket
    * 4) “Session Type” - FLEET should ideally be analyzed/treated separately since they are not your regular/passenger EV drivers
    * 5) Ignore sessions with Energy(kWh) greater than 100 kWh for “Session Type” OTHER
    """
    df_clean_1 = remove_less_than(df, col='Energy (kWh)', threshold=0.1)
    df_clean_2 = remove_less_than(df_clean_1, col='Session Time (secs)', threshold=120)
    df_clean_3 = session_data_remove_connector(df_clean_2)
    df_clean_4, df_clean_4_fleet = session_data_split_fleet(df_clean_3)
    df_clean = session_data_other_limit_kwh(df_clean_4)
    df_clean_fleet = session_data_other_limit_kwh(df_clean_4_fleet)

    if transform_datetimes:
        df_clean = transform_start_datetimes(df_clean)
        df_clean = df_clean.drop(columns=["Station Start Time (Local)"])
        df_clean = df_clean.drop(columns=["Station End Time (Local)"])

    if optional:
        df_clean_6 = remove_out_of(df_clean, col="Session Time Zone", legit_values=['PDT', 'PST'], keep_nan=True)
        df_clean_7 = remove_out_of(df_clean_6, col="Driver Country", legit_values=["United States"], keep_nan=True)
        # Keep out of state drivers for now
        # df_clean_7 = remove_out_of(df_clean_7, col="Driver State", legit_values=["California"], keep_nan=True)
        df_clean = remove_out_of(df_clean_7, col="Fee Currency", legit_values=["USD"], keep_nan=True)

    return df_clean, df_clean_fleet


def handler(event, context):

    # Get environment variables
    raw_bucket = str(os.environ["RAW_BUCKET_NAME"])
    clean_bucket = str(os.environ["CLEAN_BUCKET_NAME"])

    print("raw bucket: " + raw_bucket)
    print("clean bucket: " + clean_bucket)

    for record in event['Records']:
        file_key = record['s3']['object']['key']
        print("file key: " + file_key)
        file_name = file_key.split('/')[-1]
        print("file name: " + file_name)
        file_type = file_key.split('/')[1]
        print("residential or commercial: " + file_type)

        print("download from s3...")
        s3 = boto3.client('s3')
        s3.download_file(raw_bucket, file_key, '/tmp/' + file_name)
        print("download from s3 finished.")

        # do verbose sanity checks, and do not save in the end
        test = False
        # working on EC2 instance
        cloud = True
        # transform datetimes
        transform_datetimes = True

        # Loading data into pandas dataframe
        if cloud:
            path = "/tmp/"
            file = file_name
        else:
            path = "/home/ourownstory/github/data/SLAC"
            file = "Charging_Session_SLAC.csv"

        if test:
            nrows = 1e6
        else:
            nrows = None

        df_raw = get_csv(path, file, nrows)
        if test:
            df = df_raw.copy(deep=True)

        # List all column headers
        if test:
            print("Size of CSV: ", len(df_raw))
            print("Columns: ", list(df_raw))

        if test:
            s = sum(df['Energy (kWh)'] < 0.1)
            print("number of sessions to be removed: ", s)

        if test:
            # df_clean_1 = session_data_remove_zero_energy(df)
            df_clean_1 = remove_less_than(df, col='Energy (kWh)', threshold=0.1)

        if test:
            s = sum(df_clean_1['Session Time (secs)'] < 120)
            print("Number of sessions less than 120 secs long: ", s)

        if test:
            # df_clean_2 = session_data_remove_session_time(df_clean_1)
            df_clean_2 = remove_less_than(df_clean_1, col='Session Time (secs)', threshold=120)

        if test:
            session_connector_type = df_clean_2['Connector Type']

            # Types of sessions:
            print("Types of connectors: ", session_connector_type.unique())

            # bad connectors
            s = sum((session_connector_type == 'Type 2 Cable') | (session_connector_type == 'Type 2 Socket'))
            if s != 0:
                print("Number of sessions with connectors Type 2: ", s)
            else:
                print("No sessions with Type 2 Connector")

        if test:
            df_clean_3 = session_data_remove_connector(df_clean_2)

        if test:
            session_type = df_clean_3['Session Type']

            # Types of sessions:
            print("Types of sessions: ", session_type.unique())

            s = sum(session_type == "FLEET")

            if s != 0:
                print("Number of sessions that corresponds to fleet: ", s)
            else:
                print("No sessions with fleet data type")

        if test:
            df_clean_4, df_clean_4_fleet = session_data_split_fleet(df_clean_3)

        if test:
            session_type_other = df_clean_4[df_clean_4['Session Type'] == 'OTHER']
            session_kwh_other = session_type_other['Energy (kWh)']

            s = sum(session_kwh_other > 100)
            print("Number of sessions greater than 100kWh: ", s)

        if test:
            df_clean_5 = session_data_other_limit_kwh(df_clean_4)
            df_clean_5_fleet = session_data_other_limit_kwh(df_clean_4_fleet)

        if test:
            col = "Station Start Time (Local)"
            print(df_clean_5[col][0])
            print(datetime.strptime(df_clean_5[col][0], "%Y-%m-%d %H:%M:%S.%f"))
            print(datetime.strptime(df_clean_5[col][0], "%Y-%m-%d %H:%M:%S.%f"))
            print(df_clean_5[col].apply(lambda x: type(x)).value_counts())

            df_clean_5 = transform_start_datetimes(df_clean_5)
            df_clean_5 = df_clean_5.drop(columns=["Station Start Time (Local)"])

        if test:
            df_clean_5 = df_clean_5.drop(columns=["Station End Time (Local)"])

        if test:
            column = "Session Time Zone"
            print(df_clean_5[column].value_counts())
            # print(len(sessions[column].unique()))

            # check: if all in California, USA, must be PDT/PST
            col = "Country"
            print(col)
            print(df_clean_5[col].value_counts())
            col = "State"
            print(col)
            print(df_clean_5[col].value_counts())

        if test and transform_datetimes:
            # plot START UDT, to sanity check graph form
            df_plot = df_clean_5[df_clean_5["Session Time Zone"].apply(lambda x: x in ["PST", "PDT"])]
            df_plot = df_plot["start_seconds"]
            # plot = plt.hist(df_plot / (60 * 60), bins=50)

        if test and transform_datetimes:
            # plot START non-UT - shifted or random? seems like a mix
            df_plot = df_clean_5[df_clean_5["Session Time Zone"].apply(lambda x: x not in ["PST", "PDT"])]
            df_plot = df_plot["start_seconds"]
            # plot = plt.hist(df_plot / (60 * 60), bins=50)

        if test:
            df_clean_6 = remove_out_of(df_clean_5, col="Session Time Zone", legit_values=['PDT', 'PST'], keep_nan=True)

        if test:
            df_clean_7 = remove_out_of(df_clean_6, col="Driver Country", legit_values=["United States"], keep_nan=True)
            # Keep out of state drivers for now
            # df_clean_7 = remove_out_of(df_clean_7, col="Driver State", legit_values=["California"], keep_nan=True)

        if test:
            df_clean_8 = remove_out_of(df_clean_7, col="Fee Currency", legit_values=["USD"], keep_nan=True)

        if not test:
            # clean, transform
            df_clean, df_clean_fleet = clean_session_data(df_raw, optional=True, transform_datetimes=True)
            print("change in size:", len(df_clean) / len(df_raw))

            # save
            path += ""
            name = "cleaned_" + file_name
            print("saving...")
            df_clean.to_csv(path + name, sep=',', index=False)
            # name = 'sessions_clean_fleet.csv'
            # print("saving: ", name)
            # df_clean_fleet.to_csv(path + name, sep=',', index=False)

            if file_type == "residential":
                s3.upload_file(path + name, clean_bucket, "session/residential/" + name)
            else:
                s3.upload_file(path + name, clean_bucket, "session/commercial/" + name)

        return "Done!"

