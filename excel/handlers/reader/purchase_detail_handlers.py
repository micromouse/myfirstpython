from decimal import Decimal
from typing import List, Union

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.Utils import Utils
from excel.core.dispatcher import Dispatcher
from excel.core.models.cell_parse_result import CellparseResult
from excel.core.models.purchase_detail import CI00PurchaseDetail, PL10PurchaseDetail

class PurchaseDetailHandlers:
    """
    通用处理器
    """

    @staticmethod
    @Dispatcher.regiter_handler("READ_SHIPPING")
    def handle_purchase_details(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理采购明细
        """
        invoice_number = ""
        purchase_details: List[Union[CI00PurchaseDetail, PL10PurchaseDetail]] = []
        last_row_index = cell.row + 1

        # 从当前单元格所在行开始迭代
        for row_index, row in enumerate(sheet.iter_rows(min_row=cell.row + 2), start=cell.row + 2):
            # 先找到invocie_number
            if not invoice_number:
                invoice_number = PurchaseDetailHandlers._get_invoice_number(sheet, row)
                continue

            # 找到采购明细
            first_cell_value = Utils.get_cell_value(sheet, row[0])
            if first_cell_value and sheet.title.upper() == "CI00":
                purchase_details.append(PurchaseDetailHandlers._get_ci00_purchase_detail(sheet, row))
            elif first_cell_value and sheet.title.upper() == "PL10":
                purchase_details.append(PurchaseDetailHandlers._get_pl10_purchase_detail(sheet, row))

            # 采购明细行结束
            if purchase_details and first_cell_value == "":
                last_row_index = row_index
                break

        return CellparseResult(result={
            "invoice_number": invoice_number,
            "purchase_details": purchase_details
        }, next_row_index=last_row_index)

    @staticmethod
    def _get_invoice_number(sheet: Worksheet, row: tuple[Cell, ...]) -> str:
        """
        从指定行获得发票号信息
        """
        for index, cell in enumerate(row):
            if Utils.get_cell_value(sheet, cell) == "AS PER PROFORMA INVOICE NO. :":
                return Utils.get_cell_value(sheet, row[index + 2])

        # 没有找到发票号
        return ""

    @staticmethod
    def _get_ci00_purchase_detail(sheet: Worksheet, row: tuple[Cell, ...]) -> CI00PurchaseDetail:
        """
        获得CI00采购明细信息
        """
        purchase_detail: CI00PurchaseDetail = {
            "shipping_marks": Utils.get_cell_value(sheet, row[0]),
            "material_code": Utils.get_cell_value(sheet, row[2]),
            "description": Utils.get_cell_value(sheet, row[6]),
            "quantity": int(Utils.get_cell_value(sheet, row[9], "0").replace(",", "")),
            "unit_price": Decimal(Utils.get_cell_value(sheet, row[10], "0").replace(",", "")),
            "amount_usd": Decimal(Utils.get_cell_value(sheet, row[11], "0").replace(",", "")),
            "origin_country": Utils.get_cell_value(sheet, row[12])
        }
        return purchase_detail

    @staticmethod
    def _get_pl10_purchase_detail(sheet: Worksheet, row: tuple[Cell, ...]) -> PL10PurchaseDetail:
        """
        获得PL10采购明细信息
        """
        purchase_detail: PL10PurchaseDetail = {
            "shipping_marks": Utils.get_cell_value(sheet, row[0]),
            "material_code": Utils.get_cell_value(sheet, row[13]),
            "description": Utils.get_cell_value(sheet, row[4]),
            "total_quantity": int(Utils.get_cell_value(sheet, row[8], "0").replace(",", "")),
            "total_packages": int(Utils.get_cell_value(sheet, row[11], "0").replace(",", ""))
        }
        return purchase_detail
