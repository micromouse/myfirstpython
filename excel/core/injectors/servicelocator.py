from typing import Type, TypeVar

import injector
from black import Optional

from excel.core.injectors.iterationscope import IterationScope

T = TypeVar("T")

class ServiceLocator:
    """
    服务定位器
    """
    _injector: injector.Injector = None
    _iteration_scope: IterationScope = None

    @classmethod
    def initial(cls, *modules: injector.Module) -> type["ServiceLocator"]:
        if cls._injector is not None:
            raise AttributeError("服务定位器已初始化")
        cls._injector = injector.Injector(modules)
        cls._iteration_scope = IterationScope(cls._injector)
        cls._injector.binder.bind(IterationScope, to=cls._iteration_scope)
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

    @classmethod
    def get_iteration_scope(cls) -> IterationScope:
        """
        获得迭代范围
        :return: 迭代范围
        """
        return cls._iteration_scope
