from data_loading.repositories.jit_repository import JitRepository
from data_loading.models.jit import Jit

class JitService:
    def __init__(self, jit_repository: JitRepository):
        self.jit_repo = jit_repository

    def create_jit(self, os_date, os_number, laboratory, customer_name, note, due_date, vendor, status, is_generated):
        jit = Jit(
            os_date=os_date,
            os_number=os_number,
            laboratory=laboratory,
            customer_name=customer_name,
            note=note, due_date=due_date,
            vendor=vendor, status=status,
            is_generated=is_generated
        )
        return self.jit_repo.create_jit(jit)
    
    def create_jit_if_it_not_exist(self, os_date, os_number, laboratory, customer_name, note, due_date, vendor, status, is_generated):
        jit = self.jit_repo.get_jit_by_os_number(os_number)
        if not jit:
            jit = Jit(
                os_date=os_date,
                os_number=os_number,
                laboratory=laboratory,
                customer_name=customer_name,
                note=note, due_date=due_date,
                vendor=vendor, status=status,
                is_generated=is_generated
            )
            return self.jit_repo.create_jit(jit)
        return jit
    
    def check_existance_of_jit_by_os_number(self, os_number):
        return self.jit_repo.check_existence(os_number)
    
    def get_all(self):
        return self.jit_repo.get_all_jits()
