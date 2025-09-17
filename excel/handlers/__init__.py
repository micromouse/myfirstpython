import importlib
import pkgutil
from types import ModuleType
from typing import Union

def import_submodules(package: Union[str | ModuleType], recursive=True):
    """
    递归导入包中的所有子模块和子包
    :param package: 包名或模块对象
    :param recursive: 是否递归导入子包
    """
    if isinstance(package, str):
        package = importlib.import_module(package)

    # 导入当前包下的所有模块
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")

        # 如果是子包且需要递归，就继续导入子包中的内容
        if recursive and is_pkg:
            import_submodules(module)

# 从当前包开始递归导入所有子模块和子包
import_submodules(__name__)
