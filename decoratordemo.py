import warnings
import functools

from typing import Any, Callable

def deprecated(message: str) -> Callable[..., Any]:
    """
    自定义弃用装饰器，用于标记某个函数为弃用状态，并在调用时发出警告
    :param message: 弃用消息
    :return: 一个装饰器，用于包装被标记弃用的函数
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        装饰器，用于包装目标函数，在调用时发出弃用警告
        :param func: 要执行的函数
        :return: 包装后的函数
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            包装器,在调用被包装函数时发出弃用警告
            :param args: 传递给被装饰函数的位置参数
            :param kwargs: 传递给被装饰函数的关键字参数
            :return: 被装饰函数的返回值
            """
            warnings.warn(
                message=f"{func.__name__} is deprecated and will be removed in future versions.\n{message}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator

@deprecated("Use `new_function` instread")
def old_function(x: int, y: int) -> int:
    return x + y

def new_function(x: int, y: int) -> int:
    return x + y

result = old_function(2, 3)
print(f"Result by old_function: {result}")
print(f"Result by new_function: {new_function(2, 3)}")
