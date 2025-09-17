from decimal import Decimal
from typing import List, Union

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

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

        # 从当前单元格所在行开始迭代(values_only=True表示迭代的每一项为元组)
        for row_index, row in enumerate(sheet.iter_rows(min_row=cell.row + 2, values_only=True), start=cell.row + 2):
            # 先找到invocie_number
            if not invoice_number:
                invoice_number = PurchaseDetailHandlers._get_invoice_number(row)
                continue

            # 找到采购明细
            if row[0] and sheet.title.upper() == "CI00":
                purchase_details.append(PurchaseDetailHandlers._get_ci00_purchase_detail(row))
            elif row[0] and sheet.title.upper() == "PL10":
                purchase_details.append(PurchaseDetailHandlers._get_pl10_purchase_detail(row))

            # 采购明细行结束
            if purchase_details and str(row[0] if row[0] is not None else "") == "":
                last_row_index = row_index
                break

        return CellparseResult(result={
            "invoice_number": invoice_number,
            "purchase_details": purchase_details
        }, next_row_index=last_row_index)

    @staticmethod
    def _get_invoice_number(row: tuple) -> str:
        """
        从指定行获得发票号信息
        """
        for index, value in enumerate(row):
            if str(value).strip() == "AS PER PROFORMA INVOICE NO. :":
                return row[index + 2]

        # 没有找到发票号
        return ""

    @staticmethod
    def _get_ci00_purchase_detail(row: tuple) -> CI00PurchaseDetail:
        """
        获得CI00采购明细信息
        """
        purchase_detail: CI00PurchaseDetail = {
            "shipping_marks": str(row[0]) if row[0] is not None else "",
            "material_code": str(row[2]) if row[2] is not None else "",
            "description": str(row[6]) if row[6] is not None else "",
            "quantity": int(str(row[9]).replace(",", "")) if row[9] is not None else 0,
            "unit_price": Decimal(str(row[10].replace(",", ""))) if row[10] is not None else Decimal("0"),
            "amount_usd": Decimal(str(row[11]).replace(",", "")) if row[11] is not None else Decimal("0"),
            "origin_country": str(row[12].replace(",", "")) if row[12] is not None else ""
        }
        return purchase_detail

    @staticmethod
    def _get_pl10_purchase_detail(row: tuple) -> PL10PurchaseDetail:
        """
        获得PL10采购明细信息
        """
        purchase_detail: PL10PurchaseDetail = {
            "shipping_marks": str(row[0]) if row[0] is not None else "",
            "material_code": str(row[13]) if row[13] is not None else "",
            "description": str(row[4]) if row[4] is not None else "",
            "total_quantity": int(str(row[8]).replace(",", "")) if row[8] is not None else 0,
            "total_packages": int(str(row[11]).replace(",", "")) if row[11] is not None else 0
        }
        return purchase_detail
