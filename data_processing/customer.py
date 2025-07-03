from datetime import datetime
from dataclasses import dataclass
from data_processing.light_transformation import LightTransformation


@dataclass(frozen=True)
class Customer(LightTransformation):
    ID = "id"
    NAME = "name"
    FANTASY_NAME = "fantasy_name"
    CPF = "cpf"
    BIRTHDAY = "birthday"
    CUSTOMER_TYPE = "customer_type"
    REGISTER_DATE = "register_date"
    LAST_PRODUCT_BOUGHT = "last_product_bought"
    ACTIVE = "active"
    CEP = "cep"
    ADDRESS = "address"
    HOUSE_NUMBER = "house_number"
    COMPLEMENT = "complement"
    NEIGHBORHOOD = "neighborhood"
    CITY = "city"
    STATE = "state"
    COUNTRY = "country"
    PHONE_NUMBER = "phone_number"
    CELLPHONE_NUMBER = "cellphone_number"
    EMAIL = "email"
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_customer_csv_column_names():
        return [
            Customer.ID, Customer.NAME, Customer.FANTASY_NAME, Customer.CPF, Customer.CEP, Customer.ADDRESS,
            Customer.HOUSE_NUMBER, Customer.COMPLEMENT, Customer.NEIGHBORHOOD, Customer.CITY, Customer.STATE,
            Customer.COUNTRY, Customer.PHONE_NUMBER, Customer.CELLPHONE_NUMBER, Customer.EMAIL, Customer.REGISTER_DATE,
            Customer.LAST_PRODUCT_BOUGHT, Customer.CUSTOMER_TYPE, Customer.BIRTHDAY
        ]

    @staticmethod
    def is_nan_string(value):
        return value.lower() == "nan"

    @staticmethod
    def valida_cpf(cpf: str) -> bool:
        if Customer.is_nan_string(str(cpf)):
            return False
        cpf = "".join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
            return False

        sum_first = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_first * 10 % 11) % 10

        sum_second = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_second * 10 % 11) % 10

        return cpf[-2:] == f"{first_digit}{second_digit}"

    @staticmethod
    def validate_csv_cpf(cpf, condition):
        if condition:
            return Customer.valida_cpf(cpf)
        return not Customer.valida_cpf(cpf)

    @staticmethod
    def intersect_columns_diff(list1, list2, retain_keys=None):
        if not list1 or not list2:
            return list1

        if retain_keys is None:
            retain_keys = []

        keys_in_list2 = set().union(*(item.keys() for item in list2))

        result = [
            {key: value for key, value in entry.items() if key not in keys_in_list2 or key in retain_keys}
            for entry in list1
        ]

        return result
