import numpy as np
import requests
import io

def getScaData(item_name, url="https://s3-us-west-1.amazonaws.com/script.control.tool/load_control/"):
    ''' gets and cleans the sca data when there is no user data input '''
    r = requests.get(url + item_name)
    df = np.load(io.BytesIO(r.content))
    sca_load = (0.25*np.arange(0, 96), np.sum(df, axis=0))
    data_final = []
    for x in range(len(sca_load[0])):
        row = {"load": str(sca_load[1][x]), "time": str(sca_load[0][x])}
        data_final.append(row)

    return data_final
