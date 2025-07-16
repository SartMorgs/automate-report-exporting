from datetime import datetime
from openpyxl import Workbook
from report_feeding.report.jit.utils import Utils as ReportFeedingUtils
from data_processing.jit import Jit as JitProcess
from report_feeding.report.jit.layout_builder import LayoutBuilder
from typing import List, Dict


class FillerData(LayoutBuilder):
    """
    Report Feeding: Filler Data Class
    
    Used for filling the report with the correct data from the source data.
    
    Attributes:
        filename (str): Report filename to be saved.
        data (List[Dict[str, str]]): The source data used to fill the report.
        repro_count (int): The amount of rows with ```laboratory``` column as ```19944 - REPRO PRODUTOS OPTICOS LTDA.```
    """
    def __init__(self, filename: str, data: List[Dict[str, str]], repro_count: int):
        self.filename = filename
        self.data = data
        
        self.__JIT_VERTICAL_COUNT = ReportFeedingUtils.get_jit_report_vertical_count(len(self.data)) + 1
        self._REPRO_COUNT = repro_count
        
        super().__init__(filename)

    def __format_name(self, source_name: str):
        """
        Formats the name replacing the whole name for a short version in order to fit in the card space.

        Args:
            source_name (str): Full name version

        Returns:
            Shorter version of full name with len < 20 (str).
        """
        if len(source_name) < 20:
            return source_name

        list_name = ReportFeedingUtils.split_list_by_space(source_name)
        list_name_used = ReportFeedingUtils.get_list_of_strings_with_more_than_two_char(list_name)

        list_short_middle_name = ReportFeedingUtils.get_first_letter_of_each_string(list_name_used[ReportFeedingUtils.FIRST_NAME:ReportFeedingUtils.LAST_NAME])
        all_middle_name = " ".join(name for name in list_short_middle_name)

        final_name = f"{list_name_used[ReportFeedingUtils.FIRST_NAME]} {all_middle_name} {list_name_used[ReportFeedingUtils.LAST_NAME]}"
        return final_name
    
    def __get_seller_name_from_seller_string(self, source_seller_string: str):
        """
        Gets vendor number and name from seller string that comes from seller column.
        
        Args:
            source_seller_string (str): Complete seller string.
            
        Returns:
            Number of that identifies the seller and the seller name. (str), (str)
        """
        if source_seller_string[ReportFeedingUtils.FIRST_LIST_ITEM].isdigit():
            return f"{source_seller_string.split('-')[ReportFeedingUtils.FIRST_LIST_ITEM]} - ", source_seller_string.split("-")[ReportFeedingUtils.SECOND_LIST_ITEM]
        return "", source_seller_string

    def __format_seller(self, source_name: str):
        """
        Formats the seller name to be shorter than 24 char, cutting off middle name to make the whole name shorter.
        
        Args:
            source_name (str): Source seller name.
            
        Returns:
            Shorter version of seller name with digit prefix. (str)
        """
        if len(source_name) < 24:
            return source_name

        prefix, source_name_with_no_digits = self.__get_seller_name_from_seller_string(source_name)
        short_name = self.__format_name(source_name_with_no_digits)
        return (prefix + short_name)

    def __format_customer_and_seller_name(self):
        """
        Formats the customer and seller name into data passed in the object creation.
        """
        for row in self.data:
            row[JitProcess.CUSTOMER_NAME_COLUMN] = self.__format_name(row[JitProcess.CUSTOMER_NAME_COLUMN])
            row[JitProcess.SELLER_COLUMN] = self.__format_seller(row[JitProcess.SELLER_COLUMN])
    
    def __get_values_per_sheet_row(self, data: List[Dict[str, str]], start_row: str):
        """
        Gets the values that are gonna be used for each row in the spreadsheet.
        
        Args:
            data (List[Dict[str, str]]): Data with the infoto fill the spreadsheet
            start_row (int): Index row which starts the report that are gonna be filled.
            
        Returns:
            Dict with keys as row number in the spreadsheets and values with info to be filled out. (Dict[str, str])
        """
        report_layout_positions = ReportFeedingUtils.get_report_layout_positions(start_row)
        return {
            report_layout_positions[ReportFeedingUtils.CUSTOMER_NAME]: data[JitProcess.CUSTOMER_NAME_COLUMN],
            report_layout_positions[ReportFeedingUtils.SELLER_NAME]: data[JitProcess.SELLER_COLUMN],
            report_layout_positions[ReportFeedingUtils.DUE_DATE]: data[JitProcess.DUE_DATE_COLUMN],
            report_layout_positions[ReportFeedingUtils.OS_NUMBER]: data[JitProcess.OS_NUMBER_COLUMN],
            report_layout_positions[ReportFeedingUtils.NOTE]: data[JitProcess.NOTE_COLUMN],
        }
    
    def __fill_box(
        self, active_ws: Workbook, first_row_index: int, last_row_index: int, column_index: int, report_data: List[Dict[str, str]]):
        """
        Fills the jit card report with the info data.
        
        Args:
            active_ws (Workbook): The active worksheet.
            first_row_index (int): The first row of the jit card.
            last_row_index (int): The last row of the jit card.
            column_index (str): The column index.
            report_data (List[Dict[str, str]]): The info data for the report filling.
        """
        for line in active_ws.iter_rows(min_row=first_row_index, max_row=last_row_index, min_col=column_index, max_col=column_index):
            for cell in line:
                if cell.row in report_data.keys():
                    cell.value = report_data[cell.row]

    def __set_layout_for_column(self, active_ws, column, first_row_index, last_row_index, column_index, amount_of_store_data):
        """
        Sets the proper layout for each column given the active worksheet and position that the card should be.
        
        Args:
            active_ws (Workbook): The active worksheet.
            column (str): The column that will be dimensioned.
            first_row_index (int): The first row of the jit card.
            last_row_index (int): The last row of the jit card.
            column_index (str): The column index.
            amount_of_store_data (int): The amount of data with store laboratory type.
        """
        active_ws.column_dimensions[column].width = ReportFeedingUtils.JIT_COLUMN_SIZE
        jit_card_type = ReportFeedingUtils.STORE_VALUE if amount_of_store_data > 0 else ReportFeedingUtils.REPRO_VALUE
        self._generate_layout(active_ws, first_row_index, last_row_index, column_index, jit_card_type)

    def __build_and_fill_line_of_report(
        self, active_ws: Workbook, amount_of_reports: int, reports_to_be_built: int, amount_of_store_data: int, first_row_index: int, last_row_index: int):
        """
        Builds and fills a line of the report.
        
        Args:
            active_ws (Workbook): The active worksheet.
            amount_of_reports (int): The amount of reports that are in the data.
            reports_to_be_built (int): The amount of reports that still needs to be built.
            amount_of_store_data (int): The amount of data with store laboratory type.
            first_row_index (int): The first row of the jit card.
            last_row_index (int): The last row of the jit card.
        
        Returns:
            The amount of store data that still needs to be built and the amount of reports that still needs to be built. (int), (int)
        """
        column_index = ReportFeedingUtils.FIRST_COLUMN_USED
        for column in ReportFeedingUtils.JIT_COLUMNS_USED:
            if reports_to_be_built <= 0:
                break
            self.__set_layout_for_column(active_ws, column, first_row_index, last_row_index, column_index, amount_of_store_data)
            amount_of_store_data -= 1

            row_data = self.__get_values_per_sheet_row(self.data[amount_of_reports - reports_to_be_built], first_row_index)
            self.__fill_box(active_ws, first_row_index, last_row_index, column_index, row_data)

            column_index = column_index + ReportFeedingUtils.COLUMN_INTERVAL
            reports_to_be_built -= 1
            
        return amount_of_store_data, reports_to_be_built

    def build_and_fill_report_cards(self):
        """
        Builds and fills the jit report card with the info data.
        It builds the layout based in standard design.
        It creates the store cards first and the rest of them are repro.
        """
        wb = Workbook()
        ws = wb.active

        self.__format_customer_and_seller_name()
        amount_of_reports = len(self.data)

        first_row_index = ReportFeedingUtils.FIRST_ROW_USED
        reports_to_be_built = amount_of_reports
        amount_of_store_data = amount_of_reports - self._REPRO_COUNT

        for _ in range(1, self.__JIT_VERTICAL_COUNT):
            last_row_index = first_row_index + ReportFeedingUtils.JIT_VERTICAL_SIZE
            amount_of_store_data, reports_to_be_built = self.__build_and_fill_line_of_report(
                ws, amount_of_reports, reports_to_be_built, amount_of_store_data, first_row_index, last_row_index
            )
            first_row_index = last_row_index + ReportFeedingUtils.ROW_INTERVAL
        
        wb.save(self.filename)
        
        