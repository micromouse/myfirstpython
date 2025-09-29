import inspect
from typing import Callable, Dict

from openpyxl.cell.cell import Cell

from excel.core.injectors.servicelocator import ServiceLocator
from excel.core.models.parse_result import CellparseResult

class Dispatcher:
    """
    分发器,自动注册关键字处理器函数
    """
    _handlers: Dict[str, Callable[[Cell], CellparseResult]] = {}

    @classmethod
    def regiter_handler(cls, keyword: str, owner_cls: type = None) -> Callable:
        """
        注册关键字处理器
        :param owner_cls: 类函数所在类类型
        :param keyword: 关键字
        :return: 处理器函数装饰器
        """

        def decorator(func: Callable[[Cell], CellparseResult]):
            """
            装饰器:把处理器函数分发到分发表
            :param func: 处理器函数
            :return: 处理器函数
            """
            _keyword = keyword.upper()
            if _keyword in cls._handlers:
                raise ValueError(f"关键字 '{_keyword}' 已经被注册过了")

            parameters = list(inspect.signature(func).parameters.keys())
            if parameters[0] == "cls":
                cls._handlers[_keyword] = lambda cell: func.__func__(owner_cls, cell)
            elif parameters[0] == "self":
                cls._handlers[_keyword] = lambda cell: func.__get__(ServiceLocator.getservice(owner_cls))(cell)
            else:
                cls._handlers[_keyword] = func

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
            func._keyword = keyword.upper()
            return func

        return decorator

    @classmethod
    def get_handler(cls, keyword: str) -> Callable[[Cell], CellparseResult] | None:
        """
        获得指定关键字的处理器函数
        :param keyword: 关键字
        :return: 关键字处理器函数
        """
        return cls._handlers.get(keyword.upper()) if keyword else None
