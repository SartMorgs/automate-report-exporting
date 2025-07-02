import re
from dataclasses import dataclass
from data_processing.light_transformation import LightTransformation

@dataclass(frozen=True)
class Jit(LightTransformation):
    OS_DATE_COLUMN = "os_data"
    OS_NUMBER_COLUMN = "os_number"
    LABORATORY_COLUMN = "laboratory"
    CUSTOMER_NAME_COLUMN = "customer_name"
    NOTE_COLUMN = "note"
    DUE_DATE_COLUMN = "due_date"
    VENDOR_ROW_COLUMN = "seller"
    STATUS_COLUMN = "status"

    def __init__(self):
        pass

    @staticmethod
    def get_jit_csv_column_names():
        return [
            Jit.OS_DATE_COLUMN, Jit.OS_NUMBER_COLUMN, Jit.LABORATORY_COLUMN, Jit.CUSTOMER_NAME_COLUMN,
            Jit.NOTE_COLUMN, Jit.DUE_DATE_COLUMN, Jit.VENDOR_ROW_COLUMN, Jit.STATUS_COLUMN
        ]

    @staticmethod
    def filter_note_column_for_valid_values(jit_list):
        string_regular_expression = r'[A-Za-z]'
        pattern = re.compile(string_regular_expression)
        condition_for_note_valid_columns = lambda row: not pattern.match(row[Jit.NOTE_COLUMN]) and row[Jit.NOTE_COLUMN] != "0"
        
        return [row for row in jit_list if condition_for_note_valid_columns]
