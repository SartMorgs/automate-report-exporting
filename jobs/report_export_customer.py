from rpa.main.report_export import ReportExportMain
from data_loading.config.database import init_db
from data_loading.main.customer import CustomerMain


report_export_main = ReportExportMain()
init_db()

# CUSTOMER
report_export_main.export_customer()

customer_database_feeding = CustomerMain()
customer_database_feeding.create_all_customers()