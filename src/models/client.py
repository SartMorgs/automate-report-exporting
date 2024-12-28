from sqlalchemy import Column, Integer, String, Date, Boolean
from src.models.base import Base


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    fantasy_name = Column(String, unique=False, index=False)
    cpf = Column(String, unique=False, index=False)
    birthday = Column(Date, unique=False, index=False)
    client_type = Column(String, unique=False, index=False)
    register_date = Column(Date, unique=False, index=False)
    last_product_bought = Column(String, unique=False, index=False)
    active = Column(Boolean, unique=False, index=True)
