from sqlalchemy.orm import Session
from sqlalchemy import func
from data_loading.models.customer import Customer
from data_loading.models.customer_contact_info import CustomerContactInfo

class CustomerRepository:
    """
    Repositories: Customer Repository Class
    
    Used for database connection: reading and writing into 'customer' and 'customer_contact_info' table
    
    Attributes:
        db (Session): Database session.
    """
    def __init__(self, db: Session):
        self.db = db

        self.__MM_DD_DATE_FORMAT = "MM-DD"

    def get_customer_by_id(self, customer_id: int):
        """
        Gets customer by specified id.
        
        Args:
            customer_id (int): Customer ID.
            
        Returns:
            Customer object
        """
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_customer_by_birthday(self):
        """
        Gets customers by birthday in the current date.
        
        Returns:
            List of Customers joined with CustomerContactInfo filtered the birthday for current date.
        """
        return self.db.query(Customer, CustomerContactInfo) \
            .join(CustomerContactInfo, Customer.id == CustomerContactInfo.id) \
            .filter(func.to_char(Customer.birthday, 'MM-DD') == func.to_char(
                func.current_date(), 'MM-DD'), Customer.active == 'true').all()

    def get_all(self):
        """
        Gets all data from customer table
        
        Returns:
            List of Customers from table
        """
        return self.db.query(Customer).first()

    def create_customer(self, customer: Customer):
        """
        Creates customer in the database.
        
        Args:
            customer (Customer): object to be created
            
        Returns:
            Customer object created
        """
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def create_customer_only_if_doesnt_exist(self, customer: Customer):
        """
        Creates customer if it doesn't exist in the database.
        
        Args:
            customer (Customer): object to be created
            
        Returns:
            Customer object created or the one that exists in the database
        """
        existing_customer = self.db.query(Customer).filter_by(id=customer.id).first()
        if not existing_customer:
            return self.create_customer(customer)
        return existing_customer        

    def create_customer_contact_info(self, customer_contact_info: CustomerContactInfo):
        """
        Creates customer contact info
        
        Args:
            customer_contact_info (CustomerContactInfo): object to be created
            
        Returns:
            CustomerContactInfo object created
        """
        self.db.add(customer_contact_info)
        self.db.commit()
        self.db.refresh(customer_contact_info)
        return customer_contact_info
    
    def create_customer_contact_info_only_if_it_doesnt_exist(self, customer_contact_info: CustomerContactInfo):
        """
        Creates customer contact info if it doesn't exists in the database
        
        Args:
            customer_contact_info (CustomerContactInfo): object to be created
        
        Returns:
            CustomerContactInfo object created or the one that exists in the database
        """
        existing_customer_contact_info =self.db.query(CustomerContactInfo).filter_by(id=customer_contact_info.id).first()
        if not existing_customer_contact_info:
            return self.create_customer_contact_info(customer_contact_info)
        return existing_customer_contact_info
