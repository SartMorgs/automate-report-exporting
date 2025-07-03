from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class LightTransformation:
    def __init__(self):
        pass

    @staticmethod
    def process_csv_date_field(array_list, date_field):
        for entry in array_list:
            try:
                if entry[date_field]:
                    entry[date_field] = datetime.strptime(entry[date_field], "%d/%m/%Y").strftime("%Y-%m-%d")
                else:
                    entry[date_field] = None
            except ValueError as err:
                entry[date_field] = None
    
    @staticmethod
    def process_csv_int_field(array_list, int_field):
        for entry in array_list:
            try:
                if not isinstance(entry[int_field], int):
                    entry[int_field] = None
            except ValueError as err:
                entry[int_field] = None
    
    @staticmethod
    def process_csv_int_with_comma_and_period_field(array_list, int_field):
        for entry in array_list:
            try:
                entry[int_field] = int(entry[int_field].replace(".", "").replace(",00", ""))
                if not isinstance(entry[int_field], int):
                    entry[int_field] = None
            except ValueError as err:
                entry[int_field] = None
                

    @staticmethod
    def upper_strings_of_list(array_list):
        return [
            {key: value.upper() if isinstance(value, str) else value for key, value in item.items()}
            for item in array_list
        ]
