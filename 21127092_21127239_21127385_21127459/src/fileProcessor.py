import csv

class FileProcessor:
    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                result = []
                for row in reader:
                    result_row = []
                    for item in row:
                        result_row.append(int(item))
                    result.append(result_row)
                return result
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None
        
    @staticmethod
    def write_file(file_path, data):
        try:
            with open(file_path, 'w') as f:
                writer = csv.writer(f, delimiter=' ', lineterminator='\n')
                writer.writerows(data)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

