from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class WriteInvoicedateHandlers(WriteHandlerBase):
    """
    发票日期处理器
    """

    @Dispatcher.keyword("WRITE_DATE :")
    def handle_invoice_date(self, cell: Cell) -> CellparseResult:
        """
        处理发票日期
        """
        self._worksheet.cell(cell.row, cell.column + 1).value = self._datasource.get_common_data_source()["invoice_date"]
        if self._worksheet.title == "货代 Invoice":
            self._workbook["With material code"].cell(cell.row, cell.column + 1).value = self._datasource.get_common_data_source()["invoice_date"]
        return CellparseResult()
