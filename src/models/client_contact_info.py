from sqlalchemy import Column, Integer, String, Date, Boolean
from src.models.base import Base

class Client_contact_info(Base):
    __tablename__ = 'client_contact_info'
    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String, unique=False, index=False)
    address = Column(String, unique=True, index=False)
    house_number = Column(Integer, unique=False, index=False)
    complement = Column(String, unique=False, index=False)
    neighborhood = Column(String, unique=False, index=False)
    city = Column(String, unique=False, index=False)
    state = Column(String, unique=False, index=False)
    country = Column(String, unique=False, index=False)
    phone_number = Column(String, unique=False, index=False)
    cellphone_number = Column(String, unique=False, index=False)
    email = Column(String, unique=False, index=False)
