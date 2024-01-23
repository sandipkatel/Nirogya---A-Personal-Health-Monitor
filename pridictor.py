import pandas as pd

testing = pd.read_csv("dataset/Testing.csv")
print(testing.head())
print(list(testing.prognosis.head()))