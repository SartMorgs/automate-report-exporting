import os
import shutil
from datetime import datetime


class MoveFile:
    def __init__(self):
        self.user_path = os.path.expanduser('~')
        self.current_datetime = datetime.now().strftime("%Y-%m-%d")

        
    def move_file_from_downloads(self, source_path, domain_folder, filename):
        target_folder = f'{self.user_path}\\Documents\\{domain_folder}'
        target_full_filename = f'{target_folder}\\{filename}-{self.current_datetime}.csv'
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(source_path, target_full_filename)
