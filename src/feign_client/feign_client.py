import requests
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Define response model (adjust fields based on actual API response)
class Response(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None

class DigisacFeignClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_auth_token(self, form: Dict[str, Any]) -> Optional[Response]:
        url = f"{self.base_url}/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=form, headers=headers)
        return self._parse_response(response)

    def add_or_update_contact(self, auth_token: str, message_body: str) -> Optional[Response]:
        url = f"{self.base_url}/contacts"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, data=message_body, headers=headers)
        return self._parse_response(response)

    def send_message(self, auth_token: str, message_body: str) -> None:
        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        requests.post(url, data=message_body, headers=headers)

    def _parse_response(self, response: requests.Response) -> Optional[Response]:
        if response.status_code == 200:
            return Response.model_validate(response.json())
        print(f"Error: {response.status_code}, {response.text}")
        return None


# Example Usage
if __name__ == "__main__":
    client = DigisacFeignClient("https://oticanany.digisac.chat/api/v1")

    # Example data for auth token
    form_data = {
        "grant_type": "password",
        "client_id": "api",
        "client_secret": "secret",
        "username": "carvalho_biel@outlook.com",
        "password": "Abc@1234",
        "scope": "*"
    }
    
    # Fetch token
    token_response = client.get_auth_token(form_data)
    if token_response:
        print("Auth Token Response:", token_response)

    # Use auth token for further requests
    #auth_token = "your_auth_token_here"
    #message_body = '{"example": "data"}'
    #client.add_or_update_contact(auth_token, message_body)
    #client.send_message(auth_token, message_body)

    #contacts_response = client.get_all_contacts(auth_token, per_page=10)
    #if contacts_response:
    #    print("Contacts Response:", contacts_response.json())
