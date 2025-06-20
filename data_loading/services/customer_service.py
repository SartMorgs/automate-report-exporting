import csv
from data_loading.repositories.customer_repository import CustomerRepository
from data_processing.customer import Customer as CustomerProcess
from data_loading.models.customer import Customer
from data_loading.models.customer_contact_info import CustomerContactInfo

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repo = customer_repository

    def __get_customer_list(self, customers_file):
        filtered_data = []
        with open(customers_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', fieldnames=CustomerProcess.get_customer_csv_column_names())

            for row in reader:
                row["active"] = True
                if CustomerProcess.validate_csv_cpf(row["cpf"], False):
                    row["active"] = False
                filtered_data.append(row)
 
        return filtered_data[1:]

    def __process_customer(self, customer_list, customer_contact_info_list):
        CustomerProcess.process_csv_date_field(customer_list, "birthday")
        CustomerProcess.process_csv_date_field(customer_list, "register_date")
        CustomerProcess.process_csv_int_field(customer_contact_info_list, "house_number")
    
    def __create_customer_by_list(self, customer_list):
        for entry in customer_list:
            customer = Customer(
                id = entry["id"],
                name = entry["name"],
                fantasy_name = entry["fantasy_name"],
                cpf = entry["cpf"],
                birthday = entry["birthday"],
                customer_type = entry["customer_type"],
                register_date = entry["register_date"],
                last_product_bought = entry["last_product_bought"],
                active = entry["active"]
            )
            self.customer_repo.create_customer_only_if_doesnt_exist(customer)
    
    def __create_customer_contact_info_by_list(self, customer_contact_info_list):
        for entry in customer_contact_info_list:
            customer_contact_info = CustomerContactInfo(
                id = entry["id"],
                cep = entry["cep"],
                address = entry["address"],
                house_number = entry["house_number"],
                complement = entry["complement"],
                neighborhood = entry["neighborhood"],
                city = entry["city"],
                state = entry["state"],
                country = entry["country"],
                phone_number = entry["phone_number"],
                cellphone_number = entry["cellphone_number"],
                email = entry["email"]
            )
            self.customer_repo.create_customer_contact_info_only_if_it_doesnt_exist(customer_contact_info)

    def validate_and_save_customer_on_db(self, customers_file):
        raw_customers_list = self.__get_customer_list(customers_file)

        customer_list = [
            {
                "id": item["id"],
                "name": item["name"],
                "fantasy_name": item["fantasy_name"],
                "cpf": item["cpf"],
                "birthday": item["birthday"],
                "customer_type": item["customer_type"],
                "register_date": item["register_date"],
                "last_product_bought": item["last_product_bought"],
                "active": item["active"]
            } for item in raw_customers_list
        ]
        customer_contact_info_list = CustomerProcess.intersect_columns_diff(raw_customers_list, customer_list, retain_keys=["id"])
        customer_contact_info_upper_list = CustomerProcess.upper_strings_of_list(customer_contact_info_list)

        self.__process_customer(customer_list, customer_contact_info_upper_list)
        self.__create_customer_by_list(customer_list)
        self.__create_customer_contact_info_by_list(customer_contact_info_upper_list)

    def get_birthday_of_the_day(self):
        return self.customer_repo.get_customer_by_birthday()

