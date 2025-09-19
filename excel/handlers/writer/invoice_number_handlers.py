from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.models.parse_result import CellparseResult
from excel.core.dispatcher import Dispatcher
from excel.core.utils import Utils
from .write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class InvoicenumberHandlers(WriteHandlerBase):
    """
    发票号处理器
    """
    _invoice_number: str = ""

    @classmethod
    @Dispatcher.keyword("WRITE_INVOICE NO.")
    def handle_invoice_number(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票号(货代Invoice和With material code Sheet用)
        """
        sheet.cell(cell.row, cell.column + 2).value = cls._save_and_get_invoice_number()
        return CellparseResult()

    @classmethod
    @Dispatcher.keyword("WRITE_PACKING LIST NO.")
    def handle_packing_list_number(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票号(货代Packing Sheet用)
        """
        sheet.cell(cell.row, cell.column + 2).value = cls._save_and_get_invoice_number()
        return CellparseResult()

    @classmethod
    def _save_and_get_invoice_number(cls) -> str:
        """
        保存并获得发票号
        :return: 发票号
        """
        # 未设置发票号,先设置发票号
        if cls._invoice_number == "":
            cls._invoice_number = cls._get_data_source()["invoice_number"]

        return cls._invoice_number
