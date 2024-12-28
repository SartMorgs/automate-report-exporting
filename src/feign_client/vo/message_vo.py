import os
from dotenv import load_dotenv

load_dotenv()
ACCOUNT_ID= os.environ.get('ACCOUNT_ID', None)
SERVICE_ID=os.environ.get('SERVICE_ID', None)


def message_body_vo():
    return {
        "text": "testeMensagem Automatizada em python",
        "type": "chat",
        "number": "48996195199",
        "subject": "Sem assunto",
        "accountId": ACCOUNT_ID,
        "serviceId": SERVICE_ID
    }