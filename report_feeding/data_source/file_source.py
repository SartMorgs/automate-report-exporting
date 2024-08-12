import csv


class FileDataSource:
    def __init__(self, source, filename):
        self.source = source
        self.filename = filename
        
        self.__SENT_TO_LABORATORY_STRING = 'Enviada ao laboratório'
        
    def read_file(self):
        # Refactor after adding more file sources besides csv
        with open(self.filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            return [row for row in csv_reader if self.__SENT_TO_LABORATORY_STRING in row]
