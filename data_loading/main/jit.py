from data_loading.repositories.jit_repository import JitRepository
from data_loading.services.jit_service import JitService
from data_loading.config.database import session
from rpa.common.move_file import MoveFile


class JitMain:
    """
    Data Loading: Jit Main Class
    
    Used to feed the database with Jit information.
    """
    def __init__(self):
        self.jit_repository = JitRepository(session)
        self.jit_service = JitService(self.jit_repository)
        
        self.domain = 'otica-nany'
        self.report_name = 'os'

        self.move_file = MoveFile(self.domain, self.report_name, 'os')
            
    def create_jit(self):
        """
        Create all Jits based on OS file extracted from RPA marked as is_generated=False in the database
        
        Note:
            Needs the RPA execution to have the OS files first
        """
        self.jit_service.create_jit(self.move_file.SOURCE_REPORT_EXTRACTION_PATH)

    def update_is_generated(self):
        """
        Updates all Jits that have is_generated=False to is_generated=True
        """
        not_generated_jit = self.jit_service.get_all_not_generated_jit()
        self.jit_service.update_to_is_generated(not_generated_jit)
