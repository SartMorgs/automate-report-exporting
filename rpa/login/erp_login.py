import os
import time
from dotenv import load_dotenv
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By
from rpa.common.const_html_identifier import HtmlTagIdentifiers
from selenium.webdriver.common.keys import Keys


class ErpLogin:
    def __init__(self, driver):
        load_dotenv()
        self.URL = os.getenv('URL', None)
        self.USERNAME = os.getenv('W_USERNAME', None)
        self.PASSWORD = os.getenv('W_PASSWORD', None)

        self.driver = driver
    
    def erp_login(self):
        # Open the web application
        self.driver.get(self.URL)
        
        # Log in
        time.sleep(5)
        username = self.driver.find_element(By.ID, HtmlTagIdentifiers.USERNAME_FORM)
        password = self.driver.find_element(By.ID, HtmlTagIdentifiers.PASSWORD_FORM)

        username.send_keys(self.USERNAME)
        password.send_keys(self.PASSWORD)
        password.send_keys(Keys.ENTER)