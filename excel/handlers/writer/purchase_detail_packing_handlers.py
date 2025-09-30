from injector import inject
from openpyxl.cell.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import PL10ReadParseResult, CellparseResult
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.writer.purchase_detail_handlers import WritePurchasedetailHandlers
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class WritePurchasedetailPackingHandlers(WritePurchasedetailHandlers, WriteHandlerBase):
    """
    [货代 Packing]采购明细处理器
    """

    @inject
    def __init__(self, workbook: Workbook, worksheet: Worksheet, datasource: WriterDataSource):
        """
        初始化E[货代 Invoice]采购明细处理器
        :param workbook: 要写入的Workbook
        :param worksheet: 要写入的Worksheet
        :param datasource: Excel写入器数据源
        """
        super().__init__(workbook, worksheet, datasource)

    @Dispatcher.keyword("WRITE_SHIPPING MARKS")
    def handle_packing_purchase_detail(self, cell: Cell) -> CellparseResult:
        """
        处理[货代Packing] Sheet采购明细
        """
        purchase_details = self._datasource.get_data_source(PL10ReadParseResult)["purchase_details"]
        self._insert_blank_rows(cell.row + 1, len(purchase_details))
        return CellparseResult()
