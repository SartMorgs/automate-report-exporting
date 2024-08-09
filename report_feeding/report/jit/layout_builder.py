from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font, Alignment
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from report_feeding.report.jit.utils import get_jit_report_vertical_count
from report_feeding.report.jit.utils import JIT_COLUMNS_USED, FIRST_COLUMN_USED, COLUMN_INTERVAL, FIRST_ROW_USED, JIT_VERTICAL_SIZE, ROW_INTERVAL, STORE_VALUE, REPRO_VALUE


class LayoutBuilder:
    def __init__(self, rows_count, filename, repro_count):
        self.__CORNER_BORDER = Border(left=Side(style='thick'), right=Side(style='thick'))
        self.__TOP_BORDER = Border(top=Side(style='thick'), left=Side(style='thick'), right=Side(style='thick'))
        self.__BOTTOM_BORDER = Border(bottom=Side(style='thick'), left=Side(style='thick'),  right=Side(style='thick'))
        
        self.__JIT_COLUMN_SIZE = 27
        self.__JIT_VERTICAL_COUNT = get_jit_report_vertical_count(rows_count)
        self.__REPRO_COUNT = repro_count
        
        # Layout Details
        self.__HORIZONTAL_ALIGNMENT = 'center'
        self.__FIRST_ROW_VALUE = '\'++++'
        self.__FONT = 'Arial'
        
        self.__LAYOUT_CONFIG = {
            STORE_VALUE: {
                'background_color': '0000B050',
                'fill_type': 'solid',
                'font_color': 'FFFFFF',
                'font_size': 12,
                'value': STORE_VALUE
            },
            REPRO_VALUE: {
                'background_color': 'ff000000',
                'fill_type': 'solid',
                'font_color': 'FFFFFF',
                'font_size': 12,
                'value': REPRO_VALUE
            }
        }
        
        self.filename = filename
        self.rows_count = rows_count
    
    def __generate_layout(self, ws, first_row, last_row, first_column, box_type):
        for row in ws.iter_rows(min_row=first_row, max_row=last_row, min_col=first_column, max_col=first_column):
            for cell in row:
                cell.alignment = Alignment(horizontal=self.__HORIZONTAL_ALIGNMENT)
                cell.font = Font(name=self.__FONT)
                if cell.row == first_row:
                    cell.value = self.__FIRST_ROW_VALUE
                    cell.border = self.__TOP_BORDER
                elif cell.row == last_row:
                    cell.border = self.__BOTTOM_BORDER
                else:
                    cell.border = self.__CORNER_BORDER
                    
                if cell.row == last_row - 2:
                    cell.fill = PatternFill(start_color=self.__LAYOUT_CONFIG[box_type]['background_color'], fill_type=self.__LAYOUT_CONFIG[box_type]['fill_type'])
                    cell.font = Font(color=self.__LAYOUT_CONFIG[box_type]['font_color'], size=self.__LAYOUT_CONFIG[box_type]['font_size'], bold=True)
                    cell.value = self.__LAYOUT_CONFIG[box_type]['value']

    def build(self):
        wb = Workbook()
        ws = wb.active
        
        first_column = FIRST_COLUMN_USED
        total = self.rows_count
        store_count = self.rows_count - self.__REPRO_COUNT
        for column in JIT_COLUMNS_USED:
            ws.column_dimensions[column].width = self.__JIT_COLUMN_SIZE
            
            first_row = FIRST_ROW_USED
            for row in range(1, self.__JIT_VERTICAL_COUNT):
                last_row = first_row + JIT_VERTICAL_SIZE
                box_type = STORE_VALUE if store_count > 0 else REPRO_VALUE
                self.__generate_layout(ws, first_row, last_row, first_column, box_type)
                first_row = last_row + ROW_INTERVAL
                
                store_count = store_count - 1
                total = total - 1
                
                if total <= 0:
                    break
            
            first_column = first_column + COLUMN_INTERVAL
        
        wb.save(self.filename)