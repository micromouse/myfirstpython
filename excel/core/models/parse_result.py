from dataclasses import dataclass, field
from typing import Dict, Any, TypedDict, List, TypeVar

from .purchase_detail import CI00PurchaseDetail, PL10PurchaseDetail

"""
@dataclass 是 Python 3.7+ 引入的一个装饰器，用于 简化类的定义，自动生成一些常用方法，比如：
__init__() 构造函数
__repr__() 可读的字符串表示
__eq__() 比较对象是否相等
还可以生成 __hash__() 等
"""

@dataclass
class CellparseResult:
    """
    单元格内容解析结果
    """
    result: Dict[str, Any] = field(default_factory=dict)
    next_row_index: int = 0

    def __post_init__(self):
        """
        初始化钩子方法，在 __init__ 方法执行完、字段已经被赋值之后自动调用。
        result属性设置为None值时自动更新为{}
        """
        if self.result is None:
            self.result = {}

class SheetParseResult(TypedDict):
    """
    Excel Sheet解析结果
    """

class ReadParseResult(SheetParseResult):
    """
    读取Excel Sheet解析结果基类
    """
    filename: str
    invoice_type: str
    invoice_date: str
    invoice_number: str

class PL10ReadParseResult(ReadParseResult):
    """
    读取PL10 Sheet解析结果
    """
    purchase_details: List[PL10PurchaseDetail]
    total_gross_weight: float
    total_net_weight: float
    total_packages: int
    total_quantity: int
    total_measurement: float

class CI00ReadParseResult(ReadParseResult):
    """
    读取CI00 Sheet解析结果
    """
    purchase_details: List[CI00PurchaseDetail]
    total_quantity: int
    total_amount: int
    total_amount_english: str

class WriteParseResult(SheetParseResult):
    """
    写入Excel Sheet解析结果
    """
    invoice_number: str
