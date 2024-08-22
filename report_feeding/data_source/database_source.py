import psycopg2
import sqlite3
from data_loading.services.jit_service import JitService


class DatabaseDataSource:
    def __init__(self):
        self.jit_service = JitService()

    def read_table(self, table_name):
        return self.jit_service.get_all()
