import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from rpa.login.erp_login import ErpLogin
from rpa.common.navigate import CommonPageNavigation
from rpa.data_extraction.customers.const_html_identifier import CustomerProviderHtmlTagIdentifiers as HtmlTagId
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class CustomerReportData:
    def __init__(self, final_code):
        self.__MIN_WAIT_SECONDS = 20

        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        
        self.__FINAL_CODE = final_code

        self.__CUSTOMER_PROVIDER_REPORT_DEFAULT_NAME = "Relatório clientesfornecedores  Microvix-erp.csv"
        self.__CUSTOMER_PROVIDER_REPORT_NEW_NAME = "customer_provider"
    
    def __set_column_xpath(self, number):
        return f"//*[@id='exibir_campos']/option[{number}]"
    
    # REPETIDO
    def build_arguments_value_script(self, value):
        return f"arguments[0].value = '{value}';"
    
    def __fill_forms(self, start_code, end_code):
        start_code_form = self.driver.find_element(By.XPATH, HtmlTagId.START_CODE_XPATH)
        self.driver.execute_script(self.build_arguments_value_script(start_code), start_code_form)
        end_code_form = self.driver.find_element(By.XPATH, HtmlTagId.END_CODE_XPATH)
        self.driver.execute_script(self.build_arguments_value_script(end_code), end_code_form)
    
    def __select_checkboxes(self, select_boxes):
        if not select_boxes:
            self.driver.find_element(By.ID, HtmlTagId.LIST_IN_COLUMNS_CHECK_ID).click()
            time.sleep(1)
            self.driver.find_element(By.ID, HtmlTagId.LIST_IN_COLUMNS_CHECK_ID).click()
            time.sleep(1)
            return
        self.driver.find_element(By.ID, HtmlTagId.CUSTOMER_TYPE_CHECK_ID).click()
        time.sleep(1)
        self.driver.find_element(By.ID, HtmlTagId.CUSTOMER_AND_PROVIDER_TYPE_CHECK_ID).click()
        time.sleep(1)
        self.driver.find_element(By.ID, HtmlTagId.DISABLED_CUSTOMERS_CHECK_ID).click()
        time.sleep(1)
        self.driver.find_element(By.ID, HtmlTagId.LIST_IN_COLUMNS_CHECK_ID).click()
        time.sleep(1)
    
    def __select_columns(self):
        for i in range(1, 16):
            self.driver.find_element(By.XPATH, self.__set_column_xpath(i)).click()
    
    def __filter_customers(self, start_code, end_code, select_boxes):
        self.__fill_forms(start_code, end_code)
        self.__select_checkboxes(select_boxes)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.ID, HtmlTagId.SHOW_FIELDS_BOX_ID)))
        self.__select_columns() if select_boxes else None

    def __generate_csv(self, start_code, end_code, select_boxes):
        self.__filter_customers(start_code, end_code, select_boxes)
        self.driver.find_element(By.XPATH, HtmlTagId.CUSTOMER_GENERATE_REPORT_XPATH).click()
        time.sleep(2)
        WebDriverWait(self.driver, self.__MIN_WAIT_SECONDS).until(EC.element_to_be_clickable((By.XPATH, HtmlTagId.GENERATE_CSV_FILE_BUTTON_XPATH))).click()
        time.sleep(20)
        
    def __rename_file(self, old_filename, new_filename):
        user_path = os.path.expanduser('~')
        full_old_filename = f'{user_path}\\Downloads\\{old_filename}'
        full_new_filename = f'{user_path}\\Downloads\\{new_filename}'
        os.rename(full_old_filename, full_new_filename)
        
    def generate_customer_report(self):
        erp_login = ErpLogin(self.driver)
        navigate = CommonPageNavigation(self.driver)

        erp_login.erp_login()
        navigate.navigate_to_customer_report_page()
        
        start_code = 1
        final_code = 5000
        select_boxes = True
        while final_code <= self.__FINAL_CODE:
            self.__generate_csv(start_code, final_code, select_boxes)
            final_filename = f"{self.__CUSTOMER_PROVIDER_REPORT_NEW_NAME}_{final_code}.csv"
            self.__rename_file(self.__CUSTOMER_PROVIDER_REPORT_DEFAULT_NAME, final_filename)
            navigate.return_page()
            select_boxes = False
            start_code = final_code
            final_code = final_code + 5000

        self.driver.quit()
