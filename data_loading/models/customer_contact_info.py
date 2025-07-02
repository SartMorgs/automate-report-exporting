from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from data_loading.models.base import Base
from typing import Optional

class CustomerContactInfo(Base):
    """
    Models: Stores contact information for a customer
    including address, phone numbers, and email.

    This model enforces a unique constraint on the combination of
    address-related fields and contact details to avoid duplicates.
    
    Attributes:
        id (int): Primary key identifier for the customer contact info.
        cep (Optional[str]): CEP code.
        address (Optional[str]): Address line.
        house_number (Optional[int]): House number.
        complement (Optional[str]): Complement of address, usually apt number.
        neighborhood (Optional[str]): Neighborhood name.
        city (Optional[str]): City name.
        state (Optional[str]): State name.
        country (Optional[str]): Country name.
        phone_number (Optional[str]): Phone number.
        cellphone_number (Optional[str]): Celphone number.
        email (Optional[str]): Personal email.
    """
    __tablename__ = "customer_contact_info"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('customer.id'), primary_key=True, index=True)
    cep: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    address: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    house_number: Mapped[Optional[int]] = mapped_column(Integer, unique=False, index=False)
    complement: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    neighborhood: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    city: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    state: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    country: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    cellphone_number: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    email: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)

    # Unique constraint combining multiple fields
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

    # Relationship to Customer
    client = relationship("Customer")
