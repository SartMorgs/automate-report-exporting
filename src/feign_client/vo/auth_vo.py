import os
from dotenv import load_dotenv

load_dotenv()
DIGISAC_USERNAME= os.environ.get('DIGISAC_USERNAME', None)
DIGISAC_PASSWORD=os.environ.get('DIGISAC_PASSWORD', None)


def get_digisac_credentials():
    return {
        "grant_type": "password",
        "client_id": "api",
        "client_secret": "secret",
        "username": DIGISAC_USERNAME,
        "password": DIGISAC_PASSWORD,
        "scope": "*"
    }