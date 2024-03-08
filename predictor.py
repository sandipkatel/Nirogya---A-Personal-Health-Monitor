# predictor.py

from manager import DataManager 

dm = DataManager()
df1 = dm.load_and_process_data("dataset/AdditionalSet/testing.csv", "output1.csv")

def get_disease_probability(symptoms):
    """return diseases dictionary with their probability"""
    df = dm.load_and_process_data("dataset/AdditionalSet/training.csv", "output2.csv", set_index= True)
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
    """Return the symptoms of the given disease."""
    try:
        return df1.columns[df1.loc[disease.title()].astype(bool)].tolist()
    except KeyError:
        try:
            return df1.columns[df1.loc[disease.upper()].astype(bool)].tolist()
        except KeyError:
            return None

def show_prevention_and_cure(disease):
    """return the prevention and cure of provided disease"""
    pc = dm.load_and_process_data("dataset/AdditionalSet/prevention_and_cure.csv", "output2.csv")
    
    try:
        preventions = pc.loc[disease.title()]["Prevention"].split(";")
        cures = pc.loc[disease.title()]["Cure/Treatment"].split(";")
    except KeyError:
        preventions = pc.loc[disease.upper()]["Prevention"].split(";")
        cures = pc.loc[disease.upper()]["Cure/Treatment"].split(";")
    except KeyError:
        raise KeyError("Could not find disease in data set")

    return preventions, cures

def predict_dis(symptomList):
    """predict the disease according to selected symptoms"""
    probabal_diseases = get_disease_probability(symptomList)
    
    if len(probabal_diseases) >= 10:
        return "Please provide sufficient data."
    elif len(probabal_diseases) == 0:
        return "Sorry, the symptoms are not compatible with any disease."
    else:
        result = "Probable disease:\n"
        i = 0
        for i, (dis, per) in enumerate(probabal_diseases, start=1):
            result += "{}. {:<40}{:.2f}%\n".format(i, dis, per)
        return result

def dis_symptoms(disease):
    """return the symptoms of selected disease"""
    symptoms = get_symptoms(disease.capitalize())
    if symptoms:
        format_symptoms = "Symptoms:\n"
        for i, dis in enumerate(symptoms):
            format_symptoms += f"  {i + 1}.  {dis}\n"
        return format_symptoms
    else:
        return None

def get_prevention_and_cure(disease):
    """return the prevention and cure of provided disease"""
    preventions, cures = show_prevention_and_cure(disease)
    prevention_text = "\n\nPrevention:\n" + "\n".join([f"  {i + 1}. {prevention}" for i, prevention in enumerate(preventions)])
    cure_text = "\n\nCure/Treatment:\n" + "\n".join([f"  {i + 1}. {cure}" for i, cure in enumerate(cures)])
    return prevention_text, cure_text
