from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from data_loading.models.base import Base

class CustomerContactInfo(Base):
    __tablename__ = "customer_contact_info"
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True, index=True)
    cep = Column(String, unique=False, index=False)
    address = Column(String, unique=False, index=False)
    house_number = Column(Integer, unique=False, index=False)
    complement = Column(String, unique=False, index=False)
    neighborhood = Column(String, unique=False, index=False)
    city = Column(String, unique=False, index=False)
    state = Column(String, unique=False, index=False)
    country = Column(String, unique=False, index=False)
    phone_number = Column(String, unique=False, index=False)
    cellphone_number = Column(String, unique=False, index=False)
    email = Column(String, unique=False, index=False)
    
    __table_args__ = (
        UniqueConstraint(
            'address',
            'house_number',
            'complement',
            'neighborhood',
            'city',
            'state',
            'country',
            'phone_number',
            'cellphone_number',
            'email',
            name='uq_full_address'
        ),
    )

    client = relationship("Customer")
