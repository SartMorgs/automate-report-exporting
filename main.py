from rpa.main.report_export import ReportExportMain
from data_loading.main.jit import JitMain
from data_loading.main.customer import CustomerMain
from report_feeding.report.main.jit_generation import JitGeneration
from data_loading.config.database import init_db


report_export_main = ReportExportMain()
report_export_main.main()

init_db()

# CUSTOMER
customer_database_feeding = CustomerMain()
customer_database_feeding.create_all_customers()

# JIT
# jit_database_feeding = JitMain()
# jit_database_feeding.create_jit()
# jit_generation = JitGeneration()
# jit_generation.generate()
# jit_database_feeding.update_is_generated()
