from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class LightTransformation:
    """
    Data Processing: Light Transformation Static Class
    
    Used to light data transformations in columns, such as:
        - string to date/timestamp
        - string to int
        - cleaning int as string removing commas and additional zeros
        - upper/lower strings
    """
    def __init__(self):
        pass

    @staticmethod
    def process_csv_date_field(list_of_data: List[Dict[str, str]], date_field: str):
        """
        (Static) Converts date string data for date type from array list.
        
        Args:
            list_of_data (List[Dict[str, str]]): Source data.
            date_field (str): Date field name.
        """
        for entry in list_of_data:
            try:
                if entry[date_field]:
                    entry[date_field] = datetime.strptime(entry[date_field], "%d/%m/%Y").strftime("%Y-%m-%d")
                else:
                    entry[date_field] = None
            except ValueError as err:
                entry[date_field] = None
    
    @staticmethod
    def process_csv_int_field(list_of_data: List[Dict[str, str]], int_field: str):
        """
        (Static) Converts numeric entries from string to integer type
        
        Args:
            list_of_data (List[Dict[str, str]]): Source data.
            int_field (str): Int field name.
        """
        for entry in list_of_data:
            try:
                if not isinstance(entry[int_field], int):
                    entry[int_field] = None
            except ValueError as err:
                entry[int_field] = None
    
    @staticmethod
    def process_csv_int_with_comma_and_period_field(list_of_data: List[Dict[str, str]], int_field: str):
        """
        (Static) Cleans numeric entries thata are as string type, removing commas, period and aditional zeros.
        
        Args:
            list_of_data: List[Dict[str, str]]: Source data.
            int_field (str): Int field name.
        """
        for entry in list_of_data:
            try:
                entry[int_field] = int(entry[int_field].replace(".", "").replace(",00", ""))
                if not isinstance(entry[int_field], int):
                    entry[int_field] = None
            except ValueError as err:
                entry[int_field] = None
                

    @staticmethod
    def upper_strings_of_list(list_of_data: List[Dict[str, str]]):
        """
        (Static) Uppers strings among dict values of list.
        
        Args:
            list_of_data: List[Dict[str, str]]: Source data.
        """
        return [
            {key: value.upper() if isinstance(value, str) else value for key, value in item.items()}
            for item in list_of_data
        ]
