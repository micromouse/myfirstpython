from decimal import Decimal
from typing import List

from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from pydantic.v1.errors import cls_kwargs

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult
from excel.core.models.purchase_detail import PurchaseDetail, CI00PurchaseDetail, PL10PurchaseDetail
from excel.core.utils import Utils
from excel.handlers.reader.read_handler_base import ReadhandleBase

@Dispatcher.register_handlers
class ReadPurchaseDetailHandlers(ReadhandleBase):
    """
    通用处理器
    """

    @Dispatcher.keyword("READ_SHIPPING")
    def handle_purchase_details(self, cell: Cell) -> CellparseResult:
        """
        处理采购明细
        """
        invoice_number = ""
        purchase_details: List[PurchaseDetail] = []
        last_row_index = cell.row + 1

        # 从当前单元格所在行开始迭代
        for row_index, row in enumerate(self._worksheet.iter_rows(min_row=cell.row + 2), start=cell.row + 2):
            # 先找到invocie_number
            if not invoice_number:
                invoice_number = self._get_invoice_number(row)
                continue

            # 找到采购明细
            first_cell_value = Utils.get_cell_value(self._worksheet, row[0])
            if first_cell_value and self._worksheet.title.upper() == "CI00":
                purchase_details.append(self._get_ci00_purchase_detail(row))
            elif first_cell_value and self._worksheet.title.upper() == "PL10":
                purchase_details.append(self._get_pl10_purchase_detail(row))

            # 采购明细行结束
            if purchase_details and first_cell_value == "":
                last_row_index = row_index
                break

        return CellparseResult(result={
            "invoice_number": invoice_number,
            "purchase_details": purchase_details
        }, next_row_index=last_row_index)

    def _get_invoice_number(self, row: tuple[Cell, ...]) -> str:
        """
        从指定行获得发票号信息
        """
        for index, cell in enumerate(row):
            if Utils.get_cell_value(self._worksheet, cell) == "AS PER PROFORMA INVOICE NO. :":
                return Utils.get_cell_value(self._worksheet, row[index + 2])

        # 没有找到发票号
        return ""

    def _get_ci00_purchase_detail(self, row: tuple[Cell, ...]) -> CI00PurchaseDetail:
        """
        获得CI00采购明细信息
        """
        purchase_detail: CI00PurchaseDetail = {
            "shipping_marks": Utils.get_cell_value(self._worksheet, row[0]),
            "material_code": Utils.get_cell_value(self._worksheet, row[2]),
            "description": Utils.get_cell_value(self._worksheet, row[6]),
            "quantity": int(Utils.get_cell_value(self._worksheet, row[9], "0").replace(",", "")),
            "unit_price": Decimal(Utils.get_cell_value(self._worksheet, row[10], "0").replace(",", "")),
            "amount_usd": Decimal(Utils.get_cell_value(self._worksheet, row[11], "0").replace(",", "")),
            "origin_country": Utils.get_cell_value(self._worksheet, row[12]),
            "remark": Utils.get_cell_value(self._worksheet, row[13])
        }
        return purchase_detail

    def _get_pl10_purchase_detail(self, row: tuple[Cell, ...]) -> PL10PurchaseDetail:
        """
        获得PL10采购明细信息
        """
        purchase_detail: PL10PurchaseDetail = {
            "shipping_marks": Utils.get_cell_value(self._worksheet, row[0]),
            "material_code": Utils.get_cell_value(self._worksheet, row[13]),
            "description": Utils.get_cell_value(self._worksheet, row[4]),
            "total_quantity": int(Utils.get_cell_value(self._worksheet, row[8], "0").replace(",", "")),
            "total_packages": int(row[11].value) if row[11].value else None
        }
        return purchase_detail
