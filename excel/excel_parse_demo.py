from os import path
from typing import Dict

from core.parser import Parser
from core.models.parse_type import ParseType
from excel import handlers
from excel.core.models.parse_result import CI00ReadParseResult
from excel.core.utils import Utils
from excel.handlers.common.application_manager import ApplicationManager
from excel.handlers.common.appsettings import AppSettings
from excel.handlers.writer.write_handler_base import WriteHandlerBase

appsettings = AppSettings(
    registered_invoice_number_file=r"D:\Shadowbot\埃及-自动化开票流程-更新\整合发票号登记表.xlsx",
    hscode_file="b",
    battry_brand_file="c",
    oppo_phone_model_authentication_file="d",
    realme_phone_model_authentication_file="e")
ApplicationManager.init_appsettings(appsettings)

# 读取 采购CI00 Sheet
root_folder = r"D:\Shadowbot\埃及-自动化开票流程-更新"
folder = r"收货方：OPPO Egypt manufacturing\OPPO品牌\电池\7.15采购CI&PL"
file = path.join(root_folder, folder, "0821_电池CIPL_HKNE25082001_S2025082000999F_OPPO A5 电池 5K&6K&12K&2040&5040.xlsx")
with Parser(file, "CI00") as parser_read:
    read_ci00_result: CI00ReadParseResult = parser_read.parse(ParseType.READ, CI00ReadParseResult)
    read_ci00_result["filename"] = file
    read_ci00_result["invoice_type"] = "电池"

# 写入清关CI00 Sheet
WriteHandlerBase.set_data_source(read_ci00_result)
write_file = path.join(root_folder, r"收货方：OPPO Egypt manufacturing\OPPO品牌\电池\销售CI&PL模板.xlsx")
with Parser(write_file, "货代 Invoice") as parser_write:
    parser_write.parse(ParseType.WRITE, CI00ReadParseResult)
    parser_write.save(path.join(root_folder, "my.xlsx"))

print("done")
