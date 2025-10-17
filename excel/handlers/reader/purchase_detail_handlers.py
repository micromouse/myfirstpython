from typing import List

from injector import inject
from openpyxl.cell.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult
from excel.core.models.purchase_detail import PurchaseDetail, CI00PurchaseDetail, PL10PurchaseDetail
from excel.core.utils import Utils
from excel.handlers.reader.read_handler_base import ReadhandleBase
from excel.handlers.services.sales_price_table_service import SalespriceTableService

@Dispatcher.register_handlers
class ReadPurchaseDetailHandlers(ReadhandleBase):
    """
    采购明细处理器
    """

    @inject
    def __init__(
            self,
            workbook: Workbook,
            worksheet: Worksheet,
            sales_price_table_service: SalespriceTableService):
        """
        初始化采购明细处理器
        :param workbook: Workbook
        :param worksheet: Worksheet
        :param sales_price_table_service: 销售价目表服务
        """
        super().__init__(workbook, worksheet)
        self._sales_price_table_service = sales_price_table_service

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
        material_code = Utils.get_cell_value(self._worksheet, row[2])
        quantity = int(float(Utils.get_cell_value(self._worksheet, row[9], "0").replace(",", "")))
        unit_price = self._sales_price_table_service.get_sales_price(material_code)
        purchase_detail: CI00PurchaseDetail = {
            "shipping_marks": Utils.get_cell_value(self._worksheet, row[0]),
            "material_code": material_code,
            "description": Utils.get_cell_value(self._worksheet, row[6]),
            "quantity": quantity,
            "unit_price": unit_price,
            "amount_usd": quantity * unit_price,
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
            "total_quantity": int(float(Utils.get_cell_value(self._worksheet, row[8], "0").replace(",", ""))),
            "total_packages": int(row[11].value) if row[11].value else None
        }
        return purchase_detail
