from datetime import datetime
from sqlalchemy.orm import Session
from src.models.client import Client
from src.models.client_contact_info import Client_contact_info

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_client_by_id(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def get_client_by_birthday(self):
        return self.db.query(Client).join(Client_contact_info, Client.id == Client_contact_info.id).filter(Client.birthday == datetime.now().strftime('%Y-%m-%d')).all()

    def get_all(self):
        return self.db.query(Client).first()
    
    def create_client(self, client: Client):
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client
