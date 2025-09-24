from typing import Type

from excel.core.class_property import ClassProperty
from excel.handlers.common.appsettings import AppSettings

class ApplicationManager:
    """
    应用程序管理器
    """
    _appsettings: AppSettings = None

    @classmethod
    def init_appsettings(cls, appsettings: AppSettings):
        if cls._appsettings is not None:
            raise AttributeError("appsettings 已经初始化，不能再次赋值")
        cls._appsettings = appsettings

    # noinspection PyMethodParameters
    @ClassProperty[AppSettings]
    def appsettings(cls) -> AppSettings:
        """
        获得应用程序设置
        :return: 应用程序设置
        """
        return cls._appsettings
