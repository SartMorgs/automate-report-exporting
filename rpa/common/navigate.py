import time
from rpa.common.const_html_identifier import HtmlTagIdentifiers as CommonHtmlId
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CommonPageNavigation:    
    def __init__(self, driver):
        self.driver = driver
        self.__MIN_WAIT_SECONDS = 20
        
    def navigate_to_report_board_selection(self):
        time.sleep(10)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.ID, CommonHtmlId.LEFT_MENU_REPORT_BUTTON_ID))).click()
        time.sleep(10)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CommonHtmlId.LEFT_MENU_HIDDEN_ACCESS_BUTTON_ID))).click()
        time.sleep(10)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, CommonHtmlId.MAIN_FRAME))
        
    def navigate_to_customer_report_page(self):
        time.sleep(10)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.ID, CommonHtmlId.LEFT_MENU_CRM_BUTTON_ID))).click()
        time.sleep(2)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CommonHtmlId.LEFT_MENU_HIDDEN_CRM_REPORT_BUTTON_ID))).click()
        time.sleep(2)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.XPATH, CommonHtmlId.LEFT_MENU_HIDDEN_CRM_CUSTOMER_PROVIDER_BUTTON_XPATH))).click()
        time.sleep(2)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, CommonHtmlId.MAIN_FRAME))
    
    def return_page(self):
        self.driver.back()
        time.sleep(2)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, CommonHtmlId.MAIN_FRAME))
