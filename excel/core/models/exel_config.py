from typing import TypedDict, Literal

class ExcelConfig(TypedDict, total=False):
    """
    Excel配置信息
    """
    registered_invoice_number_file: str
    hscode_file: str

# Literal 是 Python 3.8+ 引入的类型提示工具（typing.Literal）
# 它的作用是：限制某个变量的值只能是给定的常量之一。
ConfigKey = Literal["registered_invoice_number_file", "hscode_file"]
