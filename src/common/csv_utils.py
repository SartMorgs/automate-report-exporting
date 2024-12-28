from datetime import datetime

class CsvUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_client_csv_column_names():
        return [
            'id', 'name', 'fantasy_name', 'cpf', 'cep', 'address', 'house_number', 'complement', 'neighborhood',
            'city', 'state', 'country', 'phone_number', 'cellphone_number', 'email', 'register_date',
            'last_product_bought', 'client_type', 'birthday'
        ]
    
    @staticmethod
    def valida_cpf(cpf: str) -> bool:
        if CsvUtils.is_nan_string(str(cpf)):
            return False
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
            return False

        sum_first = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_first * 10 % 11) % 10

        sum_second = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_second * 10 % 11) % 10

        return cpf[-2:] == f"{first_digit}{second_digit}"

    @staticmethod
    def validate_csv_cpf( cpf, condition):
        if condition:
            return CsvUtils.valida_cpf(cpf)
        return not CsvUtils.valida_cpf(cpf)

    @staticmethod
    def is_nan_string(value):
        return value.lower() == 'nan'

    @staticmethod
    def intersect_columns_diff(list1, list2, retain_keys=None):
        if not list1 or not list2:
            return list1
        
        if retain_keys is None:
            retain_keys = []

        
        keys_in_list2 = set().union(*(d.keys() for d in list2))
        
        result = [
            {key: value for key, value in entry.items() if key not in keys_in_list2 or key in retain_keys}
            for entry in list1
        ]
        
        return result

    @staticmethod
    def process_csv_date_field(array_list, date_field):
        for entry in array_list:
            try:
                if entry[date_field]:
                    entry[date_field] = datetime.strptime(entry[date_field], "%d/%m/%Y").strftime("%Y-%m-%d")
                else:
                    entry[date_field] = None
            except ValueError as e:
                entry[date_field] = None

    @staticmethod
    def process_csv_int_field(array_list, date_field):
        for entry in array_list:
            try:
                if not isinstance(entry[date_field], int):
                    entry[date_field] = None
            except ValueError as e:
                entry[date_field] = None
