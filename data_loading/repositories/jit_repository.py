from sqlalchemy import text
from sqlalchemy.orm import Session
from data_loading.models.jit import Jit

class JitRepository:
    """
    Repositories: Jit Repository Class
    
    Used for database connection:  reading and writing into 'jit' table.
    
    Attributes:
        db (Session): Database session.
    """
    def __init__(self, db: Session):
        self.db = db
    
    def get_jit_by_os_number(self, jit_os_number: int):
        """
        Gets Jit by OS number.
        
        Args:
            jit_os_number (int): Jit OS number
            
        Returns:
            Jit object.
        """
        return self.db.query(Jit).filter(Jit.os_number == jit_os_number).first()
    
    def check_existence(self, os_number: int):
        """
        Check if Jit is already in the database based into OS number.
        
        Args:
            os_number (int): Jit OS number
        
        Returns:
            Row in the database case it exists and 'None' if it doesn't.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {Jit.__tablename__} WHERE os_number = {os_number} and is_generated = true)"
        return self.db.execute(text(query)).scalar()

    def create_jit(self, jit: Jit):
        """
        Create Jit based on Jit object.
        
        Args:
            jit (Jit): Jit object.
        
        Returns:
            Jit object.
        """
        self.db.add(jit)
        self.db.commit()
        self.db.refresh(jit)
        return jit
    
    def create_jit_only_if_doesnt_exist(self, jit: Jit):
        """
        Create jit if it doesn't exist in the database.
        
        Args:
            jit (Jit): Jit object.
            
        Returns:
            Jit object created or the Jit already existent in the database.
        """
        existing_jit = self.db.query(Jit).filter_by(os_number=jit.os_number).first()
        if not existing_jit:
            return self.create_jit(jit)
        return existing_jit
    
    def update_to_is_generated(self, jit_os_number: int):
        """
        Update Jit 'is_generated' column to True.
        
        Args:
            jit_os_number (int): Jit OS number.
        
        Returns:
            Jit object.
        """
        jit = self.get_jit_by_os_number(jit_os_number)
        jit.is_generated = True
        self.db.commit()
        return jit
    
    def get_all_jits(self):
        """
        Gets all Jits from database.
        
        Returns:
            List of Jit object.
        """
        return self.db.query(Jit).all()
    
    def get_all_not_generated_jit(self):
        """
        Gets all Jits with 'is_generated' column as False.
        
        Returns:
            Query in the Jit table.
        """
        return self.db.query(Jit).filter_by(is_generated=False)

    def delete_all_jits(self):
        """
        Deletes all Jits in the database.
        """
        stm = f"DELETE FROM {Jit.__tablename__}"
        self.db.execute(text(stm))
        self.db.commit()
