from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"options": "-c client_encoding=utf8"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def init_db():
    Base.metadata.create_all(engine)
