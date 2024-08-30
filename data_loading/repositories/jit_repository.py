from sqlalchemy import text
from sqlalchemy.orm import Session
from data_loading.models.jit import Jit

class JitRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_jit_by_os_number(self, jit_os_number: int):
        return self.db.query(Jit).filter(Jit.os_number == jit_os_number).first()
    
    def check_existence(self, os_number):
        query = f"SELECT EXISTS(SELECT 1 FROM {Jit.__tablename__} WHERE os_number = {os_number} and is_generated = true)"
        return self.db.execute(text(query)).scalar()

    def create_jit(self, jit: Jit):
        self.db.add(jit)
        self.db.commit()
        self.db.refresh(jit)
        return jit
    
    def create_jit_only_if_doesnt_exist(self, jit: Jit):
        existing_jit = self.db.query(Jit).filter_by(os_number=jit.os_number).first()
        if not existing_jit:
            return self.create_jit(jit)
        return existing_jit
    
    def update_to_is_generated(self, jit_os_number: int):
        jit = self.get_jit_by_os_number(jit_os_number)
        jit.is_generated = True
        self.db.commit()
        return jit
    
    def get_all_jits(self):
        return self.db.query(Jit).all()

    def delete_all_jits(self):
        stm = f"DELETE FROM {Jit.__tablename__}"
        self.db.execute(text(stm))
        self.db.commit()
