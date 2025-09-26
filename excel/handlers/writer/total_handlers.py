from openpyxl.cell.cell import Cell
from openpyxl.styles import Alignment
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult, CI00ReadParseResult, PL10ReadParseResult
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class TotalHandlers(WriteHandlerBase):
    """
    合计数处理器
    """

    @Dispatcher.keyword("WRITE_TOTAL :")
    def handle_total(self, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理合计值
        """
        if self._datasource._ci00_data_source is not None:
            # 货代 Invoice Sheet
            sheet.cell(cell.row, cell.column + 1, self._datasource.get_data_source(CI00ReadParseResult)["total_quantity"])
            sheet.cell(cell.row, cell.column + 3, self._datasource.get_data_source(CI00ReadParseResult)["total_amount"])
        elif self._datasource._pl10_data_source is not None:
            # 货代 Packing Sheet
            sheet.cell(cell.row, cell.column + 3, self._datasource.get_data_source(PL10ReadParseResult)["total_packages"])
            sheet.cell(cell.row, cell.column + 4, self._datasource.get_data_source(PL10ReadParseResult)["total_quantity"])
            sheet.cell(cell.row, cell.column + 5, self._datasource.get_data_source(PL10ReadParseResult)["total_net_weight"])
            sheet.cell(cell.row, cell.column + 6, self._datasource.get_data_source(PL10ReadParseResult)["total_gross_weight"])

        return CellparseResult()

    @Dispatcher.keyword("WRITE_TRADE TERMS:CIP EGYPT")
    def handle_total_amount_usd_english(self, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理美元合计英文显示
        """
        sheet.merge_cells(start_row=cell.row + 2, start_column=cell.column, end_row=cell.row + 2, end_column=cell.column + 4)
        sheet.cell(cell.row + 2, cell.column).alignment = Alignment(wrap_text=True, vertical="center")
        sheet.cell(cell.row + 2, cell.column, self._datasource.get_data_source(CI00ReadParseResult)["total_amount_english"])
        return CellparseResult(next_row_index=cell.row + 3)
