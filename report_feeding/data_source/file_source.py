import csv


class FileDataSource:
    def __init__(self, source, filename):
        self.source = source
        self.filename = filename
        
    def read_file(self):
        # Refactor after adding more file sources besides csv
        with open(self.filename, mode='r') as file:
            csv_reader = csv.reader(file)
            
            return [row for row in csv_reader]
