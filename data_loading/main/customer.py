import os
from pathlib import Path
from data_loading.config.database import session
from data_loading.services.customer_service import CustomerService
from data_loading.repositories.customer_repository import CustomerRepository


class CustomerMain:
    def __init__(self):
        self.__USER_PATH = os.environ.get("STORE_PATH", None)
        self.__CSV_FOLDER_PATH = f"{self.__USER_PATH}\\otica-nany\\customer"
        self.__customer_repository = CustomerRepository(session)
        self.__customer_service = CustomerService(self.__customer_repository)

    def __get_list_of_customer_files_to_be_loaded(self):
        path = Path(self.__CSV_FOLDER_PATH)
        return [str(file) for file in path.rglob("*.csv") if file.is_file()]
    
    def __create_customers_by_file(self, customers_file):
        self.__customer_service.validate_and_save_customer_on_db(customers_file)

    def create_all_customers(self):
        customer_csv_files = self.__get_list_of_customer_files_to_be_loaded()
        for file in customer_csv_files:
            self.__create_customers_by_file(file)
