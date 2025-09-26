from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class AppSettings:
    """
    应用程序配置
    """
    root_folder: str
    """
    根目录
    """
    registered_invoice_number_file: str
    """
    已注册发票号文件
    """
    hscode_file: str
    """
    整合订舱明细HS CODE文件
    """
    battery_brand_file: str
    """
    电池品牌信息文件
    """
    oppo_phone_model_authentication_file: str = None
    """
    oppo手机型号认证表文件
    """
    realme_phone_model_authentication_file: str = None
    """
    realme手机型号认证表文件
    """

class AppSettingsFactory:
    """
    应用程序配置工厂
    """
    FILE_NAMES: Dict[str, str] = {
        "registered_invoice_number_file": "整合发票号登记表.xlsx",
        "hscode_file": "整合订舱明细HS CODE.xlsx",
        "battery_brand_file": "电池BRAND信息.xlsx",
        "oppo_phone_model_authentication_file": "OPPO手机型号认证表.xlsx",
        "realme_phone_model_authentication_file": "REALME手机型号认证表.xlsx",
    }

    @classmethod
    def create(cls, root_folder: str) -> AppSettings:
        """
        建立应用程序配置对象
        :param root_folder: 根目录
        :return: 应用程序配置对象
        """
        root = Path(root_folder)

        settings = {"root_folder": str(root)}
        for field, filename in cls.FILE_NAMES.items():
            file_path = root / filename
            if not file_path.exists():
                raise FileNotFoundError(f"文件[{file_path}]不存在")
            settings[field] = str(file_path)

        return AppSettings(**settings)
