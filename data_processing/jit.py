import pandas as pd
from rpa.common.move_file import MoveFile

class Jit:
    def __init__(self):
        self.domain = 'otica-nany'
        self.report_name = 'os'

        self.OS_DATE_COLUMN = 'Data OS'
        self.OS_NUMBER_COLUMN = 'numero_os'
        self.LABORATORY_COLUMN = 'Laboratório'
        self.CUSTOMER_NAME_COLUMN = 'Nome Cliente'
        self.NOTE_COLUMN = 'Observacao'
        self.DUE_DATE_COLUMN = 'Previsão de Entrega'
        self.VENDOR_ROW_COLUMN = 'Vendedor'
        self.STATUS_COLUMN = 'DescricaoPosicao'
        self.SENT_TO_LABORATORY_STRING = 'Enviada ao laboratório'
        
        self.move_file = MoveFile(self.domain, self.report_name, 'os')
        
    def __get_send_to_laboratory_data(self):
        df = pd.read_csv(self.move_file.SOURCE_REPORT_EXTRACTION_PATH)

        df[self.OS_DATE_COLUMN] = pd.to_datetime(df[self.OS_DATE_COLUMN], errors='coerce', dayfirst=True)
        df[self.OS_NUMBER_COLUMN] = df[self.OS_NUMBER_COLUMN].str.replace('.', '').str.replace(',00', '').astype(int)
        df[self.DUE_DATE_COLUMN] = pd.to_datetime(df[self.DUE_DATE_COLUMN], errors='coerce', dayfirst=True)
        
        return df[df[self.STATUS_COLUMN] == self.SENT_TO_LABORATORY_STRING]
    
    
    def __filter_note_column_for_valid_values(self, df):
        string_regular_expression = r'[A-Za-z]'
        only_integer_note_column_df = df[~df[self.NOTE_COLUMN].str.contains(string_regular_expression, na=False)]
        return only_integer_note_column_df[only_integer_note_column_df[self.NOTE_COLUMN] != '0']
    
    def get_data(self):
        df = self.__get_send_to_laboratory_data()
        return self.__filter_note_column_for_valid_values(df)
