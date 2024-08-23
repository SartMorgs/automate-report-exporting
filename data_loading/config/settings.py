import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ.get('DB_NAME', None)
DB_USER = os.environ.get('DB_USER', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
DB_HOST = os.environ.get('DB_HOST', None)
DB_PORT = os.environ.get('DB_PORT', None)

url_postgres = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DATABASE_URL = url_postgres if DB_HOST else 'sqlite:///your_database.db'
