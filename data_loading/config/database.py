from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_loading.models.base import Base
from data_loading.config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def init_db() -> None:
    Base.metadata.create_all(engine)
