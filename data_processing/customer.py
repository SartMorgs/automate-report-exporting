from datetime import datetime
from dataclasses import dataclass
from data_processing.light_transformation import LightTransformation
from typing import List, Dict


@dataclass(frozen=True)
class Customer(LightTransformation):
    """
    Data Processing: Customer Static Class
    
    Used for supporting data reading from csv adding correct column names and filtering valid values based on cpf column.
    """
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
    
    CPF_NUMBER_OF_DIGITS = 11
    CPF_FIRST_DIGIT_INDEX = 0
    CPF_9_FIRSTS_DIGITS_INDEX = 9
    CPF_10_FIRST_DIGITS_INDEX = 10
    CPF_LAST_TWO_DIGITS = -2
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_customer_csv_column_names():
        """
        (Static) Gets Customer columns names for renaming when reading csv.
        """
        return [
            Customer.ID, Customer.NAME, Customer.FANTASY_NAME, Customer.CPF, Customer.CEP, Customer.ADDRESS,
            Customer.HOUSE_NUMBER, Customer.COMPLEMENT, Customer.NEIGHBORHOOD, Customer.CITY, Customer.STATE,
            Customer.COUNTRY, Customer.PHONE_NUMBER, Customer.CELLPHONE_NUMBER, Customer.EMAIL, Customer.REGISTER_DATE,
            Customer.LAST_PRODUCT_BOUGHT, Customer.CUSTOMER_TYPE, Customer.BIRTHDAY
        ]

    @staticmethod
    def is_nan_string(value: str):
        """
        (Static) Checks if the value is ```nan```.
        
        Args:
            value (str): Value to check if is ```nan```.
        
        Returns:
            True if the value is ```nan``` and False if it's not.
        """
        return value.lower() == "nan"

    @staticmethod
    def is_cpf_number_of_digits_valid(cpf_number: str):
        """
        (Static) Checks if number of digits are valid.
        
        Args:
            cpf_number (str): CPF number.
        
        Returns:
            `True` if number of digits are valid and `False` if it's not.
        """
        return len(cpf_number) != Customer.CPF_NUMBER_OF_DIGITS or cpf_number == cpf_number[Customer.CPF_FIRST_DIGIT_INDEX] * len(cpf_number)
    
    @staticmethod
    def is_cpf_value_valid(cpf_number: str):
        """
        (Static) Checks if CPF number is valid following standard rule.
        
        Args:
            cpf_number (str): CPF number.
        
        Returns:
            `True` if cpf is valid and `False` if it's not.
        """
        sum_first = sum(int(cpf_number[digit]) * (Customer.CPF_10_FIRST_DIGITS_INDEX - digit) for digit in range(Customer.CPF_9_FIRSTS_DIGITS_INDEX))
        first_digit = Customer.calculate_validating_digit(sum_first)

        sum_second = sum(int(cpf_number[digit]) * (Customer.CPF_NUMBER_OF_DIGITS - digit) for digit in range(Customer.CPF_10_FIRST_DIGITS_INDEX))
        second_digit = Customer.calculate_validating_digit(sum_second)
        
        return cpf_number[Customer.CPF_LAST_TWO_DIGITS:] == f"{first_digit}{second_digit}"
    
    @staticmethod
    def calculate_validating_digit(sum_number: int):
        """
        (Static) Calculates the validating digit based on standard rule and given sum number.
        
        Args:
            sum_number (int): Sum number after applying digit sums rule.
        
        Returns:
            Validating digit.
        """
        return (sum_number * Customer.CPF_10_FIRST_DIGITS_INDEX % Customer.CPF_NUMBER_OF_DIGITS) % Customer.CPF_10_FIRST_DIGITS_INDEX

    @staticmethod
    def valida_cpf(cpf_number: str):
        """
        (Static) Validates CPF number, checking if the number of digits are valid and if the value is valid.
        
        Args:
            cpf_number (str): CPF number.
        
        Returns:
            `True` if cpf is valid and `False` if it's not.
        """
        if Customer.is_nan_string(str(cpf_number)):
            return False
        cpf_number = "".join(filter(str.isdigit, cpf_number))

        if Customer.is_cpf_number_of_digits_valid(cpf_number):
            return False

        return Customer.is_cpf_value_valid(cpf_number)

    @staticmethod
    def is_cpf_valid(cpf_number: str, is_looking_for_valid: bool):
        """
        (Static) Checks if the cpf is valid.
        
        Args:
            cpf_number (str): CPF number.
            is_looking_for_valid (bool): `True` if is looking for valid ones.
        
        Returns:
            `True` if CPF is valid and `is_looking_for_valid` is also `True` or CPF is invalid and `is_looking_for_valid` is `False`
        """
        return Customer.valida_cpf(cpf_number) == is_looking_for_valid

    @staticmethod
    def intersect_columns_diff(list1: List[Dict[str, str]], list2: List[Dict[str, str]], retain_keys=None):
        """
        (Static) Removes the keys in a list that are in a second list provided.
        
        Args:
            list1 (List[Dict[str, str]]): List to remove the keys.
            list2 (List[Dict[str, str]]): List with keys that should be removed from first list.
        
        Returns:
            list1 with the keys in list2 removed.
        """
        if not list1 or not list2:
            return list1

        if retain_keys is None:
            retain_keys = []

        keys_in_list2 = set().union(*(item.keys() for item in list2))

        result = [
            {
                key: value for key, value in entry.items()
                if key not in keys_in_list2 or key in retain_keys
            }
            for entry in list1
        ]

        return result
