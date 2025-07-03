import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from rpa.data_extraction.os.report_data import OsReportData
from rpa.data_extraction.customers.report_data import CustomerReportData
from rpa.common.move_file import MoveFile


class ReportExportMain:
    def __init__(self):
        self.user_path = os.path.expanduser("~")

        self.current_datetime = datetime.now()
        self.previous_day = self.current_datetime - timedelta(days=1)
        
        self.reference_date = self.previous_day.strftime("%d/%m/%Y")
        
        load_dotenv()
        self.final_code = int(os.getenv("FINAL_CODE", "30000"))
        
    def __move_file(self, report_name, old_file_name, new_file_name):
        move_file = MoveFile("otica-nany", report_name, new_file_name)
        source_path = f"{self.user_path}\\Downloads\\{old_file_name}.csv"
        move_file.move_file_from_downloads(source_path)
        
    def export_jit(self):
        os_report_data = OsReportData(self.reference_date, self.reference_date)
        os_report_data.generate_jit_report()
        self.__move_file("os", "pivot", "os")
        
    def export_customer(self):
        customer_report_data = CustomerReportData(self.final_code)
        customer_report_data.generate_customer_report()
        it_code = 5000
        while it_code <= self.final_code:
            self.__move_file("customer", f"customer_provider_{it_code}", f"customer_provider_{it_code}")
            it_code = it_code + 5000


if __name__ == "__main__":
    report_export_main = ReportExportMain()
    report_export_main.main()
