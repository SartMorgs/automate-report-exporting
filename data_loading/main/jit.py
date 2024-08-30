import pandas as pd
from data_loading.models.jit import Jit
from data_loading.repositories.jit_repository import JitRepository
from data_loading.config.database import session
from rpa.common.move_file import MoveFile


class JitMain():
    def __init__(self):
        self.domain = 'otica-nany'
        self.report_name = 'os'
        
        self.jit_repository = JitRepository(session)
        self.move_file = MoveFile(self.domain, self.report_name)
        
        self.__OS_DATE_COLUMN = 'Data OS'
        self.__OS_NUMBER_COLUMN = 'numero_os'
        self.__LABORATORY_COLUMN = 'Laboratório'
        self.__CUSTOMER_NAME_COLUMN = 'Nome Cliente'
        self.__NOTE_COLUMN = 'Observacao'
        self.__DUE_DATE_COLUMN = 'Previsão de Entrega'
        self.__VENDOR_ROW_COLUMN = 'Vendedor'
        self.__STATUS_COLUMN = 'DescricaoPosicao'

        self.__SENT_TO_LABORATORY_STRING = 'Enviada ao laboratório'

        self.__VENDOR_ALIAS = {
            '6': 'Nany',
            '16': 'Nany',
            '20': 'Aline',
            '12': 'Marilete',
            '19': 'Adriana'
        }
        
    def __read_file(self):
        df = pd.read_csv(self.move_file.SOURCE_REPORT_EXTRACTION_PATH)

        df[self.__OS_DATE_COLUMN] = pd.to_datetime(df[self.__OS_DATE_COLUMN], errors='coerce', dayfirst=True)
        df[self.__OS_NUMBER_COLUMN] = df[self.__OS_NUMBER_COLUMN].str.replace('.', '').str.replace(',00', '').astype(int)
        df[self.__DUE_DATE_COLUMN] = pd.to_datetime(df[self.__DUE_DATE_COLUMN], errors='coerce', dayfirst=True)
        
        return df[df[self.__STATUS_COLUMN] == self.__SENT_TO_LABORATORY_STRING]
    
    def __save_jit_as_not_generated(self, df):
        for index, row in df.iterrows():
            jit = Jit(
                os_date=row[self.__OS_DATE_COLUMN],
                os_number=row[self.__OS_NUMBER_COLUMN],
                laboratory=row[self.__LABORATORY_COLUMN],
                customer_name=row[self.__CUSTOMER_NAME_COLUMN],
                note=row[self.__NOTE_COLUMN],
                due_date=row[self.__DUE_DATE_COLUMN],
                vendor=self.__create_vendor_alias(row[self.__VENDOR_ROW_COLUMN]),
                status=row[self.__STATUS_COLUMN],
                is_generated=False
            )
            self.jit_repository.create_jit_only_if_doesnt_exist(jit)

    def __create_vendor_alias(self, vendor_name):
        vendor_code = vendor_name[:2]
        return self.__VENDOR_ALIAS[vendor_code]
    
    def delete_all_jits(self):
        self.jit_repository.delete_all_jits()
            
    def create_jit(self):
        df = self.__read_file()
        self.__save_jit_as_not_generated(df)
        
    def update_is_generated(self):
        df = self.__read_file()
        for os in df[self.__OS_NUMBER_COLUMN]:
            self.jit_repository.update_to_is_generated(os)
        
if __name__ == "__main__":
    jit = JitMain()
    jit.main()
