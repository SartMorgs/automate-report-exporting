from sqlalchemy import Column, Integer, String, Date, Boolean
from data_loading.models.base import Base

class Jit(Base):
    __tablename__ = 'jit'
    id = Column(Integer, primary_key=True, index=True)
    os_date = Column(Date, unique=False, index=False)
    os_number = Column(Integer, unique=True, index=True)
    laboratory = Column(String, unique=False, index=False)
    customer_name = Column(String, unique=False, index=False)
    note = Column(String, unique=False, index=False)
    due_date = Column(Date, unique=False, index=False)
    vendor = Column(String, unique=False, index=False)
    status = Column(String, unique=False, index=True)
    is_generated = Column(Boolean, unique=False, index=False)
