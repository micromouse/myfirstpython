from decimal import Decimal
from pathlib import Path
from typing import Dict

from injector import inject

from excel.core.utils import Utils
from excel.handlers.models.pending_file_model import PendingFileModel

class SalespriceTableService:
    """
    销售价格表服务
    """
    _sales_prices: Dict[Path, Dict[str, Decimal]] = {}

    @inject
    def __init__(self, pending_file_model: PendingFileModel):
        """
        初始化销售价格服务
        :param pending_file_model: 正在处理的[采购CI&PL]文件模型
        """
        self._pending_file_model = pending_file_model
        if pending_file_model.brand_subcategory_path not in self._sales_prices:
            self._load_sales_prices()

    def get_sales_price(self, material_code: str) -> Decimal:
        """
        由物料编码获得报关单价
        :param material_code: 物料编码
        :return: 报关单价
        """
        if material_code not in self._sales_prices[self._pending_file_model.brand_subcategory_path]:
            raise KeyError(f"未能获得物料[{self._pending_file_model.brand_category}/{self._pending_file_model.brand_subcategory}/{material_code}]报关单价")

        return self._sales_prices[self._pending_file_model.brand_subcategory_path][material_code]

    def _load_sales_prices(self):
        """
        加载销售价目表
        """
        self._sales_prices[self._pending_file_model.brand_subcategory_path] = {}
        with Utils.open_workbook(self._pending_file_model.get_sales_price_table_file_path(), data_only=True) as workbook:
            sheet = workbook.worksheets[0]
            for row in sheet.iter_rows(min_row=2):
                if row[1].value and row[3].value and row[4].value:
                    material_code = str(row[1].value).strip()
                    if material_code not in self._sales_prices[self._pending_file_model.brand_subcategory_path]:
                        # 未能获得计算列的值
                        price = Decimal(str(row[3].value).strip()) * (Decimal(1) + Decimal(str(row[4].value).strip()))
                        self._sales_prices[self._pending_file_model.brand_subcategory_path][material_code] = price
