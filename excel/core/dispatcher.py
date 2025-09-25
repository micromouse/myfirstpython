import inspect
from typing import Callable, Dict

from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.models.parse_result import CellparseResult
from excel.core.servicelocator import ServiceLocator

class Dispatcher:
    """
    分发器,自动注册关键字处理器函数
    """
    _handlers: Dict[str, Callable[[Worksheet, Cell], CellparseResult]] = {}

    @classmethod
    def regiter_handler(cls, keyword: str, owner_cls: type = None) -> Callable:
        """
        注册关键字处理器
        :param owner_cls: 类函数所在类类型
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

            parameters = list(inspect.signature(func).parameters.keys())
            if parameters[0] == "cls":
                cls._handlers[keyword] = lambda sheet, cell: func.__func__(owner_cls, sheet, cell)
            elif parameters[0] == "self":
                cls._handlers[keyword] = lambda sheet, cell: func.__get__(ServiceLocator.getservice(owner_cls))(sheet, cell)
            else:
                cls._handlers[keyword] = func

            return func

        return decorator

    @classmethod
    def register_handlers(cls, target_cls: type) -> type:
        """
        注册目标类中的所有处理器
        :param target_cls: 目标类
        :return: 目标类
        """
        for name, method in target_cls.__dict__.items():
            func = getattr(method, "__func__", method)
            keyword = getattr(func, "_keyword", None)
            if keyword:
                cls.regiter_handler(keyword, target_cls)(method)

        return target_cls

    @classmethod
    def keyword(cls, keyword: str):
        def decorator(func):
            func._keyword = keyword
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
