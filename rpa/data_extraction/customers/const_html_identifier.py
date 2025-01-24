class CustomerProviderHtmlTagIdentifiers:
    # XPATH
    CUSTOMER_GENERATE_REPORT_XPATH = "/html/body/form/table/tbody/tr[27]/td[2]/input"
    CUSTOMER_TEXT_FILE_OPTION_XPATH = "/html/body/form/font/font/table[3]/tbody/tr/td/input[8]"
    START_CODE_XPATH = "/html/body/form/table/tbody/tr[1]/td[2]/input[1]"
    END_CODE_XPATH = "/html/body/form/table/tbody/tr[1]/td[2]/input[2]"
    GENERATE_CSV_FILE_BUTTON_XPATH = "//*[@id='tabela_wrapper']/div[3]/a[1]"
    
    # ID
    CUSTOMER_TYPE_CHECK_ID = "f_tipo_cliente1"
    CUSTOMER_AND_PROVIDER_TYPE_CHECK_ID = "f_tipo_cliente3"
    DISABLED_CUSTOMERS_CHECK_ID = "desabilitados"
    LIST_IN_COLUMNS_CHECK_ID = "resumida"
    SELECT_ALL_CUSTOMERS_BUTTON_ID = "selecionar"
    START_DATE_FORM_ID = "data_1"
    END_DATE_FORM_ID = "data_2"
    SHOW_FIELDS_BOX_ID = "exibir_campos"
