from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, Boolean
from data_loading.models.base import Base
from typing import Optional

class Jit(Base):
    """
    Models: Represents a Jit order record containing details about
    work orders, scheduling, and status tracking.

    Attributes:
        id (int): Unique identifier for the JIT record.
        os_date (Optional[Date]): Date the order/service was created.
        os_number (Optional[int]): Unique number identifying the order/service.
        laboratory (Optional[str]): Name of the laboratory handling the order.
        customer_name (Optional[str]): Name of the customer associated with the order.
        note (Optional[str]): Additional notes or remarks.
        due_date (Optional[Date]): Due date for completing the order.
        vendor (Optional[str]): Vendor responsible for the order.
        status (Optional[str]): Current status of the order.
        is_generated (Optional[bool]): Indicates whether the record was auto-generated.
    """
    __tablename__ = 'jit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    os_date: Mapped[Optional[Date]] = mapped_column(Date, unique=False, index=False)
    os_number: Mapped[Optional[int]] = mapped_column(Integer, unique=True, index=True)
    laboratory: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    note: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    due_date: Mapped[Optional[Date]] = mapped_column(Date, unique=False, index=False)
    vendor: Mapped[Optional[str]] = mapped_column(String, unique=False, index=False)
    status: Mapped[Optional[str]] = mapped_column(String, unique=False, index=True)
    is_generated: Mapped[Optional[bool]] = mapped_column(Boolean, unique=False, index=False)
