import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from rpa.common.const_html_identifier import HtmlTagIdentifiers


class ErpLogin:
    def __init__(self, driver):
        load_dotenv()
        self.URL = os.environ.get('URL')
        self.USERNAME = os.environ.get('W_USERNAME')
        self.PASSWORD = os.environ.get('W_PASSWORD')
        
        self.driver = driver
    
    def erp_login(self):
        # Open the web application
        self.driver.get(self.URL)
        
        # Log in
        username = self.driver.find_element(By.ID, HtmlTagIdentifiers.USERNAME_FORM)
        password = self.driver.find_element(By.ID, HtmlTagIdentifiers.PASSWORD_FORM)

        username.send_keys(self.USERNAME)
        password.send_keys(self.PASSWORD)
        password.submit()
