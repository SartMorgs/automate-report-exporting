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
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.ID, CommonHtmlId.LEFT_MENU_REPORT_BUTTON_ID))).click()
        time.sleep(3)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CommonHtmlId.LEFT_MENU_HIDDEN_ACCESS_BUTTON_ID))).click()
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element(By.ID, CommonHtmlId.MAIN_FRAME))
