import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from rpa.data_extraction.os.const_html_identifier import OsHtmlTagIdentifiers as HtmlTagId
from rpa.common.navigate import CommonPageNavigation
from rpa.common.const_html_identifier import HtmlTagIdentifiers as CommonHtmlId
from rpa.login.erp_login import ErpLogin


class OsReportData:
    def __init__(self, start_date, end_date):
        self.__MIN_WAIT_SECONDS = 20
        
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        
        self.start_date_filter = start_date
        self.end_date_filter = end_date
        
        self.erp_login = ErpLogin(self.driver)
        self.navigate = CommonPageNavigation(self.driver)
    
    def access_os_report_menu_page(self):
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.presence_of_element_located((By.XPATH, HtmlTagId.OS_REPORT_BOX_XPATH))).click()
        
    def __access_jit_report_filter_page(self):
        self.access_os_report_menu_page()
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.presence_of_element_located((By.XPATH, HtmlTagId.ACCESS_OS_REPORT_BUTTON_XPATH))).click()
        time.sleep(3)
        
    def build_arguments_value_script(self, value):
        return f"arguments[0].value = '{value}';"

    def __filter_by_date(self):
        start_date = self.driver.find_element(By.ID, HtmlTagId.START_DATE_FORM_ID)
        end_date = self.driver.find_element(By.ID, HtmlTagId.END_DATE_FORM_ID)
        time.sleep(5)
        self.driver.find_element(By.ID, HtmlTagId.START_DATE_FORM_ID).click()
        self.driver.execute_script(self.build_arguments_value_script(self.start_date_filter), start_date)
        self.driver.find_element(By.ID, HtmlTagId.END_DATE_FORM_ID).click()
        self.driver.execute_script(self.build_arguments_value_script(self.end_date_filter), end_date)
        time.sleep(5)
        self.driver.find_element(By.XPATH, CommonHtmlId.FILTER_BUTTON_XPATH).click()

    def __export_csv_data(self):
        self.navigate.click_button_by_xpath(HtmlTagId.DROP_DOWN_EXPORT_MENU_BUTTON_XPATH, 0)
        self.driver.find_element(By.XPATH, CommonHtmlId.CSV_EXPORT_BUTTON_ID).click()
        time.sleep(10)
        
    def generate_jit_report(self):    
        self.erp_login.erp_login()
        self.navigate.navigate_to_report_board_selection()

        self.__access_jit_report_filter_page()
        self.__filter_by_date()
        self.__export_csv_data()

        self.driver.quit()
