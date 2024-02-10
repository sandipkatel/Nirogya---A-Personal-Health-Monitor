# manager.py

import pandas as pd

class DataManager:
    def __init__(self):
        self.df = None

    def load_and_process_data(self, source_filename, dest_filename):
        # Read the source file
        self.df = pd.read_csv(source_filename)

        # Drop duplicate data if any and reset index
        self.df.drop_duplicates(inplace = True)
        self.df.reset_index(drop=True, inplace=True)

        # Find the column containing the disease using the first object-type column
        index_col_to_be = next(col for col, dtype in self.df.dtypes.items() if dtype == "object")

        # Set index and capitalize it
        self.df[index_col_to_be.title()] = self.df.pop(index_col_to_be).apply(lambda x: x.title() if x != x.upper() else x)
        self.df.set_index([self.df.index, index_col_to_be.title()], inplace = True)
        # self.df.set_index(index_col.title(), inplace=True)


        # Replace underscores with spaces in column names and capitalize them
        self.df.columns = [col.replace("_", " ").title() for col in self.df.columns]

        # Sort the DataFrame by index and columns
        self.df.sort_index(axis=0, inplace=True)
        self.df.sort_index(axis=1, inplace=True)

        # Save the modified DataFrame to a new CSV file
        self.df.to_csv(dest_filename)
        return self.df

    """@staticmethod
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
            raise ValueError("DataFrame not loaded or processed yet.")"""