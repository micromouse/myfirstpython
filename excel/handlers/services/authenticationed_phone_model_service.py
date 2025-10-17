from typing import Dict, List

from injector import inject

from excel.appsettings import AppSettings
from excel.core.utils import Utils

class AuthenticationedPhonemodelService:
    """
    已认证手机型号服务
    """
    PHONEMODEL_OPPO = "OPPO"
    PHONEMODEL_REALME = "REALME"
    _factory_codes: Dict[str, List[str]] = {}
    _oppo_factorycode_index: int = -1
    _realme_factorycode_index: int = -1

    @inject
    def __init__(self, appsettings: AppSettings):
        """
        初始化已认证手机型号服务
        :param appsettings: 应用程序配置
        """
        self._appsettings = appsettings
        if not self._factory_codes:
            self._load_authenticationed_phonemodel_factorycodes()

    def to_first(self, brand_category: str) -> "AuthenticationedPhonemodelService":
        """
        设置当前手机型号工厂编码索引为第一个索引位置
        :param brand_category: 品牌大类
        :return: 已认证手机型号服务
        """
        if brand_category.startswith(self.PHONEMODEL_OPPO):
            AuthenticationedPhonemodelService._oppo_factorycode_index = -1
        elif brand_category.startswith(self.PHONEMODEL_REALME):
            AuthenticationedPhonemodelService._realme_factorycode_index = -1
        else:
            raise RuntimeError(f"当前手机型号[{brand_category}]不是[OPPO,REALME]之一")

        return self

    def get_next_factorycode(self, brand_category: str) -> str:
        """
        获得指定品牌类别下一个已认证手机型号工厂编码
        :param brand_category: 品牌大类
        :return: 下一个已认证手机型号工厂编码
        """
        if brand_category.startswith(self.PHONEMODEL_OPPO):
            if self._oppo_factorycode_index + 1 >= len(self._factory_codes[self.PHONEMODEL_OPPO]):
                self.to_first(brand_category)
            AuthenticationedPhonemodelService._oppo_factorycode_index += 1
            return self._factory_codes[self.PHONEMODEL_OPPO][self._oppo_factorycode_index]
        elif brand_category.startswith(self.PHONEMODEL_REALME):
            if self._realme_factorycode_index + 1 >= len(self._factory_codes[self.PHONEMODEL_REALME]):
                self.to_first(brand_category)
            AuthenticationedPhonemodelService._realme_factorycode_index += 1
            return self._factory_codes[self.PHONEMODEL_REALME][self._realme_factorycode_index]
        else:
            raise RuntimeError(f"当前手机型号[{brand_category}]不是[OPPO,REALME]之一")

    def _load_authenticationed_phonemodel_factorycodes(self):
        """
        加载已认证手机型号工厂编码
        """
        self._factory_codes[self.PHONEMODEL_OPPO] = self._get_factory_codes(self._appsettings.oppo_phone_model_authentication_file)
        self._factory_codes[self.PHONEMODEL_REALME] = self._get_factory_codes(self._appsettings.realme_phone_model_authentication_file)

    @classmethod
    def _get_factory_codes(cls, file: str) -> List[str]:
        """
        获得指定文件已认证手机型号工厂编码集合
        :param file: 包含已认证手机型号工厂编码集合文件
        :return: 已认证手机型号工厂编码集合
        """
        factory_codes: List[str] = []

        workbook, worksheet = Utils.load_worksheet(file, sheet_index=0)
        try:
            for row in worksheet.iter_rows(min_row=2):
                if row[1].value:
                    factory_code = str(row[1].value).strip()
                    if factory_code not in factory_codes:
                        factory_codes.append(factory_code)

            return factory_codes
        finally:
            workbook.close()
