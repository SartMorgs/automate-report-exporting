import os
from datetime import datetime, timedelta
from rpa.data_extraction.os.report_data import OsReportData
from rpa.common.move_file import MoveFile


class ReportExportMain:
    def __init__(self):
        self.user_path = os.path.expanduser('~')

        self.current_datetime = datetime.now()
        self.previous_day = self.current_datetime - timedelta(days=1)
        
        self.start_date = self.previous_day.strftime("%d/%m/%Y")
        self.end_date = self.current_datetime.strftime("%d/%m/%Y")
        
        self.os_report_data = OsReportData(self.start_date, self.end_date)
        
    def __move_file(self, report_name):
        move_file = MoveFile()
        source_path = f'{self.user_path}\\Downloads\\pivot.csv'
        move_file.move_file_from_downloads(source_path, f'otica-nany\\{report_name}', report_name)
        
        
    def main(self):
        self.os_report_data.generate_jit_report()
        self.__move_file('os')


if __name__ == "__main__":
    report_export_main = ReportExportMain()
    report_export_main.main()
