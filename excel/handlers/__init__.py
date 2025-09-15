import importlib
import pkgutil

# 自动加载当前包下所有模块（__path__ 代表当前包路径）
for _, module_name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_name}")
