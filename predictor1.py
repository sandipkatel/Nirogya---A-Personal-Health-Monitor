# predictor.py
from manager2 import DataManager 

class Prediction:
    def __init__(self):
        self.dm = DataManager()
        self.df = self.dm.load_and_process_data("dataset/AdditionalSet/training.csv", "output2.csv")

    def get_columns(self):
        """return the columns label"""
        return self.df.columns()

    def get_disease_probability(self, symptoms):
        """return diseases dictionary with their probability"""
        diseases = self.df.find_diseases(symptoms)
        total_sym = len(symptoms)
        probabal_dis = {}
        for dis_label, sum_sym in diseases:
            if dis_label not in probabal_dis:
                probabal_dis[dis_label] = (total_sym / sum_sym)**2
            else:
                probabal_dis[dis_label] += (total_sym / sum_sym)**2
        
        total_probablity = sum(probabal_dis.values())
        for dis, probablity in probabal_dis.items():
            probabal_dis[dis] = probablity * 100/total_probablity

        sorted_probabal_dis = sorted(probabal_dis.items(), key=lambda x: x[1], reverse = True)
        return sorted_probabal_dis

    def predict_dis(self, symptomList):
        """predict the disease according to selected symptoms"""
        probabal_diseases = self.get_disease_probability(symptomList)
        
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
            
class Detail:
    def __init__(self):
        self.dm = DataManager()
        self.disease = None

    def _get_descriptions(self, disease):
        """return short description of disease"""
        dcr = self.dm.load_and_process_data("dataset/AdditionalSet/description.csv", "output1.csv")
        try:
            description = dcr.find_internal_data(disease.title())
            self.disease = disease.title()
            return description
        except KeyError:
            try:
                description = df.find_internal_data(disease.upper())
                self.disease = disease.upper()
                return description
            except KeyError:
                return None

    def _get_symptoms(self):
        """Return the symptoms of the given disease."""
        sym = self.dm.load_and_process_data("dataset/AdditionalSet/testing.csv", "output1.csv")
        symptoms = self.sym.find_symptoms(self.disease)

        return symptoms

    def _get_preventions_and_cures(self):
        """return the prevention and cure of provided disease"""
        pv = self.dm.load_and_process_data("dataset/AdditionalSet/prevention.csv", "output3.csv")
        preventions = pv.find_internal_data(self.disease)
        cure = self.dm.load_and_process_data("dataset/AdditionalSet/prevention.csv", "output3.csv")
        cures = cure.find_internal_data(self.disease)

        return prevention, cure


    def dis_description(self, disease):
        """return the symptoms of selected disease"""
        description = self._get_descriptions(disease)
        if description:
            format_description += f"\n\n {description}"
            return format_description
        else:
            return None

    def dis_detail(self):
        """return the detail of provided disease"""
        symptoms = self.get_symptoms()
        symptom_text = "\n\nSymptoms:\n" + "\n".join([f"  {i + 1}. {symptom}" for i, symptom in enumerate(symptoms)])
        preventions, cures = self.get_prevention_and_cure()
        prevention_text = "\n\nPreventive Measures:\n" + "\n".join([f"  {i + 1}. {prevention}" for i, prevention in enumerate(preventions)])
        cure_text = "\n\nCures/Treatments:\n" + "\n".join([f"  {i + 1}. {cure}" for i, cure in enumerate(cures)])
        return symptom_prevention_text, cure_text
