from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult, CI00ReadParseResult, PL10ReadParseResult
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class WritePurchasedetailHandlers(WriteHandlerBase):
    """
    采购明细处理器
    """

    @Dispatcher.keyword("WRITE_HS")
    def handle_invoice_purchase_detail(self, cell: Cell) -> CellparseResult:
        """
        处理[货代Invoice] Sheet采购明细
        """
        purchase_details = self._datasource.get_data_source(CI00ReadParseResult)["purchase_details"]
        self._insert_blank_rows(cell.row + 2, len(purchase_details))

        return CellparseResult()

    @Dispatcher.keyword("WRITE_SHIPPING MARKS")
    def handle_packing_purchase_detail(self, cell: Cell) -> CellparseResult:
        """
        处理[货代Packing] Sheet采购明细
        """
        purchase_details = self._datasource.get_data_source(PL10ReadParseResult)["purchase_details"]
        self._insert_blank_rows(cell.row + 2, len(purchase_details))
        return CellparseResult()

    def _insert_blank_rows(self, index: int, count: int):
        """
        插入空白行
        :param index: 插入行索引(在索引位置前插入空白行)
        :param count: 行数
        """
        self._worksheet.delete_rows(index, 1)
        self._worksheet.insert_rows(index, count)

        # 重置新插入行的行高
        for row_index in range(index, index + count):
            self._worksheet.row_dimensions[row_index].height = None

        return self
