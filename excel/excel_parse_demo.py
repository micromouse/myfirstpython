import json
from os import path

from core.parser import Parser
import handlers

folder = r"D:\Shadowbot\埃及-自动化开票流程-更新\收货方：OPPO Egypt manufacturing\OPPO品牌\电池\7.15采购CI&PL"
file = path.join(folder, "0821_电池CIPL_HKNE25082001_S2025082000999F_OPPO A5 电池 5K&6K&12K&2040&5040.xlsx")
with Parser.from_file(file, "CI00") as parser:
    result = parser.parse()
    print(json.dumps(result, default=lambda x: float(x), indent=2))
