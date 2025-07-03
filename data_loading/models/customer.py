from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, Boolean
from data_loading.models.base import Base
from typing import Optional

class Customer(Base):
    """
    Models: Represents a customer record in the system.

    Attributes:
        id (int):
            Primary key identifier for the customer.
        name (Optional[str]): The customer's full name.
        fantasy_name (Optional[str]): An alternative or trade name (commonly used by businesses).
        cpf (Optional[str]): The customer's CPF (Cadastro de Pessoas Físicas) tax ID number.
        birthday (Optional[date]): The customer's date of birth.
        customer_type (Optional[str]): The type of customer (e.g., individual, company).
        register_date (Optional[date]): The date when the customer was registered in the system.
        last_product_bought (Optional[str]): A description or name of the last product the customer purchased.
        active (Optional[bool]): Indicates whether the customer is currently active.
    """
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    fantasy_name: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    cpf: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    birthday: Mapped[Optional[Date]] = mapped_column(Date, unique=False, index=False)
    customer_type: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    register_date: Mapped[Optional[Date]] = mapped_column(Date, unique=False, index=False)
    last_product_bought: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, unique=False, index=True)
