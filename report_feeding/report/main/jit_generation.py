import os
from datetime import datetime
from report_feeding.report.jit.layout_builder import LayoutBuilder
from report_feeding.report.jit.data_filler import FillerData
from data_loading.repositories.jit_repository import JitRepository
from data_loading.services.jit_service import JitService
from data_loading.config.database import session
from openpyxl import load_workbook


class JitGeneration:
    def __init__(self):

        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        self.table_name = 'jit'
        self.user_path = os.environ.get('STORE_PATH', None)

        self.__TARGET_FOLDER = f'{self.user_path}\\otica-nany\\jit'
        self.__TARGET_PATH = f'{self.__TARGET_FOLDER}\\jit-{self.current_datetime}.xlsx'
        
        self.__REPRO_STRING = '19944 - REPRO PRODUTOS OPTICOS LTDA'
        
        self.jit_repository = JitRepository(session)
        self.jit_service = JitService(self.jit_repository)

        self.data = self.__read_table()
        
    def __read_table(self):
        jit_table = self.jit_service.get_all()
        return [[jit.os_date, jit.os_number, jit.laboratory, jit.customer_name, jit.note, jit.due_date, jit.vendor, jit.status, jit.is_generated] for jit in jit_table]
    
    def __get_only_existant_data(self):
        return [jit for jit in self.data if self.jit_service.check_existance_of_jit_by_os_number(jit[1])]
    
    def __split_data_by_repro_and_store(self):
        existant_data = self.__get_only_existant_data()
        non_existent_data = [row for row in self.data if row not in existant_data]
        
        repro_data = []
        store_data = []
        for row in non_existent_data:
            if self.__REPRO_STRING in row:
                repro_data.append(row)
            else:
                store_data.append(row)
                
        return repro_data, store_data
    
    def __is_xlsx_empty(self, file_path):
        if self.__is_file_created(file_path):
            workbook = load_workbook(file_path, read_only=True)
            first_sheet = workbook.worksheets[0]
            first_cell = first_sheet['A1']
            return first_cell.value is None or first_cell.value == ""
        
        return True
    
    def __is_file_created(self, file_path):
        return os.path.exists(file_path)
    
    def generate(self):
        repro_data, store_data = self.__split_data_by_repro_and_store()
        repro_data_size = len(repro_data)
        full_data = store_data + repro_data
        
        os.makedirs(self.__TARGET_FOLDER, exist_ok=True)

        if self.__is_xlsx_empty(self.__TARGET_PATH):
            filler_data = FillerData(self.__TARGET_PATH, full_data, repro_data_size)
            filler_data.build_and_fill()

if __name__ == "__main__":
    jit_generation = JitGeneration()
    jit_generation.generate()

