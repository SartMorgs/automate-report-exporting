import csv
from data_loading.repositories.customer_repository import CustomerRepository
from data_processing.customer import Customer as CustomerProcess
from data_loading.models.customer import Customer
from data_loading.models.customer_contact_info import CustomerContactInfo
from typing import List, Dict


class CustomerService:
    """
    Services: Customer Class.
    
    Used to create/update customers and customer's info on the database based in the report files extracted by RPA.
    It also is used for validating customers based on CPF and mark them as active or not active.
    
    Attributes:
        customer_repository (CustomerRepository)
    """
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repo = customer_repository

    def __get_customer_list(self, customers_file):
        """
        Gets all valid customer list from csv file. It marks all customers as active unless it has non valid CPF.
        
        Args:
            customers_file (str): Filename used to read the customers.
            
        Returns:
            List of all active customers
        """
        filtered_data = []
        with open(customers_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', fieldnames=CustomerProcess.get_customer_csv_column_names())

            for row in reader:
                row[CustomerProcess.ACTIVE] = True
                if CustomerProcess.is_cpf_valid(row[CustomerProcess.CPF], False):
                    row[CustomerProcess.ACTIVE] = False
                filtered_data.append(row)
 
        return filtered_data[1:]

    def __process_customer(self, customer_list: List[Dict[str, str]], customer_contact_info_list: List[Dict[str, str]]):
        """
        Applies some light data transformation in the customer data, such as date formatting and str to int casting.
        
        Args:
            customer_list (List[Dict[str,str]]): List of customer dictionaries
            customer_contact_info_list (List[Dict[str,str]]): List of customer contact info dictionaries
        """
        CustomerProcess.process_csv_date_field(customer_list, CustomerProcess.BIRTHDAY)
        CustomerProcess.process_csv_date_field(customer_list, CustomerProcess.REGISTER_DATE)
        CustomerProcess.process_csv_int_field(customer_contact_info_list, CustomerProcess.HOUSE_NUMBER)
    
    def __create_customer_by_list(self, customer_list: List[Dict[str, str]]):
        """
        Creates customer by list of customer dictionaries if it doesn't exist in the database.
        It creates a Customer object based in each item of the list provided.
        
        Args:
            customer_list (List[Dict[str,str]]): List of customer dictionaries
        """
        for entry in customer_list:
            customer = Customer(
                id = entry[CustomerProcess.ID],
                name = entry[CustomerProcess.NAME],
                fantasy_name = entry[CustomerProcess.FANTASY_NAME],
                cpf = entry[CustomerProcess.CPF],
                birthday = entry[CustomerProcess.BIRTHDAY],
                customer_type = entry[CustomerProcess.CUSTOMER_TYPE],
                register_date = entry[CustomerProcess.REGISTER_DATE],
                last_product_bought = entry[CustomerProcess.LAST_PRODUCT_BOUGHT],
                active = entry[CustomerProcess.ACTIVE]
            )
            self.customer_repo.create_customer_only_if_doesnt_exist(customer)
    
    def __create_customer_contact_info_by_list(self, customer_contact_info_list: List[Dict[str, str]]):
        """
        Creates customer contact info by list of customer contact info dictionaries if it doesn't exist in the database.
        It creates a CustomerContactInfo object based in the ecch item of the list provided.
        
        Args:
            customer_contact_info_list (List[Dict[str,str]]): List of customer contact info dictionaries
        """
        for entry in customer_contact_info_list:
            customer_contact_info = CustomerContactInfo(
                id = entry[CustomerProcess.ID],
                cep = entry[CustomerProcess.CEP],
                address = entry[CustomerProcess.ADDRESS],
                house_number = entry[CustomerProcess.HOUSE_NUMBER],
                complement = entry[CustomerProcess.COMPLEMENT],
                neighborhood = entry[CustomerProcess.NEIGHBORHOOD],
                city = entry[CustomerProcess.CITY],
                state = entry[CustomerProcess.STATE],
                country = entry[CustomerProcess.COUNTRY],
                phone_number = entry[CustomerProcess.PHONE_NUMBER],
                cellphone_number = entry[CustomerProcess.CELLPHONE_NUMBER],
                email = entry[CustomerProcess.EMAIL]
            )
            self.customer_repo.create_customer_contact_info_only_if_it_doesnt_exist(customer_contact_info)

    def validate_and_save_customer_on_db(self, customers_file: str):
        """
        Validates customer and saves customer and customer contact info in the database.
        It apply some light data transformation to guarantee valid date formating number in the proper data type.
        It generates both data: customer and customer contact info.
        
        Args:
            customers_file (str): Filename used to read the customers.
        """
        raw_customers_list = self.__get_customer_list(customers_file)

        customer_list = [
            {
                CustomerProcess.ID: item[CustomerProcess.ID],
                CustomerProcess.NAME: item[CustomerProcess.NAME],
                CustomerProcess.FANTASY_NAME: item[CustomerProcess.FANTASY_NAME],
                CustomerProcess.CPF: item[CustomerProcess.CPF],
                CustomerProcess.BIRTHDAY: item[CustomerProcess.BIRTHDAY],
                CustomerProcess.CUSTOMER_TYPE: item[CustomerProcess.CUSTOMER_TYPE],
                CustomerProcess.REGISTER_DATE: item[CustomerProcess.REGISTER_DATE],
                CustomerProcess.LAST_PRODUCT_BOUGHT: item[CustomerProcess.LAST_PRODUCT_BOUGHT],
                CustomerProcess.ACTIVE: item[CustomerProcess.ACTIVE]
            } for item in raw_customers_list
        ]
        customer_contact_info_list = CustomerProcess.intersect_columns_diff(raw_customers_list, customer_list, retain_keys=[CustomerProcess.ID])
        customer_contact_info_upper_list = CustomerProcess.upper_strings_of_list(customer_contact_info_list)

        self.__process_customer(customer_list, customer_contact_info_upper_list)
        self.__create_customer_by_list(customer_list)
        self.__create_customer_contact_info_by_list(customer_contact_info_upper_list)

    def get_birthday_of_the_day(self):
        """
        Gets customers that have birthday as current date
        
        Returns:
            List of Customers joined with CustomerContactInfo filtered the birthday for current date.
        """
        return self.customer_repo.get_customer_by_birthday()
