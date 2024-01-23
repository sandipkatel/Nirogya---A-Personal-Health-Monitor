import pandas as pd

df = pd.read_csv("dataset/dis_sym_dataset_norm.csv", sep = ",", quotechar='"').values.tolist()
print(list(df[i][0] for i in range(len(df))))