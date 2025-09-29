from openpyxl.cell.cell import Cell

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult
from excel.handlers.reader.read_handler_base import ReadhandleBase

@Dispatcher.register_handlers
class ReadInvoicedateHandlers(ReadhandleBase):
    """
    发票日期处理器
    """

    @Dispatcher.keyword("READ_INVOICE DATE :")
    def handle_invoice_date(self, cell: Cell) -> CellparseResult:
        """
        处理发票日期
        """
        invoice_number = str(self._worksheet.cell(cell.row, cell.column + 1).value).strip()
        return CellparseResult({"invoice_date": invoice_number})
