from src.repositories.client_repository import ClientRepository
from src.models.client import Client

class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.client_repo = client_repository

    def create_client(self, id, name, fantasy_name, cpf, birthday, client_type, register_date, last_product_bought, active):
        client = Client(
            id=id,
            name=name,
            fantasy_name=fantasy_name,
            cpf=cpf,
            birthday=birthday,
            client_type=client_type,
            register_date=register_date, 
            last_product_bought=last_product_bought,
            active=active
        )
        return self.client_repo.create_client(client)
    
    def create_client_if_it_not_exist(self, id, name, fantasy_name, cpf, birthday, client_type, register_date, last_product_bought, active):
        client = self.client_repo.get_client_by_id(id)
        if not client:
            client = Client(
            id=id,
            name=name,
            fantasy_name=fantasy_name,
            cpf=cpf,
            birthday=birthday,
            client_type=client_type,
            register_date=register_date, 
            last_product_bought=last_product_bought,
            active=active
            )
            return self.client_repo.create_client(client)
        return client
    
    def get_birthdays_of_the_day(self):
        return self.client_repo.get_client_by_birthday()
