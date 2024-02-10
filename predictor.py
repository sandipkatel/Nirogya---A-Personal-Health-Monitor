# predictor.py
"""Predict the disease for given symptoms and also find symptoms, prevention and cure of selected disease."""
from manager import DataManager 

dm = DataManager()
df1 = dm.load_and_process_data("dataset/AdditionalSet/testing.csv", "output0.csv")

def get_disease_probability(symptoms):
    """return diseases dictionary with their probability"""
    df = dm.load_and_process_data("dataset/AdditionalSet/training.csv", "output1.csv", set_index= True)
    total_sym = len(symptoms)
    diseases = df[df[symptoms].isin([1]).all(axis=1)].index.tolist()
    probabal_dis = {}
    for dis_index, dis_value in diseases:
        sum_sym = df.iloc[dis_index].sum()
        if dis_value not in probabal_dis:
            # calculate probablity = (total no. of selected symtoms) / (tota no. of symptoms of that disease) 
            probabal_dis[dis_value] = (total_sym / sum_sym)**2
        else:
            probabal_dis[dis_value] += (total_sym / sum_sym)**2
    
    total_probablity = sum(probabal_dis.values())
    for dis, probablity in probabal_dis.items():
        probabal_dis[dis] = probablity * 100/total_probablity

    sorted_probabal_dis = sorted(probabal_dis.items(), key=lambda x: x[1], reverse = True)
    return sorted_probabal_dis

def get_symptoms(disease):
    """return the symptom of given disease"""
    try:
        return df1.columns[df1.loc[disease.title()].astype(bool)].tolist()
    except KeyError:
        return df1.columns[df1.loc[disease.upper()].astype(bool)].tolist()
    except KeyError:
        raise KeyError("Could not find disease in data set")

def show_prevention_and_cure(disease):
    """print the prevention and cure of provided disease"""
    pc = dm.load_and_process_data("dataset/AdditionalSet/pervention_and_cure.csv", "output2.csv")
    
    try:
        preventions = pc.loc[disease.title()]["Prevention"].split(";")
        cures = pc.loc[disease.title()]["Cure/Treatment"].split(";")
    except KeyError:
        preventions = pc.loc[disease.upper()]["Prevention"].split(";")
        cures = pc.loc[disease.upper()]["Cure/Treatment"].split(";")
    except KeyError:
        raise KeyError("Could not find disease in data set")

    print("Prevention: ")
    for i, prevention in enumerate(preventions):
        print(f"\t{i + 1}. {prevention}")
    print("Cure/Treatment: ")
    for i, cure in enumerate(cures):
        print(f"\t{i + 1}. {cure}")


def pridict_dis():
    """predict the disease accourding to selected symtoms"""
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
    
    probabal_diseases = get_disease_probability(symptoms)
    if len(probabal_diseases) >= 10:
        print("Please provide sufficient data.")
    elif len(probabal_diseases) == 0:
        print("Sorry, the symptoms are not compatible to any disease." )
    else:
        print("Probabale disease:")
        for dis, per in probabal_diseases:
            print(f"\t{dis}\t{per:.2f}%")

def dis_symptoms():
    """display the symptoms of selected disease"""
    disease = input("Enter the disease name: ")
    print("Symptoms: ")
    for i, sym in enumerate(get_symptoms(disease)):
        print(f"\t{i + 1}. {sym}")
    choice = input("Would you like to find prevention and cure (Enter Y for yes): ")
    if choice.lower() == "y":
        show_prevention_and_cure(disease)

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