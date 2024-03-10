# manager.py
import csv
from src.DSA_Stuff.AVLTree import AVLTree

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
            header = next(csv_reader)
            self.columns = header
            for row in csv_reader:
                row[0] = row[0].title() if row[0] != row[0].upper() else row[0]
                for i, _data in enumerate(row):
                    if _data.islower():
                        row[i] = _data.capitalize()
                self.data.insert(row)

        if dest_filename:
            with open(dest_filename, 'w') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self.columns)
                for data_row in self.data.get_data():
                    converted_data = [str(item) if not isinstance(item, str) else item for item in data_row]
                    csv_writer.writerow(converted_data)

        class DataFrameLike:
            def __init__(self, data_manager):
                self.data_manager = data_manager

            def columns(self):
                return self.data_manager.columns[1:]
                    
            def find_diseases(self, symptoms):
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
                return repr(self.data_manager.data)

        return DataFrameLike(self)
