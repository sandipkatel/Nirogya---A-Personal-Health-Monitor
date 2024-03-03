# Privictionary dictionary
import pandas as pd

df = pd.read_csv("dataset/dis_sym_dataset_norm.csv")
df.set_index("label_dis", inplace = True)


def get_symptoms(disease):
    return df.columns[df.loc[disease].astype(bool)].tolist()

def pridict_dis():
    all_symptoms = {}
    print("Among the following select the symptoms:")
    for i, sym in enumerate(df.columns):
        all_symptoms[i] = sym


    print(all_symptoms.items(), end=", ")
    print()
    symptom_num = list(int(s) for s in input("Select the symptoms:" ).split())
    symptoms = []

    for num in symptom_num:
        symptoms.append(all_symptoms[num])

    disease = set(df[df[symptoms].isin([1]).all(axis=1)].index)

    print(f"Sorry, You are seem to be affected by {disease}." if disease else "Sorry, the symptoms are not compatible to any disease." )

def dis_symptoms():
    disease = input("Enter the disease name: ")
    for i, dis in enumerate(get_symptoms(disease.capitalize())):
        print(f"\t{i + 1}. {dis}")

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