import requests
import os
from typing import Optional, Dict, Any
from pydantic import BaseModel
import json
from vo.message_vo import message_body_vo
from vo.auth_vo import get_digisac_credentials
from dotenv import load_dotenv

load_dotenv()

class Response(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None


def _parse_response(response: requests.Response) -> Optional[Response]:
    if response.status_code == 200:
        return response.json()
    return None

class DigisacFeignClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_auth_token(self, form: Dict[str, Any]) -> Optional[Response]:
        url = f"{self.base_url}/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=form, headers=headers)
        token_response =  _parse_response(response)
        return token_response["access_token"]
    
    def add_or_update_contact(self, auth_token: str, message_body: str) -> Optional[Response]:
        url = f"{self.base_url}/contacts"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, data=message_body, headers=headers)
        return _parse_response(response)
    
    def send_message(self, auth_token: str, message_body: str) -> None:
        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        requests.post(url, data=message_body, headers=headers)


def set_encoder(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError("Object of type set is not JSON serializable")

# Example Usage
if __name__ == "__main__":
    client = DigisacFeignClient(os.environ.get('DIGISAC_URL', None))
    auth_token = client.get_auth_token(get_digisac_credentials())

    with open(os.environ.get('ANNIVERSARY_IMG_SRC', None), 'r') as file:
        file_contents = file.read() 

    message_body = message_body_vo()
    jsonBody = json.dumps(message_body)

    client.send_message(auth_token, jsonBody)
