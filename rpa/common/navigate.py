import time
from rpa.common.const_html_identifier import HtmlTagIdentifiers as CommonHtmlId
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CommonPageNavigation:    
    def __init__(self, driver):
        self.driver = driver
        self.__MIN_WAIT_SECONDS = 20
        
    def click_button_by_id(self, button_id, time_sleep):
        time.sleep(time_sleep)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.ID, button_id))).click()
        
    def click_button_by_css_selector(self, button_css_selector, time_sleep):
        time.sleep(time_sleep)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))).click()
    
    def click_button_by_xpath(self, button_xpath, time_sleep):
        time.sleep(time_sleep)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        
    def __switch_to_frame(self, frame_id, time_sleep):
        time.sleep(time_sleep)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, frame_id))
        
    def navigate_to_report_board_selection(self):
        self.click_button_by_id(CommonHtmlId.LEFT_MENU_REPORT_BUTTON_ID, 10)
        self.click_button_by_css_selector(CommonHtmlId.LEFT_MENU_HIDDEN_ACCESS_BUTTON_ID, 10)
        self.__switch_to_frame(CommonHtmlId.MAIN_FRAME, 10)
        
    def navigate_to_customer_report_page(self):
        self.click_button_by_id(CommonHtmlId.LEFT_MENU_CRM_BUTTON_ID, 10)
        self.click_button_by_css_selector(CommonHtmlId.LEFT_MENU_HIDDEN_CRM_REPORT_BUTTON_ID, 2)
        self.click_button_by_xpath(CommonHtmlId.LEFT_MENU_HIDDEN_CRM_CUSTOMER_PROVIDER_BUTTON_XPATH, 2)
        self.__switch_to_frame(CommonHtmlId.MAIN_FRAME, 2)
    
    def return_page(self):
        self.driver.back()
        time.sleep(2)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, CommonHtmlId.MAIN_FRAME))
