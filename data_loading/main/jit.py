import pandas as pd
from data_loading.models.jit import Jit
from data_loading.repositories.jit_repository import JitRepository
from data_loading.config.database import session
from data_processing.jit import Jit as processingJit


class JitMain():
    def __init__(self):
        self.jit_repository = JitRepository(session)
        self.processing_jit = processingJit()

        self.__VENDOR_ALIAS = {
            '6': 'Nany',
            '16': 'Nany',
            '20': 'Aline',
            '12': 'Marilete',
            '19': 'Adriana'
        }

    def __save_jit_as_not_generated(self, df):
        for index, row in df.iterrows():
            jit = Jit(
                os_date=row[self.processing_jit.OS_DATE_COLUMN],
                os_number=row[self.processing_jit.OS_NUMBER_COLUMN],
                laboratory=row[self.processing_jit.LABORATORY_COLUMN],
                customer_name=row[self.processing_jit.CUSTOMER_NAME_COLUMN],
                note=row[self.processing_jit.NOTE_COLUMN],
                due_date=row[self.processing_jit.DUE_DATE_COLUMN],
                vendor=self.__create_vendor_alias(row[self.processing_jit.VENDOR_ROW_COLUMN]),
                status=row[self.processing_jit.STATUS_COLUMN],
                is_generated=False
            )
            self.jit_repository.create_jit_only_if_doesnt_exist(jit)

    def __create_vendor_alias(self, vendor_name):
        vendor_code = vendor_name[:2].rstrip()
        return self.__VENDOR_ALIAS[vendor_code]
    
    def delete_all_jits(self):
        self.jit_repository.delete_all_jits()
            
    def create_jit(self):
        df = self.processing_jit.get_data()
        self.__save_jit_as_not_generated(df)
        
    def update_is_generated(self):
        df = self.processing_jit.get_data()
        for os in df[self.processing_jit.OS_NUMBER_COLUMN]:
            self.jit_repository.update_to_is_generated(os)
        
if __name__ == "__main__":
    jit = JitMain()
    jit.main()
