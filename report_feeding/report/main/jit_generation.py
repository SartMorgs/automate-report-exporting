import os
from datetime import datetime
from report_feeding.data_source.file_source import FileDataSource as FileDS
from report_feeding.report.jit.layout_builder import LayoutBuilder
from report_feeding.report.jit.data_filler import FillerData


class JitGeneration:
    def __init__(self):
        self.user_path = os.path.expanduser('~')

        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        self.__SOURCE_PATH = f'{self.user_path}\\Documents\\otica-nany\\os\\os-{self.current_datetime}.csv'
        self.__TARGET_FOLDER = f'{self.user_path}\\Documents\\otica-nany\\jit'
        self.__TARGET_PATH = f'{self.__TARGET_FOLDER}\\jit-{self.current_datetime}.xlsx'
        
        self.__REPRO_STRING = '19944 - REPRO PRODUTOS OPTICOS LTDA'
        
        self.file_data_source = FileDS('csv', self.__SOURCE_PATH)
        self.data = self.file_data_source.read_file()
    
    def __split_data_by_repro_and_store(self):
        repro_data = []
        store_data = []
        for row in self.data[1:]:
            if self.__REPRO_STRING in row:
                repro_data.append(row)
            else:
                store_data.append(row)
                
        return repro_data, store_data
    
    def generate(self):
        repro_data, store_data = self.__split_data_by_repro_and_store()
        repro_data_size = len(repro_data)
        full_data = store_data + repro_data
        
        os.makedirs(self.__TARGET_FOLDER, exist_ok=True)
        
        layout_builder = LayoutBuilder(len(full_data), self.__TARGET_PATH, repro_data_size)
        layout_builder.build()

        filler_data = FillerData(self.__TARGET_PATH, full_data)
        filler_data.fill()

if __name__ == "__main__":
    jit_generation = JitGeneration()
    jit_generation.generate()

