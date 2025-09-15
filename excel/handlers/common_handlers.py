from decimal import Decimal
from typing import Dict, List

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.dispatcher import Dispatcher
from excel.core.models.cell_parse_result import CellparseResult
from excel.core.models.purchase_detail import PurchaseDetail

class CommonHandlers:
    """
    通用处理器
    """

    @staticmethod
    @Dispatcher.regiter_handler("INVOICE DATE :")
    def handle_invoice_date(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票日期
        """
        invoice_number = str(sheet.cell(cell.row, cell.column + 1).value).strip()
        return CellparseResult({"invoice_date": invoice_number})

    @staticmethod
    @Dispatcher.regiter_handler("SHIPPING")
    def handle_purchase_details(sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理采购明细
        """
        invoice_number = ""
        purchase_details: List[PurchaseDetail] = []
        last_row_index = cell.row

        # 从当前单元格所在行开始迭代(values_only=True表示迭代的每一项为元组)
        for row in sheet.iter_rows(min_row=cell.row, values_only=True):
            # 先找到invocie_number
            if invoice_number == "":
                if "AS PER PROFORMA INVOICE NO. :" in [str(cell) for cell in row]:
                    invoice_number = str(row[8]).strip()
                continue

            # 找到采购明细
            if not row[0]:
                purchase_details.append(CommonHandlers._parse_purchase_detail_row(row))

            # 采购明细行结束
            if len(purchase_details) > 0 and str(row[0] if row[0] is not None else "") == "":
                break

            # 已处理的最后行索引
            last_row_index += 1

        return CellparseResult(result={
            "last_row_index": last_row_index,
            "invoice_number": invoice_number,
            "purchase_details": purchase_details
        }, next_row_index=last_row_index + 1)

    @staticmethod
    def _parse_purchase_detail_row(row: tuple) -> PurchaseDetail:
        """
        解析采购明细行
        """
        purchase_detail: PurchaseDetail = {
            "hs_code": str(row[0]) if row[0] is not None else "",
            "model": "",
            "material_code": str(row[2]) if row[2] is not None else "",
            "description": str(row[6]) if row[6] is not None else "",
            "quantity": int(row[9]) if row[9] is not None else 0,
            "unit_price": Decimal(str(row[10])) if row[10] is not None else Decimal("0"),
            "amount_usd": Decimal(str(row[11])) if row[11] is not None else Decimal("0"),
            "origin_country": str(row[12]) if row[12] is not None else ""
        }
        return purchase_detail
