class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

class DataManager:
    def __init__(self):
        self.data = LinkedList()
        self.columns = []

    def load_and_process_data(self, source_filename, dest_filename, set_index=False):
        with open(source_filename, 'r') as file:
            # Read header to extract column names
            header = file.readline().strip().split(',')
            self.columns = header

            # Skip header and read data
            for line in file:
                row = line.strip().split(',')
                self.data.add(row)

        # Now you can perform various operations on self.data
        # For example, you can implement functions to remove duplicates, sort, search, etc.

        # Save the modified data to a new CSV file
        with open(dest_filename, 'w') as file:
            # Write header
            file.write(','.join(self.columns) + '\n')

            current = self.data.head
            while current:
                file.write(','.join(current.data) + '\n')
                current = current.next

        # Simulating DataFrame behavior by providing similar interface
        class DataFrameLike:
            def __init__(self, data_manager):
                self.data_manager = data_manager

            def __getitem__(self, key):
                # Implement column access
                if isinstance(key, str):
                    if key in self.data_manager.columns:
                        index = self.data_manager.columns.index(key)
                        result = []
                        current = self.data_manager.data.head
                        while current:
                            result.append(current.data[index])
                            current = current.next
                        return result
                    else:
                        raise KeyError(f"Column '{key}' not found.")
                else:
                    raise TypeError("Only column name access is supported.")

            def to_csv(self, filename):
                # Save DataFrame as CSV
                with open(filename, 'w') as file:
                    # Write header
                    file.write(','.join(self.data_manager.columns) + '\n')

                    current = self.data_manager.data.head
                    while current:
                        file.write(','.join(current.data) + '\n')
                        current = current.next

            def __repr__(self):
                # Implement representation
                return repr(self.data_manager.data)

        return DataFrameLike(self)



def main():
    data_manager = DataManager()
    df = data_manager.load_and_process_data("dataset/AdditionalSet/testing.csv", "output0.csv")
    df.to_csv('new_output.csv')


main()