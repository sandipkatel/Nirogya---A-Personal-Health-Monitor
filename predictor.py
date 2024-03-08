# predictor.py
from manager import DataManager 
from DSA_Stuff.merge_sort import sort_dic

class Prediction:
    def __init__(self):
        self.dm = DataManager()
        self.df = self.dm.load_and_process_data("dataset/AdditionalSet/training.csv", "output2.csv")
    def get_columns(self):
        """return the columns label"""
        return self.df.columns()

    ''' def get_disease_probability(self, symptoms):
        """return diseases dictionary with their probability"""
        diseases = self.df.find_diseases(symptoms)
        total_sym = len(symptoms)
        probabal_dis = {}
        for dis_label, sum_sym in diseases:
            if dis_label not in probabal_dis:
                probabal_dis[dis_label] = (total_sym / sum_sym)**2
            else:
                probabal_dis[dis_label] += (total_sym / sum_sym)**2
        if probabal_dis:
            probabal_dis["Others"] = 1
            total_probablity = sum(probabal_dis.values())
            for dis, probablity in probabal_dis.items():
                probabal_dis[dis] = probablity * 100/total_probablity
            other_dis_prob = probabal_dis.pop("Others")
            sorted_probabal_dis = list(probabal_dis.items())
            sort_dic(sorted_probabal_dis)
            sorted_probabal_dis.append(["Others", other_dis_prob])
            return sorted_probabal_dis
        else:
            return None'''
    def get_disease_probability(self, symptoms):
        """Return diseases dictionary with their probability using Baye's theorem of probability"""
        diseases = self.df.find_diseases(symptoms)
        total_sym = len(symptoms)
        probabal_dis = {}
        total_probablity = 0
        
        for dis_label, sum_sym in diseases:
            probability_given_symptoms = sum_sym / total_sym
            prior_probability = 1 / len(diseases)
            posterior_probability = probability_given_symptoms * prior_probability
            if dis_label not in probabal_dis :
                    probabal_dis[dis_label] = posterior_probability
            else:
                    probabal_dis[dis_label] += posterior_probability
            total_probablity += posterior_probability

        if probabal_dis:
            for dis, probablity in probabal_dis.items():
                probabal_dis[dis] = probablity * 100 / total_probablity

            scaling_factor = 1 / (total_sym + 1)
            probabal_others = 100 * scaling_factor

            remaining_prob = 100 - probabal_others
            total_other_prob = sum(probabal_dis.values())
            for dis in probabal_dis:
                if dis:
                    probabal_dis[dis] *= remaining_prob / total_other_prob
            
            sorted_probabal_dis = list(probabal_dis.items())
            sort_dic(sorted_probabal_dis)  
            sorted_probabal_dis.append(["Others", probabal_others]) 
            return sorted_probabal_dis
        else:
            return None





    def predict_dis(self, symptomList):
        """predict the disease according to selected symptoms"""
        probabal_diseases = self.get_disease_probability(symptomList)
        
        if probabal_diseases:
            if len(probabal_diseases) >= 10:
                return "Please provide sufficient data."
            else:
                result = "Probable disease:\n"
                i = 0
                for i, (dis, per) in enumerate(probabal_diseases, start=1):
                    result += "{}. {:<40}{:.2f}%\n".format(i, dis, per)
                result += "\n\nDisclaimer: This is for informational purposes\nonly and shouldn't be used for medical diagnosis."
                return result
        else:
            return "Sorry, the symptoms are not compatible with\nany disease."

class Detail:
    def __init__(self):
        self.dm = DataManager()
        self.disease = None

    def _get_descriptions(self, disease):
        """return short description of disease"""
        dcr = self.dm.load_and_process_data("dataset/AdditionalSet/description.csv")
        try:
            description = dcr.find_internal_data(disease.title())
            self.disease = disease.title()
            return description
        except AttributeError:
            try:
                description = dcr.find_internal_data(disease.upper())
                self.disease = disease.upper()
                return description
            except AttributeError:
                return None

    def _get_symptoms(self):
        """Return the symptoms of the given disease."""
        sym = self.dm.load_and_process_data("dataset/AdditionalSet/testing.csv")
        symptoms = sym.find_symptoms(self.disease)
        return symptoms

    def _get_preventions_and_cures(self):
        """return the prevention and cure of provided disease"""
        pv = self.dm.load_and_process_data("dataset/AdditionalSet/prevention.csv")
        preventions = pv.find_internal_data(self.disease)
        cure = self.dm.load_and_process_data("dataset/AdditionalSet/cure.csv")
        cures = cure.find_internal_data(self.disease)
        return preventions, cures


    def dis_description(self, disease):
        """return the symptoms of selected disease"""
        description = self._get_descriptions(disease)
        if description:
            format_description = "\n" + "\n".join([f"  {describe}" for describe in description])
            return format_description
        else:
            return None

    def dis_detail(self):
        """return the detail of provided disease"""
        symptoms = self._get_symptoms()
        symptom_text = "\n\nSymptoms:\n" + "\n".join([f"  {i + 1}. {symptom}" for i, symptom in enumerate(symptoms)])
        preventions, cures = self._get_preventions_and_cures()
        prevention_text = "\n\nPreventive Measures:\n" + "\n".join([f"  {i + 1}. {prevention}" for i, prevention in enumerate(preventions)])
        cure_text = "\n\nCures/Treatments:\n" + "\n".join([f"  {i + 1}. {cure}" for i, cure in enumerate(cures)])
        print("Executed Succssfully detailed")
        return symptom_text, prevention_text, cure_text
