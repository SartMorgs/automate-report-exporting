from data_loading.services.jit_service import JitService
from data_loading.repositories.jit_repository import JitRepository


class DatabaseDataSource:
    def __init__(self, jit_repository: JitRepository):
        self.jit_service = JitService(jit_repository)

    def read_jit(self):
        jit_table = self.jit_service.get_all()
        
        return [[jit.os_date, jit.os_number, jit.laboratory, jit.customer_name, jit.note, jit.due_date, jit.vendor, jit.status, jit.is_generated] for jit in jit_table]
