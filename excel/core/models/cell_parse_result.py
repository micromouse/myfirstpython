from dataclasses import dataclass, field
from typing import Dict, Any

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
