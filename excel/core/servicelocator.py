from typing import Type, TypeVar

import injector
from black import Optional

T = TypeVar("T")

class ServiceLocator:
    """
    服务定位器
    """
    _injector: injector.Injector = None

    @classmethod
    def initial(cls, *modules: injector.Module) -> type["ServiceLocator"]:
        if cls._injector is not None:
            raise AttributeError("服务定位器已初始化")
        cls._injector = injector.Injector(modules)
        return cls

    @classmethod
    def register_service(
            cls,
            interface: Type[T],
            implementation: Type[T],
            scope: Optional[Type[injector.Scope]] = injector.noscope
    ) -> type["ServiceLocator"]:
        """
        注册服务
        :param interface: 接口类型
        :param implementation: 接口实现类型
        :param scope: 范围
        """
        cls._injector.binder.bind(interface, to=implementation, scope=scope)
        return cls

    @classmethod
    def register_instance(cls, instance: T) -> type["ServiceLocator"]:
        cls._injector.binder.bind(type(instance), to=instance)
        return cls

    @classmethod
    def getservice(cls, _type: Type[T]) -> T:
        """
        获得服务
        :param _type: 服务类型
        :return: 服务实例
        """
        return cls._injector.get(_type)
