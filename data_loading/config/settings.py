import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
DB_NAME = os.getenv('DB_NAME', None)
DB_USER = os.getenv('DB_USER', None)
DB_PASSWORD = quote_plus(os.environ.get('DB_PASSWORD', None))
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)

url_postgres = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DATABASE_URL = url_postgres if DB_HOST else 'sqlite:///your_database.db'
