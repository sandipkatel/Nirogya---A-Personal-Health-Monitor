# Privictionary dictionary

from manager import DataManager 

dm = DataManager()
df1 = dm.load_and_process_data("/dataset/AdditionalSet/testing.csv", "output0.csv")
df2 = dm.load_and_process_data("/dataset/AdditionalSet/training.csv", "output1.csv")

def get_disease_probablity(symptoms):
    total_sym = len(symptoms)
    diseases = df2[df2[symptoms].isin([1]).all(axis=1)].index.tolist()
    probabal_dis = {}
    for dis_index, dis_value in diseases:
        sum_sym = df2.iloc[dis_index].sum()
        if dis_value not in probabal_dis:
            # calculate probablity = (total no. of selected symtoms) / (tota no. of symptoms of that disease) 
            probabal_dis[dis_value] = total_sym / sum_sym
        else:
            probabal_dis[dis_value] += total_sym / sum_sym
    
    total_probablity = sum(probabal_dis.values())
    for dis, probablity in probabal_dis.items():
        probabal_dis[dis] = probablity * 100/total_probablity

    sorted_probabal_dis = sorted(probabal_dis.items(), key=lambda x: x[1], reverse = True)
    return sorted_probabal_dis

def get_symptoms(disease):
    """return the symptom of given disease"""
    # make only one index to avoid KeyError
    df1.set_index(df1.index.get_level_values(1), inplace = True)
    try:
        return df1.columns[df1.loc[disease.title()].astype(bool)].tolist()
    except KeyError:
        return df1.columns[df1.loc[disease.upper()].astype(bool)].tolist()
    except KeyError:
        raise KeyError("Could not find disease in data set")


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
    
    probabal_diseases = get_disease_probablity(symptoms)
    if len(probabal_diseases) >= 10:
        print("Please provide sufficient data.")
    elif len(probabal_diseases) == 0:
        print("Sorry, the symptoms are not compatible to any disease." )
    else:
        print("probabale disease:")
        for dis, per in probabal_diseases:
            print(f"\t{dis}\t{per:.2f}%")

def dis_symptoms():
    """display the symptoms of selected disease"""
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