import importlib
import pkgutil

from fastapi import FastAPI

from FastApi.FastApiBase import FastApiBase

class RouterRegistrar:
    """
    路由注册器
    """

    def __init__(self, app: FastAPI, package: str = "FastApi"):
        """
        初始化路由注册器
        :param app: FastAPI
        :param package: 动态路由包名
        """
        self.app = app
        self.__package = package

    def registerRouters(self):
        """
        注册路由
        """
        package = importlib.import_module(self.__package)
        """
        pkgutil.iter_modules
        这个函数用于获取指定包路径下的所有子模块信息，非常适合动态发现和加载模块。        
        当一个Python包被导入后，它会有一个 __path__ 属性，这是一个列表，包含了这个包的所有子模块所在的目录路径                
        package.__name__ 是包的名称，例如 'FastApi'
        加上 '.' 变成 'FastApi.', 这个前缀会被添加到找到的每个子模块名称前面      
        """
        for module_info in pkgutil.iter_modules(package.__path__, f"{package.__name__}."):
            if not module_info.name.endswith('__init__'):
                module = importlib.import_module(module_info.name)
                self.__register_module_routers(module)

    """
        使用 pkgutil.iter_modules() 替代 resources.files().iterdir() 确实是一个更好的选择，因为：        
        它直接处理Python模块而不是文件系统路径，更符合Python的模块导入系统
        它在普通Python环境和PyInstaller打包环境中都能正常工作
        不需要额外的环境检测逻辑，代码更简洁    
        for file in resources.files(package).iterdir():
            if file.suffix == ".py" and file.name != "__init__.py":
                # 使用模块名加载模块
                module_name = f"{self.__package}.{file.stem}"
                module = importlib.import_module(module_name)
    """

    def __register_module_routers(self, module):
        """
        注册模块中的路由
        :param module: 包含路由的模块
        """
        # 遍历模块中的所有类
        # dir(module)：获取module(动态导入的Python模块)中的所有属性名称(类、函数、变量等)
        for name in dir(module):
            value = getattr(module, name)

            # isinstance(value, type): 确保value是一个类，而不是普通变量或函数。
            # 加载FastApi.FastApiBase子类中的API路由器
            if isinstance(value, type) and issubclass(value, FastApiBase) and value is not FastApiBase:
                if hasattr(value, "router"):
                    # 使用FastApiBase子类router类属性
                    self.app.include_router(value.router)
                else:
                    # 使用FastApiBase子类router实例属性
                    instance = value()
                    self.app.include_router(instance.router)
