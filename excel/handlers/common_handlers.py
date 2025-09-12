from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from excel.core.dispatcher import Dispatcher
from excel.core.cell_parse_result import CellparseResult

class CommonHandlers:
    """
    通用处理器
    """

    @classmethod
    @Dispatcher.regiter_handler("发票号")
    def handle_invoice_number(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票号
        :param sheet: WorkSheet
        :param cell: 单元格
        :return: 单元格内容解析结果
        """
        pass
