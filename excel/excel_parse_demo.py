from os import path
from typing import Dict

from core.parser import Parser
from core.models.parse_type import ParseType
from excel import handlers
from excel.core.models.parse_result import CI00ParseResult
from excel.core.utils import Utils
from excel.handlers.writer.write_handler_base import WriteHandlerBase

# 读取 采购CI00 Sheet
read_ci00_result: Dict[str, any]
folder = r"D:\Shadowbot\埃及-自动化开票流程-更新\收货方：OPPO Egypt manufacturing\OPPO品牌\电池\7.15采购CI&PL"
file = path.join(folder, "0821_电池CIPL_HKNE25082001_S2025082000999F_OPPO A5 电池 5K&6K&12K&2040&5040.xlsx")
with Parser.from_file(file, "CI00") as parser_read:
    read_ci00_result = parser_read.parse(ParseType.READ, CI00ParseResult)

# 写入清关CI00 Sheet
Utils \
    .init_config("registered_invoice_number_file", "registered.xlsx") \
    .init_config("hscode_file", "hscode.xls")
WriteHandlerBase.set_data_source(read_ci00_result)
write_file = r"D:\Shadowbot\埃及-自动化开票流程-更新\收货方：OPPO Egypt manufacturing\OPPO品牌\电池\销售CI&PL模板.xlsx"
with Parser.from_file(write_file, "货代 Invoice") as parser_write:
    parser_write.parse(ParseType.WRITE, CI00ParseResult)
    pass
