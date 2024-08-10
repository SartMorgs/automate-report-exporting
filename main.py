from rpa.main.report_export import ReportExportMain
from report_feeding.report.main.jit_generation import JitGeneration

report_export_main = ReportExportMain()
report_export_main.main()
jit_generation = JitGeneration()
jit_generation.generate()