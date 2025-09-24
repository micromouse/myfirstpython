from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult, CI00ReadParseResult, PL10ReadParseResult
from excel.core.models.purchase_detail import PL10PurchaseDetail
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class PurchasedetailHandlers(WriteHandlerBase):
    """
    采购明细处理器
    """

    @classmethod
    @Dispatcher.keyword("WRITE_HS")
    def handle_invoice_purchase_detail(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理[货代Invoice] Sheet采购明细
        """
        purchase_details = cls._get_data_source(CI00ReadParseResult)["purchase_details"]
        cls._insert_blank_rows(sheet, cell.row + 2, len(purchase_details) + 1)

        return CellparseResult()

    @classmethod
    @Dispatcher.keyword("WRITE_SHIPPING MARKS")
    def handle_packing_purchase_detail(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理[货代Packing] Sheet采购明细
        """
        purchase_details = cls._get_data_source(PL10ReadParseResult)["purchase_details"]
        sheet.insert_rows(cell.row + 2, len(purchase_details))
        return CellparseResult()

    @classmethod
    def _insert_blank_rows(cls, sheet: Worksheet, index: int, count: int):
        """
        插入空白行
        :param sheet: Worksheet
        :param index: 插入行索引(在索引位置前插入空白行)
        :param count: 行数
        """
        sheet.delete_rows(index, 1)
        sheet.insert_rows(index, count)

        # 重置新插入行的行高
        for row_index in range(index, index + count + 1):
            sheet.row_dimensions[row_index].height = None
