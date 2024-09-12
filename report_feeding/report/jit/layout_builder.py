from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font, Alignment
from openpyxl.styles import PatternFill
from report_feeding.report.jit.utils import get_jit_report_vertical_count
from report_feeding.report.jit.utils import STORE_VALUE, REPRO_VALUE


class LayoutBuilder:
    def __init__(self, rows_count, filename, repro_count):
        self.__CORNER_BORDER = Border(left=Side(style='thick'), right=Side(style='thick'))
        self.__TOP_BORDER = Border(top=Side(style='thick'), left=Side(style='thick'), right=Side(style='thick'))
        self.__BOTTOM_BORDER = Border(bottom=Side(style='thick'), left=Side(style='thick'),  right=Side(style='thick'))
        
        self._REPRO_COUNT = repro_count
        
        # Layout Details
        self.__HORIZONTAL_ALIGNMENT = 'center'
        self.__FIRST_ROW_VALUE = '\'++++'
        self.__FONT = 'Arial'
        
        self.__LAYOUT_CONFIG = {
            STORE_VALUE: {
                'background_color': '0000B050',
                'fill_type': 'solid',
                'font_color': 'FFFFFF',
                'font_size': 10,
                'value': STORE_VALUE
            },
            REPRO_VALUE: {
                'background_color': 'ff000000',
                'fill_type': 'solid',
                'font_color': 'FFFFFF',
                'font_size': 10,
                'value': REPRO_VALUE
            }
        }
        
        self.filename = filename
        self.rows_count = rows_count
    
    def _generate_layout(self, ws, first_row, last_row, first_column, box_type):
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
