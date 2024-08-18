import os
import shutil
from datetime import datetime


class MoveFile:
    def __init__(self, domain, report_name):
        self.user_path = os.path.expanduser('~')
        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        self.__CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d")
        self.__USER_PATH = os.path.expanduser('~')
        self.__SOURCE_REPORT_FOLDER = f'{self.__USER_PATH}\\Documents\\{domain}\\{report_name}'
        self.SOURCE_REPORT_EXTRACTION_PATH = f'{self.__SOURCE_REPORT_FOLDER}\\{report_name}-{self.__CURRENT_DATETIME}.csv'
        self.TARGET_FOLDER = f'{self.__USER_PATH}\\Documents\\otica-nany\\jit'

        
    def move_file_from_downloads(self, source_path):
        os.makedirs(self.__SOURCE_REPORT_FOLDER, exist_ok=True)
        shutil.move(source_path, self.SOURCE_REPORT_EXTRACTION_PATH)
