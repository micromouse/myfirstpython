from dataclasses import dataclass

@dataclass(frozen=True)
class AppSettings:
    """
    应用程序配置
    """
    registered_invoice_number_file: str
    """
    已注册发票号文件
    """
    hscode_file: str
    """
    整合订舱明细HS CODE文件
    """
    battry_brand_file: str
    """
    电池品牌信息文件
    """
    oppo_phone_model_authentication_file: str
    """
    oppo手机型号认证表文件
    """
    realme_phone_model_authentication_file: str
    """
    realme手机型号认证表文件
    """
