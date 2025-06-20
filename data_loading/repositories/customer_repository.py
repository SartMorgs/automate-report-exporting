from sqlalchemy.orm import Session
from sqlalchemy import func
from data_loading.models.customer import Customer
from data_loading.models.customer_contact_info import CustomerContactInfo

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_customer_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_customer_by_birthday(self):
        return self.db.query(Customer, CustomerContactInfo) \
            .join(CustomerContactInfo, Customer.id == CustomerContactInfo.id) \
            .filter(func.to_char(Customer.birthday, 'MM-DD') == func.to_char(
                func.current_date(), 'MM-DD'), Customer.active == 'true').all()

    def get_all(self):
        return self.db.query(Customer).first()

    def create_customer(self, customer: Customer):
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def create_customer_only_if_doesnt_exist(self, customer: Customer):
        existing_customer = self.db.query(Customer).filter_by(id=customer.id).first()
        if not existing_customer:
            return self.create_customer(customer)
        return existing_customer        

    def create_customer_contact_info(self, customer_contact_info: CustomerContactInfo):
        self.db.add(customer_contact_info)
        self.db.commit()
        self.db.refresh(customer_contact_info)
        return customer_contact_info
    
    def create_customer_contact_info_only_if_it_doesnt_exist(self, customer_contact_info: CustomerContactInfo):
        existing_customer_contact_info =self.db.query(CustomerContactInfo).filter_by(id=customer_contact_info.id).first()
        if not existing_customer_contact_info:
            return self.create_customer_contact_info(customer_contact_info)
        return existing_customer_contact_info
