from sqlalchemy import Column, Integer, String, Date, Boolean, MetaData
from data_loading.models.base import Base

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    fantasy_name = Column(String, unique=False, index=False)
    cpf = Column(String, unique=False, index=False)
    birthday = Column(Date, unique=False, index=False)
    customer_type = Column(String, unique=False, index=False)
    register_date = Column(Date, unique=False, index=False)
    last_product_bought = Column(String, unique=False, index=False)
    active = Column(Boolean, unique=False, index=True)
