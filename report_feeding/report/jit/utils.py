JIT_COLUMNS_USED = ['A', 'C', 'E', 'G'] # 1, 3, 5, 7
FIRST_COLUMN_USED = 1
COLUMN_INTERVAL = 2
        
FIRST_ROW_USED = 1
JIT_VERTICAL_SIZE = 6
ROW_INTERVAL = 2

AMOUNT_OF_JITS_BY_LINE = 4

STORE_VALUE = 'LOJA'
REPRO_VALUE = 'REPRO'

def get_jit_report_vertical_count(rows_count):
        return (rows_count // AMOUNT_OF_JITS_BY_LINE) + 1