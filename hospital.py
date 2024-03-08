import pandas as pd
import csv
def readData():
    df = pd.read_csv("dataset\hospitals.csv", encoding="ISO-8859-1")
    data_list = df.T.values.tolist()
    return data_list


