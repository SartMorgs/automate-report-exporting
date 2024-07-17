from datetime import datetime, timedelta
from rpa.data_extraction.os.report_data import OsReportData


class ReportExportMain:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.previous_day = self.current_datetime - timedelta(days=1)
        
        self.start_date = self.previous_day.strftime("%d/%m/%Y")
        self.end_date = self.current_datetime.strftime("%d/%m/%Y")
        
        self.os_report_data = OsReportData(self.start_date, self.end_date)
        
    def main(self):
        self.os_report_data.generate_jit_report()


if __name__ == "__main__":
    report_export_main = ReportExportMain()
    report_export_main.main()
