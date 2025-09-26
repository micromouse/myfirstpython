from typing import Dict

from injector import inject
from openpyxl.worksheet.worksheet import Worksheet

from excel.appsettings import AppSettings
from excel.core.utils import Utils
from excel.handlers.models.battery_brand_model import BatteryBrandModel

class BatteryBrandService:
    """
    电池品牌服务
    """
    _battery_brand_models: Dict[str, BatteryBrandModel] = {}

    @inject
    def __init__(self, appsettings: AppSettings):
        """
        初始化电池品牌服务
        :param appsettings: 应用程序设置
        """
        self._appsettings = appsettings
        if not BatteryBrandService._battery_brand_models:
            self._load_battry_brands()

    def get_battry_brand(self, material_code: str) -> BatteryBrandModel:
        """
        由物料编码获得电池品牌信息模型
        :param material_code: 物料编码
        :return: 电池品牌信息模型
        """
        if material_code not in self._battery_brand_models:
            raise IndexError(f"电池品牌集合中没有当前物料编码[{material_code}]信息")

        return self._battery_brand_models[material_code]

    def _load_battry_brands(self):
        """
        加载电池品牌信息
        """
        with Utils.open_workbook(self._appsettings.battery_brand_file) as workbook:
            sheet: Worksheet = workbook.worksheets[0]
            for row in sheet.iter_rows():
                if row[1].value:
                    material_code = str(row[1].value).strip()
                    if material_code not in self._battery_brand_models:
                        self._battery_brand_models[material_code] = BatteryBrandModel(
                            material_code=material_code,
                            model=str(row[0].value).strip(),
                            description=str(row[2].value).strip(),
                            supplier=str(row[3].value).strip(),
                            brand=str(row[4].value).strip()
                        )
