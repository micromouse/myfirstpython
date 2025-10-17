from typing import Dict

from injector import inject
from openpyxl.worksheet.worksheet import Worksheet

from excel.appsettings import AppSettings
from excel.core.utils import Utils

class HScodeService:
    """
    订舱明细HS CODE服务
    """
    _hscodes: Dict[str, str] = {}

    @inject
    def __init__(self, appsettings: AppSettings):
        """
        初始化订舱明细HS CODE服务
        :param appsettings: 应用程序配置
        """
        self._appsettings = appsettings
        if not self._hscodes:
            self._load_hscodes()

    def get_hscode(self, material_code: str) -> str:
        """
        由物料编码获得HSCODE
        :param material_code: 物料编码
        :return: HSCODE
        """
        if material_code not in self._hscodes:
            raise KeyError(f"未找到物料编码[{material_code}] HSCODE")
        return self._hscodes[material_code]

    def _load_hscodes(self):
        """
        加载订舱明细HS CODE数据
        """
        with Utils.open_workbook(self._appsettings.hscode_file) as workbook:
            sheet: Worksheet = workbook.worksheets[0]
            for row in sheet.iter_rows(min_row=2):
                if row[0].value and row[1].value:
                    material_code = str(row[0].value).strip()
                    if material_code not in self._hscodes:
                        self._hscodes[material_code] = str(row[1].value).strip()
