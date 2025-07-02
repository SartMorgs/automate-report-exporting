from rpa.main.report_export import ReportExportMain
from data_loading.config.database import init_db
from data_loading.main.jit import JitMain
from report_feeding.report.main.jit_generation import JitGeneration


report_export_main = ReportExportMain()
init_db()

# JIT
report_export_main.export_jit()

jit_database_feeding = JitMain()
jit_database_feeding.create_jit()
jit_generation = JitGeneration()
jit_generation.generate()
jit_database_feeding.update_is_generated()