# manager2.py
import csv
from AVLTree import AVLTree

class DataManager:
    def __init__(self):
        self.data = AVLTree()
        self.columns = []
    def clear_data(self):
        self.data = AVLTree()
        self.columns = []

    def load_and_process_data(self, source_filename, dest_filename=None):
        self.clear_data()
        with open(source_filename, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            self.columns = header
            # Read data rows
            for row in csv_reader:
                row[0] = row[0].title() if row[0] != row[0].upper() else row[0]
                self.data.insert(row)

        if dest_filename:
            with open(dest_filename, 'w') as file:
                csv_writer = csv.writer(file)
                # Write header
                csv_writer.writerow(self.columns)
                # Write data
                for data_row in self.data.get_data():
                    converted_data = [str(item) if not isinstance(item, str) else item for item in data_row]
                    csv_writer.writerow(converted_data)

        # Simulating DataFrame behavior by providing similar interface
        class DataFrameLike:
            def __init__(self, data_manager):
                self.data_manager = data_manager

            def columns(self):
                # Return column names
                return self.data_manager.columns[1:]
                    
            def find_diseases(self, symptoms):
                # Find diseases where all specified symptoms are present
                result = []
                dataset = self.data_manager.data.get_data()
                for data in dataset:
                    has_symptoms = True
                    for symptom in symptoms:
                        symptom_index = self.data_manager.columns.index(symptom)
                        if data[symptom_index] != '1':
                            has_symptoms = False
                            break
                    if has_symptoms:
                        sum = 0
                        new_data = data[1:]
                        for value in new_data:
                            sum += int(value)
                        result.append((data[0], sum))
                return result

            def find_symptoms(self, disease):
                data = self.data_manager.data.search_data(disease)
                if data:
                    symptoms = []
                    for i, value in enumerate(data):
                        if value == "1":
                            symptoms.append(self.data_manager.columns[i])
                    return symptoms
                else:
                    return None

            def find_internal_data(self, disease):
                data = self.data_manager.data.search_data(disease)
                if data:
                    data_values = []
                    for value in data[1:]:
                        if value:
                            data_values.append(value)
                    return data_values
                else:
                    return None

            def __repr__(self):
                # Implement representation
                return repr(self.data_manager.data)

        return DataFrameLike(self)


def main():
    data_manager = DataManager()
    df = data_manager.load_and_process_data("dataset/AdditionalSet/training.csv", "output2.csv")
    symptoms = ["Continuous Sneezing"]

    diseases = df.find_diseases(symptoms)
    print("Diseases:", diseases)
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
    print(sorted_probabal_dis)

    
    df1 = data_manager.load_and_process_data("dataset/Additionalset/testing.csv", "output7.csv")
    syms = df1.find_internal_data("AIDS")
    print(syms)

if __name__ == "__main__":
    main()
