from decimal import Decimal

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.dispatcher import Dispatcher
from excel.core.models.cell_parse_result import CellparseResult
from excel.core.currency_formatter import CurrencyFormatter

class TotalHandlers:
    """
    合计数处理器
    """

    @staticmethod
    @Dispatcher.regiter_handler("READ_TOTAL :")
    def handle_total(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理合计值
        """
        total_quantity = int(str(sheet.cell(cell.row, cell.column + 1).value).replace(",", ""))
        total_amount = Decimal(str(sheet.cell(cell.row, cell.column + 3).value).replace(",", ""))
        return CellparseResult({
            "total_quantity": total_quantity,
            "total_amount": total_amount,
            "total_amount_english": CurrencyFormatter.format_currency_amount(total_amount)
        })

    @staticmethod
    @Dispatcher.regiter_handler("READ_TOTAL GROSS WEIGHT")
    def handle_total_gross_weight(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理 [TOTAL GROSS WEIGHT][TOTAL NET WEIGHT][TOTAL PACKAGES][TOTAL QUANTITY][TOTAL MEASUREMENT]
        """
        total_gross_weight = Decimal(str(sheet.cell(cell.row, cell.column + 6).value).replace(",", ""))
        total_net_weight = Decimal(str(sheet.cell(cell.row + 1, cell.column + 6).value).replace(",", ""))
        total_packages = int(str(sheet.cell(cell.row + 2, cell.column + 6).value).replace(",", ""))
        total_quantity = int(str(sheet.cell(cell.row + 3, cell.column + 6).value).replace(",", ""))
        total_measurement = Decimal(str(sheet.cell(cell.row + 4, cell.column + 6).value).replace(",", ""))
        return CellparseResult({
            "total_gross_weight": total_gross_weight,
            "total_net_weight": total_net_weight,
            "total_packages": total_packages,
            "total_quantity": total_quantity,
            "total_measurement": total_measurement
        }, next_row_index=cell.row + 5)
