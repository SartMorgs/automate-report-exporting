from dataclasses import dataclass

@dataclass(frozen=True)
class Utils:
    JIT_COLUMNS_USED = ["A", "C", "E", "G"] # 1, 3, 5, 7
    FIRST_COLUMN_USED = 1
    COLUMN_INTERVAL = 2
        
    FIRST_ROW_USED = 1
    JIT_VERTICAL_SIZE = 6
    ROW_INTERVAL = 2
    JIT_COLUMN_SIZE = 24
    
    AMOUNT_OF_JITS_BY_LINE = 4

    STORE_VALUE = "LOJA"
    REPRO_VALUE = "REPRO"

    FIRST_CHAR = 0
    FIRST_NAME = 0
    LAST_NAME = -1

    FIRST_LIST_ITEM = 0
    SECOND_LIST_ITEM = 1

    CUSTOMER_NAME = "customer_name"
    SELLER_NAME = "seller_name"
    DUE_DATE = "due_date"
    OS_NUMBER = "os_number"
    NOTE = "note"

    BACKGROUND_COLOR_KEY = "background_color"
    FILL_TYPE_KEY = "fill_type"
    FONT_COLOR_KEY = "font_color"
    FONT_SIZE_KEY = "font_size"
    VALUE_KEY = "value"

    BORDER_STYLE = "thick"
    STORE_BACKGROUND_COLOR = "0000B050"
    REPRO_BACKGROUND_COLOR = "ff000000"
    FILL_TYPE = "solid"
    FONT_SIZE = 10
    FONT_COLLOR = "FFFFFF"
    
    def __init__(self):
        pass

    @staticmethod
    def get_jit_report_vertical_count(rows_count):
        return (rows_count // Utils.AMOUNT_OF_JITS_BY_LINE) + 1

    @staticmethod
    def split_list_by_space(str_list):
        return str_list.upper().split(" ")

    @staticmethod
    def get_list_of_strings_with_more_than_two_char(str_list):
        return [item for item in str_list if len(item) > 2]

    @staticmethod
    def get_first_letter_of_each_string(str_list):
        return [item[Utils.FIRST_CHAR] for item in str_list]

    @staticmethod
    def get_report_layout_positions(start_row):
        return {
            Utils.CUSTOMER_NAME: (start_row + 1),
            Utils.SELLER_NAME: (start_row + 2),
            Utils.DUE_DATE: (start_row + 3),
            Utils.OS_NUMBER: (start_row + 5),
            Utils.NOTE: (start_row + 6)
        }