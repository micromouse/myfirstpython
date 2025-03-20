import importlib
import os

from fastapi import FastAPI

from FastApi.FastApiBase import FastApiBase

class RouterRegistrar:
    """
    路由注册器
    """

    def __init__(self, app: FastAPI, apiDirectory: str):
        """
        初始化路由注册器
        :param app: FastAPI
        :param apiDirectory: api目录
        """
        self.app = app
        self.__api_module_directory = apiDirectory

    def registerRouters(self):
        """
        注册路由
        """
        for fileName in os.listdir(self.__api_module_directory):
            if fileName != "__init__.py" and fileName.endswith(".py"):
                moduleName = f"FastApi.{fileName[:-3]}"
                module = importlib.import_module(moduleName)

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
