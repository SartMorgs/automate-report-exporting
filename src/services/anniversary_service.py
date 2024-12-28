from src.repositories.client_repository import ClientRepository
from src.config.database import session

class AnniversaryService:

    def __init__(self):
        self.client_repository = ClientRepository(session)

    def send_anniversary(self):
        clients = ClientRepository.get_all(self.client_repository)
        print(clients)

if __name__ == "__main__":
    anniversary_service = AnniversaryService()
    anniversary_service.send_anniversary()