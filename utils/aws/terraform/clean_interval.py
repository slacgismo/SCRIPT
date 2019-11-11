import pandas as pd
import numpy as np
import boto3
import os


def get_csv(file, nrows, dtype=None):
    print("Reading {} rows of dataframe {}".format(nrows if nrows is not None else "ALL", file))
    return pd.read_csv(file, index_col=False, nrows=nrows, dtype=dtype)


def apply_inplace(df, field, fun):
    return pd.concat([df.drop(field, axis=1), df[field].apply(fun)], axis=1)


def remove_less_or_equal(data, col, threshold):
    print("removing {} occurences of {} of less than {}".format(sum(data[col] <= threshold), col, threshold))
    return data[data[col] > threshold]


def remove_less_than(data, col, threshold):
    print("removing {} occurences of {} of less than {}".format(sum(data[col] < threshold), col, threshold))
    return data[data[col] >= threshold]


def limit_power(data, col, threshold):
    print("In {}, {} extreme entries were replaced with {}".format(col, sum(data[col] > threshold), threshold))
    fun = lambda x: min(x, threshold)
    return apply_inplace(data, col, fun)


def replace_neg_with_zero(data, col):
    print("In {}, {} negative entries were replaced with 0".format(col, sum(data[col] < 0)))
    fun = lambda x: x if (x > 0) else 0.0
    return apply_inplace(data, col, fun)


def limit_energy_sophisticated(data, threshold):
    assert sum(data['Interval Duration (Secs)'] == 0) == 0
    col = 'Interval Energy'
    col_s = 'Interval Duration (Secs)'
    to_replace = data[col]  > (threshold/3600)*data[col_s]
    print("In {}, {} extreme entries were replaced with {}".format(col, sum(to_replace), threshold))
    data.loc[:, col] = np.minimum(data[col], (threshold/3600)*data[col_s])
    return data


def clean_intervals(df):
    """
    * 0 - Remove all Intervals with Zero or Negative Energy (End of a session is captured in session data)
    * 1 - Remove intervals of duration less than 1 second
    * 2 - Replace negative energy values with zero
    * 3a - Ignore interval data with super high “Power” (limit to station max: 50kW) -> Assuming power data is in kW.
    * 3b - Also limit maximal energy, to 50kW times Interval-duration
    * optional: Sort by session ID and interval ID
    * optional: round to 4 decimals
    """
    # 0
    df = remove_less_or_equal(df, col="Interval Energy", threshold=0.0)

    # 1
    df = remove_less_than(df, col='Interval Duration (Secs)', threshold=1)

    # 2
    df = replace_neg_with_zero(df, col='Peak Power')
    df = replace_neg_with_zero(df, col='Average Power')
    df = replace_neg_with_zero(df, col='Interval Energy')

    # 3
    df = limit_power(df, col='Peak Power', threshold=50)
    df = limit_power(df, col='Average Power', threshold=50)
    # df = limit_power(df, col='Interval Energy, threshold=50/4.0)
    df = limit_energy_sophisticated(df, threshold=50)

    # sort
    df = df.sort_values(by=["Session ID", "Interval ID"], axis=0, ascending=True)

    # round to 4 decimals
    df = df.round(decimals={'Interval Energy': 4, 'Peak Power': 4, 'Average Power': 4, })
    return df


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

        # Loading data into pandas dataframe
        path = "/tmp/"
        file_names = [file_name]

        if test:
            nrows = 1e6
        else:
            nrows = None

        col_types = {
            'Interval ID': int,
            'Session ID': int,
            'Interval Start Time (Local)': str,
            'Interval Duration (Secs)': int,
            'Peak Power': float,
            'Average Power': float,
            'Interval Energy': float
        }

        df_raw_list = [get_csv(path + f, nrows, dtype=col_types) for f in file_names]
        print("concatenate dataframes")
        df_raw = pd.concat(df_raw_list, ignore_index=True)

        if test:
            df = df_raw.copy(deep=True)

        # List all column headers

        print("Len of CSV: ", len(df_raw.index))
        print("Columns: ", list(df_raw))

        if test:
            data = df.copy(deep=True)
            zeros = sum(data["Interval Energy"] == 0.0)
            print("Percentage Zero-Energy:", zeros / len(df))
            data = data[data["Interval Energy"] > 0.0]
            near_zero = sum(data["Interval Energy"] < 0.01)
            print("Percentage Near Zero-Energy:", near_zero / len(df))

        if test:
            # keep all non-zero entries, saves about half of the space
            #     df = remove_zero_entries(df, col="Interval Energy")
            # also remove all negative entries
            df = remove_less_or_equal(df, col="Interval Energy", threshold=0.0)

        if test:
            df = remove_less_than(df, col='Interval Duration (Secs)', threshold=1)

        if test:
            df = replace_neg_with_zero(df, col='Peak Power')
            df = replace_neg_with_zero(df, col='Average Power')

        if test:
            data = df.copy(deep=True)
            print("found {} entries where data['Average Power'] > 0.1 + data['Peak Power']".format(
                sum(data['Average Power'] > 0.1 + data['Peak Power'])))

        if test:
            df = limit_power(df, col='Peak Power', threshold=50)
            df = limit_power(df, col='Average Power', threshold=50)
            # df = limit_power(df, col='Interval Energy, threshold=50/4.0)
            df = limit_energy_sophisticated(df, threshold=50)

        if test:
            df = df.sort_values(by=["Session ID", "Interval ID"], axis=0, ascending=True)

        if test:
            data = df.copy(deep=True)
            print("fraction of incomplete intervals:", sum(data["Interval Duration (Secs)"] != 900) / len(data))

        if test:
            decimals = {
                'Interval Energy': 4,
                'Peak Power': 4,
                'Average Power': 4,
            }
            df = df.round(decimals=decimals)

        if not test:
            df_clean = clean_intervals(df_raw)
            print("change in size:", len(df_clean) / len(df_raw))

        if not test:
            print("saving...")
            df_clean.to_csv(path + "cleaned_" + file_name, sep=',', index=False)

            if file_type == "residential":
                s3.upload_file(path + "cleaned_" + file_name, clean_bucket,
                               "interval/residential/" + "cleaned_" + file_name)
            else:
                s3.upload_file(path + "cleaned_" + file_name, clean_bucket,
                               "interval/commercial/" + "cleaned_" + file_name)

        return "Done!"


