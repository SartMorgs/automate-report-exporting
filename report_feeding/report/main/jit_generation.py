import os
from datetime import datetime
from report_feeding.report.jit.layout_builder import LayoutBuilder
from report_feeding.report.jit.data_filler import FillerData
from data_loading.repositories.jit_repository import JitRepository
from data_loading.services.jit_service import JitService
from data_loading.config.database import session
from data_processing.jit import Jit as JitProcess
from openpyxl import load_workbook


class JitGeneration:
    """
    Report Feeding: Jit Generation Class
    
    Used to generate the Jit report in the spreadsheet file.
    """
    def __init__(self):

        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        self.table_name = "jit"
        self.user_path = os.environ.get("STORE_PATH", None)

        self.__TARGET_FOLDER = f"{self.user_path}\\otica-nany\\jit"
        self.__TARGET_PATH = f"{self.__TARGET_FOLDER}\\jit-{self.current_datetime}.xlsx"
        
        self.__REPRO_STRING = "19944 - REPRO PRODUTOS OPTICOS LTDA"
        
        self.jit_repository = JitRepository(session)
        self.jit_service = JitService(self.jit_repository)

        self.data = self.__read_table()

    def __read_table(self):
        """
        Reads the table and generates a list of dictionaries with the data to fill the report.
        
        Returns:
            A list of dictionaries with the data to fill the report. (List[Dict[str, Any]])
        """
        jit_table = self.jit_service.get_all_not_generated_jit()
        return [
            {
                JitProcess.OS_DATE_COLUMN: jit.os_date,
                JitProcess.OS_NUMBER_COLUMN: jit.os_number,
                JitProcess.LABORATORY_COLUMN: jit.laboratory,
                JitProcess.CUSTOMER_NAME_COLUMN: jit.customer_name,
                JitProcess.NOTE_COLUMN: jit.note,
                JitProcess.DUE_DATE_COLUMN: jit.due_date,
                JitProcess.SELLER_COLUMN: jit.vendor,
                JitProcess.STATUS_COLUMN: jit.status,
                JitProcess.IS_GENERATED_COLUMN: jit.is_generated
            } for jit in jit_table
        ]
    
    def __split_data_by_repro_and_store(self):
        """
        Splits the data by repro type and store type
        
        Returns:
            Two list of dicts, one for repro data and another for store data. (List[Dict[str, Any]])
        """
        repro_data = []
        store_data = []
        for row in self.data:
            repro_data.append(row) if self.__REPRO_STRING in row[JitProcess.LABORATORY_COLUMN] else store_data.append(row)
                
        return repro_data, store_data
    
    def __is_xlsx_empty(self, file_path: str):
        """
        Checks if the ```.xlsx``` file is empty.
        
        Args:
            file_path (str): The file path where the file is created.
        """
        if self.__is_file_created(file_path):
            workbook = load_workbook(file_path, read_only=True)
            first_sheet = workbook.worksheets[0]
            first_cell = first_sheet["A1"]
            return first_cell.value is None or first_cell.value == ""
        
        return True
    
    def __is_file_created(self, file_path):
        """
        Checks if the file is created.
        
        Args:
            file_path (str): The file path where the file should be created.
        """
        return os.path.exists(file_path)
    
    def generate(self):
        """
        Generates the ```.xlsx``` report file given the jit data in the database.
        """
        repro_data, store_data = self.__split_data_by_repro_and_store()
        repro_data_size = len(repro_data)
        full_data = store_data + repro_data
        
        os.makedirs(self.__TARGET_FOLDER, exist_ok=True)

        if self.__is_xlsx_empty(self.__TARGET_PATH):
            filler_data = FillerData(self.__TARGET_PATH, full_data, repro_data_size)
            filler_data.build_and_fill_report_cards()

if __name__ == "__main__":
    jit_generation = JitGeneration()
    jit_generation.generate()
