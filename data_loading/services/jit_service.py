import csv
from data_loading.repositories.jit_repository import JitRepository
from data_processing.jit import Jit as JitProcess
from data_loading.models.jit import Jit
from typing import List, Dict


class JitService:
    """
    Services: Jit Class
    
    Used to create/update/delete Jits information in the database.
    
    Attributes:
        jit_repository (JitRepository)
    """
    def __init__(self, jit_repository: JitRepository):
        self.jit_repo = jit_repository

        self.SENT_TO_LABORATORY_STRING = "Enviada ao laboratório"
        self.__VENDOR_ALIAS = {
            "6": "Nany",
            "15": "Nany", # needs review
            "16": "Nany",
            "20": "Aline",
            "12": "Marilete",
            "19": "Adriana"
        }

    def __get_jit_list(self, jit_filename: str):
        """
        Gets list of Jits that have 'status' column as 'Enviada ao laboratório' from file extracted by RPA.
        
        Note:
            It needs the execution from RPA to export Jit report.
        
        Args:
            jit_filename (str): Filename used to read Jits.
            
        Returns:
            List of dictionaries of Jits
        """
        jit_file = open(jit_filename, mode='r', encoding='utf-8')
        reader = csv.DictReader(jit_file, delimiter=',', fieldnames=JitProcess.get_jit_csv_column_names())
        return [row for row in reader if row[JitProcess.STATUS_COLUMN] == self.SENT_TO_LABORATORY_STRING]

    def __process_jit(self, jit_list: List[Dict[str, str]]):
        """
        Applies some light data transformation in the jit data, such as date formatting and str to int casting.
        
        Args:
            jit_list (List[Dict[str,str]]): List of jit dictionaries
        """
        JitProcess.process_csv_date_field(jit_list, JitProcess.OS_DATE_COLUMN)
        JitProcess.process_csv_date_field(jit_list, JitProcess.DUE_DATE_COLUMN)
        JitProcess.process_csv_int_with_comma_and_period_field(jit_list, JitProcess.OS_NUMBER_COLUMN)

    def __get_vendor_alias(self, vendor_name: str):
        """
        Gets the vendor alias based into a code number.
        
        Args:
            vendor_name (str): Vendor code + full name in '00 - Name' format
            
        Returns:
            str: The vendor alias
        """
        vendor_code = vendor_name[:2].rstrip()
        return self.__VENDOR_ALIAS[vendor_code]

    def __save_jit_as_not_generated_on_db(self, jit_list: List[Dict[str, str]]):
        """
        Creates new Jit in the database as not generated.
        
        Args:
            jit_list (List[Dict[str, str]]): dataframe with all jits
        """
        for row in jit_list:
            vendor_with_alias = self.__get_vendor_alias(row[JitProcess.VENDOR_ROW_COLUMN])
            jit = Jit(
                os_date=row[JitProcess.OS_DATE_COLUMN],
                os_number=row[JitProcess.OS_NUMBER_COLUMN],
                laboratory=row[JitProcess.LABORATORY_COLUMN],
                customer_name=row[JitProcess.CUSTOMER_NAME_COLUMN],
                note=row[JitProcess.NOTE_COLUMN],
                due_date=row[JitProcess.DUE_DATE_COLUMN],
                vendor=vendor_with_alias,
                status=row[JitProcess.STATUS_COLUMN],
                is_generated=False
            )
            self.jit_repo.create_jit_only_if_doesnt_exist(jit)

    def get_all_not_generated_jit(self):
        """
        Retrieve the list of not generated Jit's from jit table in the database
        
        Returns:
            List[Jit]: List of Jits with is_generated=False in the database
        """
        not_generated_jit = self.jit_repo.get_all_not_generated_jit()
        return [jit for jit in not_generated_jit]

    def create_jit(self, jit_file: str):
        """
        Creates Jits with 'is_generate=False' on database using file of Jits extracted by RPA as source.
        
        Note:
            It needs the execution from RPA to export Jit report.

        Args:
            jit_file (str): Filename used to read Jits.
        """
        jit_list = self.__get_jit_list(jit_file)
        self.__process_jit(jit_list)
        jit_list_with_note_valid_values = JitProcess.filter_note_column_for_valid_values(jit_list)
        self.__save_jit_as_not_generated_on_db(jit_list_with_note_valid_values)

    def update_to_is_generated(self, not_generated_jit):
        """
        Updates all Jits that have is_generated=False to is_generated=True
        
        Args:
            not_generated_jit (List[Jit]): List of Jits that were not generated yet
        """
        for jit in not_generated_jit:
            self.jit_repo.update_to_is_generated(jit.os_number)

    def check_existance_of_jit_by_os_number(self, os_number):
        """
        Checks existance of Jit on the database by OS Number.
        
        Args:
            os_number (int): OS Number.
            
        Returns:
            Row in the database case it exists and 'None' if it doesn't.
        """
        return self.jit_repo.check_existence(os_number)

    def get_all(self):
        """
        Gets all Jits from database.
        
        Returns:
            Lits of all Jits on the database.
        """
        return self.jit_repo.get_all_jits()

    def delete_all(self):
        """
        Deletes all Jits on the database.
        """
        return self.jit_repo.delete_all_jits()
