from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Utils:
    """
    Report Feeding: Jit Utils Static Class
    
    Used for some light data transformations needed for Jit report feeding.
    """
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
    def get_jit_report_vertical_count(rows_count: int):
        """
        Gets number of jits in vertical axis.
        
        Args:
            rows_count (int): number of rows in source data.
            
        Returns:
            Number of jits in vertical axis
        """
        return (rows_count // Utils.AMOUNT_OF_JITS_BY_LINE) + 1

    @staticmethod
    def split_list_by_space(str_list: str):
        """
        Splits string in list by space.
        
        Args:
            str_list (str): String to split in list.
            
        Returns:
            list with upper values.
        """
        return str_list.upper().split(" ")

    @staticmethod
    def get_list_of_strings_with_more_than_two_char(str_list: List[str]):
        """
        Gets list of values with size greater than 2 given list of string.
        
        Args:
            str_list (List[str]): List of strings.
        
        Returns:
            list with all string with size greater than 2.
        """
        return [item for item in str_list if len(item) > 2]

    @staticmethod
    def get_first_letter_of_each_string(str_list: List[str]):
        """
        Gets a lits of all firsts letter of each string in a list.
        
        Args:
            str_list (List[str]): List of strings.
        
        Returns:
            list with all first letters in each string given.
        """
        return [item[Utils.FIRST_CHAR] for item in str_list]

    @staticmethod
    def get_report_layout_positions(start_row: int):
        """
        Gets dictionary with the card layout, the position in the report spreadsheet which the card is gonna be posted.
        
        Args:
            start_row (int): start position for the card in the spreadsheet.
            
        Returns:
            Dictionary with keys as type of infos and values the position for each info.
        """
        return {
            Utils.CUSTOMER_NAME: (start_row + 1),
            Utils.SELLER_NAME: (start_row + 2),
            Utils.DUE_DATE: (start_row + 3),
            Utils.OS_NUMBER: (start_row + 5),
            Utils.NOTE: (start_row + 6)
        }