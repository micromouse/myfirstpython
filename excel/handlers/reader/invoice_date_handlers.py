from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.dispatcher import Dispatcher
from excel.core.models.cell_parse_result import CellparseResult

class InvoicedateHandlers:
    """
    发票日期处理器
    """

    @staticmethod
    @Dispatcher.regiter_handler("READ_INVOICE DATE :")
    def handle_invoice_date(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票日期
        """
        invoice_number = str(sheet.cell(cell.row, cell.column + 1).value).strip()
        return CellparseResult({"invoice_date": invoice_number})
