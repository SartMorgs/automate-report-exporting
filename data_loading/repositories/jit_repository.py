from sqlalchemy.orm import Session
from data_loading.models.jit import Jit

class JitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_jit_by_id(self, jit_id: int):
        return self.db.query(Jit).filter(Jit.id == jit_id).first()

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
    
    def update_to_is_generated(self, jit_id: int):
        jit = self.get_jit_by_id(jit_id)
        jit.is_generated = True
        self.db.commit()
        return jit
