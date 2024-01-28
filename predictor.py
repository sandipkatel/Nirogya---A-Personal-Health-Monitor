# Privictionary dictionary
import pandas as pd

df1 = pd.read_csv("dataset/dis_sym_dataset_norm.csv")
df1.set_index("label_dis", inplace = True)
df1.index = df1.index.str.title()
df1.to_csv("output0.csv")

df2 = pd.read_csv("dataset/dis_sym_dataset_comb.csv")
df2.set_index("label_dis", inplace = True)

def get_symptoms(disease):
    return df1.columns[df1.loc[disease].astype(bool)].tolist()

def predict_dis(symptomString):
    print("predict_dis called")
    all_symptoms = {}
    print("Among the following select the symptoms:")
    for i, sym in enumerate(df1.columns):
        all_symptoms[i] = sym


   # print(all_symptoms.items(), end=", ")
    print()
    '''symptom_num = list(int(s) for s in input("Select the symptoms:" ).split()) '''
    symptoms = []
    symptom_num = list(int(s) for s in symptomString.split())

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
            return count_dis
    else:
        print("Sorry, the symptoms are not compatible to any disease." )
        return None
    

def dis_symptoms():
    disease = input("Enter the disease name: ")
    for i, sym in enumerate(get_symptoms(disease.title())):
        print(f"\t{i + 1}. {sym}")


def predict_dis1(symptomString):
    print(symptomString)
    print("predict_dis called")
    all_symptoms = {}
    print("Among the following select the symptoms:")
    for i, sym in enumerate(df1.columns):
        all_symptoms[i] = sym


   # print(all_symptoms.items(), end=", ")
    print()
    '''symptom_num = list(int(s) for s in input("Select the symptoms:" ).split()) '''
    symptoms = []
    symptom_num = list(symptomString.split(" "))
    print(symptom_num)
    '''for num in symptom_num:
        symptoms.append(all_symptoms[num])'''

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