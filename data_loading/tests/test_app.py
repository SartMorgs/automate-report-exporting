import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.jit import Jit, Base
from repositories.jit_repository import JitRepository

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up in-memory SQLite engine and create tables"""
        cls.test_engine = create_engine('sqlite:///:memory:')  # In-memory SQLite database
        cls.SessionLocal = sessionmaker(bind=cls.test_engine)
        Base.metadata.create_all(bind=cls.test_engine)  # Create the database schema

    def setUp(self):
        """Start a new session for each test"""
        self.session = self.SessionLocal()
        self.jit_repository = JitRepository(self.session)

    def tearDown(self):
        """Close the session and rollback changes"""
        self.session.rollback()
        self.session.close()
    
    @classmethod
    def tearDownClass(cls):
        """Drop all tables and dispose of the engine"""
        Base.metadata.drop_all(bind=cls.test_engine)
        cls.test_engine.dispose()
        
    def test_create_jit(self):
        jit = Jit(
            os_date=datetime.strptime('2024-08-15', "%Y-%m-%d").date(),
            os_number=123,
            laboratory='REPRO',
            customer_name='customer1',
            note='note1',
            due_date=datetime.strptime('2024-08-16', "%Y-%m-%d").date(),
            vendor='vendor1',
            status='done',
            is_generated=False
        )
        self.jit_repository.create_jit(jit)
        queried_jit = self.session.query(Jit).filter_by(os_number=jit.os_number).first()
        self.assertEqual(queried_jit.os_number, jit.os_number)
        self.assertEqual(queried_jit.customer_name, jit.customer_name)
        self.assertFalse(queried_jit.is_generated)
    
    def test_create_jit_when_it_doesnt_exist(self):
        jit = Jit(
            os_date=datetime.strptime('2024-08-15', "%Y-%m-%d").date(),
            os_number=134,
            laboratory='REPRO',
            customer_name='customer1',
            note='note1',
            due_date=datetime.strptime('2024-08-16', "%Y-%m-%d").date(),
            vendor='vendor1',
            status='done',
            is_generated=False
        )
        self.jit_repository.create_jit_only_if_doesnt_exist(jit)
        queried_jit = self.session.query(Jit).filter_by(os_number=jit.os_number).first()
        self.assertEqual(queried_jit.os_number, jit.os_number)
        self.assertEqual(queried_jit.customer_name, jit.customer_name)
        self.assertFalse(queried_jit.is_generated)
    
    def test_update_to_is_generated(self):
        jit = Jit(
            os_date=datetime.strptime('2024-08-15', "%Y-%m-%d").date(),
            os_number=124,
            laboratory='REPRO',
            customer_name='customer1',
            note='note1',
            due_date=datetime.strptime('2024-08-16', "%Y-%m-%d").date(),
            vendor='vendor1',
            status='done',
            is_generated=False
        )
        self.jit_repository.create_jit(jit)
        queried_jit = self.session.query(Jit).filter_by(os_number=jit.os_number).first()
        self.jit_repository.update_to_is_generated(queried_jit.id)
        self.assertEqual(queried_jit.os_number, jit.os_number)
        self.assertEqual(queried_jit.is_generated, jit.is_generated)

if __name__ == "__main__":
    unittest.main()
