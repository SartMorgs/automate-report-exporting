import csv
import os
from src.common.csv_utils import CsvUtils
from dotenv import load_dotenv

load_dotenv()

def get_clients_list(validation):
    filtered_data = []
    with open(os.environ.get('CSV_FILE_SRC', None), mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', fieldnames=CsvUtils.get_client_csv_column_names())
        
        for row in reader:
            if CsvUtils.validate_csv_cpf(row["cpf"], validation):
                filtered_data.append(row)
                row['active'] = validation

    if not validation:
        filtered_data.pop(0)

    return filtered_data

def process_clients(client_list, client_contact_info_list):
    CsvUtils.process_csv_date_field(client_list, "birthday")
    CsvUtils.process_csv_date_field(client_list, "register_date")
    CsvUtils.process_csv_int_field(client_contact_info_list, "house_number")

def validate_and_save_clients_on_db(valid_clients):
    raw_clients_list = get_clients_list(valid_clients)

    client_list = [{"id": item["id"], "name": item["name"], "fantasy_name": item["fantasy_name"], "cpf": item["cpf"], "birthday": item["birthday"], "client_type": item["client_type"], "register_date": item["register_date"], "last_product_bought": item["last_product_bought"], "active": item["active"]} for item in raw_clients_list]
    client_contact_info_list = CsvUtils.intersect_columns_diff(raw_clients_list, client_list, retain_keys=["id"])

    process_clients(client_list, client_contact_info_list)

    print(client_list[0])
    print(client_contact_info_list[0])

# Example usage
validate_and_save_clients_on_db(valid_clients=True)
validate_and_save_clients_on_db(valid_clients=False)