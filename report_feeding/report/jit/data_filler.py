from openpyxl import load_workbook
from report_feeding.report.jit.utils import get_jit_report_vertical_count
from report_feeding.report.jit.utils import JIT_COLUMNS_USED, FIRST_COLUMN_USED, COLUMN_INTERVAL, FIRST_ROW_USED, JIT_VERTICAL_SIZE, ROW_INTERVAL, STORE_VALUE, REPRO_VALUE


class FillerData:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
        self.__JIT_VERTICAL_COUNT = get_jit_report_vertical_count(len(self.data))
        
    def __format_name(self, source_name):
        if len(source_name) < 20:
            return source_name
        list_name = source_name.split(' ')
        list_name_used = [name for name in list_name if name.lower() not in list_name]
        list_short_middle_name = [name[0] for name in list_name_used[1:-1]]
        middle_name = ' '.join(name for name in list_short_middle_name)
        final_name = f'{list_name_used[0]} {middle_name} {list_name_used[-1]}'
        return final_name
    
    def __format_vendor(self, source_name):
        if len(source_name) < 24:
            return source_name
        source_name_with_no_digits = source_name.split('-')[1] if source_name[0].isdigit() else source_name
        prefix = f"{source_name.split('-')[0]} - " if source_name[0].isdigit() else ''
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
            (first_row + 3): data[2],
            (first_row + 5): data[3],
            (first_row + 6): data[4],
        }
    
    def __fill_box(self, ws, first_row, last_row, first_column, data):
        for row in ws.iter_rows(min_row=first_row, max_row=last_row, min_col=first_column, max_col=first_column):
            for cell in row:
                if cell.row in data.keys():
                    cell.value = data[cell.row]
        
    def fill(self):
        wb = load_workbook(self.filename)
        ws = wb.active
        
        sort_data = self.__convert_to_string(self.__get_sort_data())
        rows_count = len(sort_data)
        
        first_column = FIRST_COLUMN_USED
        total = rows_count
        for column in JIT_COLUMNS_USED:
            first_row = FIRST_ROW_USED
            for row in range(1, self.__JIT_VERTICAL_COUNT):
                row_data = self.__get_values_per_row(sort_data[rows_count - total], first_row)
                last_row = first_row + JIT_VERTICAL_SIZE
                self.__fill_box(ws, first_row, last_row, first_column, row_data)
                first_row = last_row + ROW_INTERVAL

                total = total - 1
                
                if total <= 0:
                    break
            
            first_column = first_column + COLUMN_INTERVAL
        
        wb.save(self.filename)
        
        