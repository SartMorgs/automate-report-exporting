JIT_COLUMNS_USED = ['A', 'C', 'E', 'G'] # 1, 3, 5, 7
FIRST_COLUMN_USED = 1
COLUMN_INTERVAL = 2
        
FIRST_ROW_USED = 1
JIT_VERTICAL_SIZE = 6
ROW_INTERVAL = 2
JIT_COLUMN_SIZE = 24

AMOUNT_OF_JITS_BY_LINE = 4

STORE_VALUE = 'LOJA'
REPRO_VALUE = 'REPRO'

FIRST_CHAR = 0
FIRST_NAME = 0
LAST_NAME = -1

FIRST_LIST_ITEM = 0
SECOND_LIST_ITEM = 1

def get_jit_report_vertical_count(rows_count):
    return (rows_count // AMOUNT_OF_JITS_BY_LINE) + 1

def split_list_by_space(str_list):
    return str_list.upper().split(" ")

def get_list_of_strings_with_more_than_two_char(str_list):
    return [item for item in str_list if len(item) > 2]

def get_first_letter_of_each_string(str_list):
    return [item[FIRST_CHAR] for item in str_list]
