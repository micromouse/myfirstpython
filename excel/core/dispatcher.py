from typing import Callable, Dict
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from excel.core.models.cell_parse_result import CellparseResult

class Dispatcher:
    """
    分发器,自动注册关键字处理器函数
    """
    _handlers: Dict[str, Callable[[Worksheet, Cell], CellparseResult]] = {}

    @classmethod
    def regiter_handler(cls, keyword: str) -> Callable:
        """
        注册关键字处理器
        :param keyword: 关键字
        :return: 处理器函数装饰器
        """

        def decorator(func: Callable[[Worksheet, Cell], CellparseResult]):
            """
            装饰器:把处理器函数分发到分发表
            :param func: 处理器函数
            :return: 处理器函数
            """
            if keyword in cls._handlers:
                raise ValueError(f"关键字 '{keyword}' 已经被注册过了")
            cls._handlers[keyword] = func
            return func

        return decorator

    @classmethod
    def get_handler(cls, keyword: str) -> Callable[[Worksheet, Cell], CellparseResult] | None:
        """
        获得指定关键字的处理器函数
        :param keyword: 关键字
        :return: 关键字处理器函数
        """
        return cls._handlers.get(keyword) if keyword else None
