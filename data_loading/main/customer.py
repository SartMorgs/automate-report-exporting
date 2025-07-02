import os
from pathlib import Path
from data_loading.config.database import session
from data_loading.services.customer_service import CustomerService
from data_loading.repositories.customer_repository import CustomerRepository
from typing import List


class CustomerMain:
    """
    Data Loading: Customer Main Class
    
    Used to feed the database with customer information.
    """
    def __init__(self):
        self.__USER_PATH = os.environ.get("STORE_PATH", None)
        self.__CSV_FOLDER_PATH = f"{self.__USER_PATH}\\otica-nany\\customer"
        self.__customer_repository = CustomerRepository(session)
        self.__customer_service = CustomerService(self.__customer_repository)

    def __get_list_of_customer_files_to_be_loaded(self) -> List[str]:
        """
        Gets all filenames related to customer information
        
        Returns:
            List[str]: List with all filenames of customer related information extracted by RPA
        """
        path = Path(self.__CSV_FOLDER_PATH)
        return [str(file) for file in path.rglob("*.csv") if file.is_file()]
    
    def __create_customers_by_file(self, customers_file: str) -> None:
        """
        Creates customer in the database by file.
        
        Args:
            customers_file (str): filename containing customer information
        """
        self.__customer_service.validate_and_save_customer_on_db(customers_file)

    def create_all_customers(self):
        """
        Creates all customers based on files of customer information created by RPA.
        It validates each customer coming from the RPA as valid or not and creates or updates
        the customer in the database.
        
        Note:
            Needs the RPA execution to have the customer files first.
        """
        customer_csv_files = self.__get_list_of_customer_files_to_be_loaded()
        for file in customer_csv_files:
            self.__create_customers_by_file(file)
