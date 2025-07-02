from datetime import datetime
from openpyxl import Workbook
from report_feeding.report.jit.utils import (
    get_jit_report_vertical_count, split_list_by_space, get_list_of_strings_with_more_than_two_char,
    get_first_letter_of_each_string
)
from report_feeding.report.jit.utils import (
    JIT_COLUMNS_USED, FIRST_COLUMN_USED, COLUMN_INTERVAL, FIRST_ROW_USED, JIT_VERTICAL_SIZE, ROW_INTERVAL, STORE_VALUE, REPRO_VALUE, JIT_COLUMN_SIZE,
    FIRST_CHAR, FIRST_NAME, LAST_NAME, FIRST_LIST_ITEM, SECOND_LIST_ITEM
)
from report_feeding.report.jit.layout_builder import LayoutBuilder


class FillerData(LayoutBuilder):
    def __init__(self, filename, data, repro_count):
        self.filename = filename
        self.data = data
        
        self.__JIT_VERTICAL_COUNT = get_jit_report_vertical_count(len(self.data)) + 1
        
        super().__init__(len(self.data), filename, repro_count)

    def __format_name(self, source_name):
        if len(source_name) < 20:
            return source_name

        list_name = split_list_by_space(source_name)
        list_name_used = get_list_of_strings_with_more_than_two_char(list_name)

        list_short_middle_name = get_first_letter_of_each_string(list_name_used[FIRST_NAME:LAST_NAME])
        all_middle_name = " ".join(name for name in list_short_middle_name)

        final_name = f"{list_name_used[FIRST_NAME]} {all_middle_name} {list_name_used[LAST_NAME]}"
        return final_name
    
    def __get_vendor_name_from_note_string(self, source_note_string):
        if source_note_string[FIRST_LIST_ITEM].isdigit():
            return f"{source_note_string.split('-')[FIRST_LIST_ITEM]} - ", source_note_string.split("-")[SECOND_LIST_ITEM]
        return "", source_note_string

    def __format_vendor(self, source_name):
        if len(source_name) < 24:
            return source_name

        prefix, source_name_with_no_digits = self.__get_vendor_name_from_note_string(source_name)
        short_name = self.__format_name(source_name_with_no_digits)
        return (prefix + short_name)

    def __get_sort_data(self):
        values_for_row = []
        for row in self.data:
            name = self.__format_name(row[3])
            vendor_name = self.__format_vendor(row[6])
            os_number = row[1]
            sorted_data = [name, vendor_name, row[5], os_number, row[4]]
            values_for_row.append(sorted_data)
        
        return values_for_row
    
    def __convert_to_string(self, data):
        string_data = []
        for line in data:
            new_line = [str(row) for row in line]
            string_data.append(new_line)
        return string_data
    
    def __get_values_per_row(self, data, first_row):
        return {
            (first_row + 1): data[0],
            (first_row + 2): data[1],
            (first_row + 3): datetime.strptime(data[2], '%Y-%m-%d').strftime('%d/%m/%Y'),
            (first_row + 5): data[3],
            (first_row + 6): data[4],
        }
    
    def __fill_box(self, ws, first_row, last_row, first_column, data):
        for row in ws.iter_rows(min_row=first_row, max_row=last_row, min_col=first_column, max_col=first_column):
            for cell in row:
                if cell.row in data.keys():
                    cell.value = data[cell.row]
        
    def build_and_fill(self):
        wb = Workbook()
        ws = wb.active
        
        sort_data = self.__convert_to_string(self.__get_sort_data())
        rows_count = len(sort_data)

        # This logic is used in both FillerData and LayoutBuilder
        first_row = FIRST_ROW_USED
        total = rows_count
        store_count = self.rows_count - self._REPRO_COUNT
        
        for row in range(1, self.__JIT_VERTICAL_COUNT):
            last_row = first_row + JIT_VERTICAL_SIZE
            first_column = FIRST_COLUMN_USED
            for column in JIT_COLUMNS_USED:
                if total <= 0:
                    break
                # Layout builder
                ws.column_dimensions[column].width = JIT_COLUMN_SIZE
                box_type = STORE_VALUE if store_count > 0 else REPRO_VALUE
                self._generate_layout(ws, first_row, last_row, first_column, box_type)
                store_count = store_count - 1

                row_data = self.__get_values_per_row(sort_data[rows_count - total], first_row)
                self.__fill_box(ws, first_row, last_row, first_column, row_data)
                
                first_column = first_column + COLUMN_INTERVAL
                total = total - 1

            first_row = last_row + ROW_INTERVAL
        
        wb.save(self.filename)
        
        