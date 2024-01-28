# Privictionary dictionary
import pandas as pd

# Read the CSV file and perform necessary transformations
df1 = pd.read_csv("dataset/AdditionalSet/testing.csv")

# Capitalize the 'Disease' column based on your condition
df1["Disease"] = df1["prognosis"].apply(lambda x: x.title() if x != x.upper() else x)

# Drop unnecessary columns
df1.drop(["prognosis"], axis=1, inplace=True)

# Set 'Disease' as the new index
df1.set_index("Disease", inplace=True)

# Replace underscores with spaces in column names
df1.columns = df1.columns.str.replace("_", " ")

# Capitalize the column names
df1.columns = df1.columns.str.title()

# Sort the DataFrame by index and columns
df1.sort_index(axis=0, inplace=True)
df1.sort_index(axis=1, inplace=True)

# Save the modified DataFrame to a new CSV file
df1.to_csv("output0.csv")

# Read the CSV file and perform necessary transformations
df2 = pd.read_csv("dataset/AdditionalSet/training.csv")

# Capitalize the 'Disease' column based on your condition
df2["Disease"] = df2["prognosis"].apply(lambda x: x.title() if x != x.upper() else x)

# Drop unnecessary columns
df2.drop(["prognosis"], axis=1, inplace=True)

# Set 'Disease' as the new index
df2.set_index("Disease", inplace=True)

# Replace underscores with spaces in column names
df2.columns = df2.columns.str.replace("_", " ")

# Capitalize the column names
df2.columns = df2.columns.str.title()

# Sort the DataFrame by index and columns
df2.sort_index(axis=0, inplace=True)
df2.sort_index(axis=1, inplace=True)

# Save the modified DataFrame to a new CSV file
df2.to_csv("output1.csv")


def get_symptoms(disease):
    try:
        return df1.columns[df1.loc[disease.title()].astype(bool)].tolist()
    except KeyError:
        return df1.columns[df1.loc[disease.upper()].astype(bool)].tolist()
    except KeyError:
        raise KeyError("Could not find disease in data set")

def pridict_dis():
    all_symptoms = {}
    print("Among the following select the symptoms:")
    for i, sym in enumerate(df1.columns):
        all_symptoms[i] = sym


    print(all_symptoms.items(), end=", ")
    print()
    symptom_num = list(int(s) for s in input("Select the symptoms:" ).split())
    symptoms = []

    for num in symptom_num:
        symptoms.append(all_symptoms[num])
    dis1 = df1[df1[symptoms].isin([1]).all(axis=1)].index.tolist()
    dis2 = df2[df2[symptoms].isin([1]).all(axis=1)].index.tolist()
    disease = dis1 + dis2
    count_dis = {}
    for dis in disease:
        if dis in count_dis:
            count_dis[dis]  += 1/len(disease) * 100
        else:
            count_dis[dis] = 1/len(disease) * 100
    count_dis = dict(sorted(count_dis.items(), key=lambda d: d[1], reverse=True))
    if disease:
        print("Probale disease:")
        for dis_, per in count_dis.items():
            print(f"\t{dis_}\t{per:.2f}")
    else:
        print("Sorry, the symptoms are not compatible to any disease." )

def dis_symptoms():
    disease = input("Enter the disease name: ")
    for i, sym in enumerate(get_symptoms(disease)):
        print(f"\t{i + 1}. {sym}")

def main():
    print("What do you want?")
    choice = int(input("Enter 1 to find disease name or 2 to see symptoms: "))
    if choice == 1:
        pridict_dis()
    elif choice == 2:
        dis_symptoms()
    else:
        print("Invalid choice!!")

if __name__ == "__main__":
    main()