# manager.py

import pandas as pd

class DataManager:
    df = None  # Shared class variable

    def __init__(self, source_filename, dest_filename):
        self.source_filename = source_filename
        self.dest_filename = dest_filename

    def load_and_process_data(self):
        # Read the source file
        df = pd.read_csv(self.source_filename)

        # Find the column containing the disease using the first object-type column
        index_col = next(col for col, dtype in df.dtypes.items() if dtype == "object")

        # Set index and capitalize it
        df[index_col.title()] = df.pop(index_col).apply(lambda x: x.title() if x != x.upper() else x)
        df.set_index(index_col.title(), inplace=True)

        # Replace underscores with spaces in column names and capitalize them
        df.columns = [col.replace("_", " ").title() for col in df.columns]

        # Sort the DataFrame by index and columns
        df.sort_index(axis=0, inplace=True)
        df.sort_index(axis=1, inplace=True)

        # Save the modified DataFrame to a new CSV file
        df.to_csv(self.dest_filename)

        # Save the processed DataFrame to the class variable for shared access
        DataManager.df = df

        return df

    @staticmethod
    def get_all_headers():
        if DataManager.df is not None:
            return DataManager.df.columns.tolist()
        else:
            raise ValueError("DataFrame not loaded or processed yet.")

    def get_header(self, disease):
        try:
            return DataManager.df.columns[DataManager.df.loc[disease.title()].astype(bool)].tolist()
        except KeyError:
            return DataManager.df.columns[DataManager.df.loc[disease.upper()].astype(bool)].tolist()
        except KeyError:
            raise KeyError("Could not find disease in data set")

    def save_data(self):
        if DataManager.df is not None:
            DataManager.df.to_csv(self.dest_filename)
        else:
            raise ValueError("DataFrame not loaded or processed yet.")