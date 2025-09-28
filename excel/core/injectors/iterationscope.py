from contextvars import ContextVar
from typing import Optional, Dict, Type, Tuple, Any

from injector import Scope, Injector, InstanceProvider, UnsatisfiedRequirement

class IterationScope(Scope):
    """
    自定义的迭代作用域，支持为任意类型绑定指定实例。
    使用方法：
        scope = IterationScope(injector)
        with scope.enter((PendingFileModel, pending_file)):
            ...
        或：
        with scope.enter((TypeA, instance_a), (TypeB, instance_b)):
            ...
    """

    # 每个线程/协程都有自己的作用域上下文
    _context: ContextVar[Optional[Dict[Type, InstanceProvider]]] = ContextVar(
        "iteration_scope_context", default=None
    )

    def __init__(self, injector: Injector):
        """
        初始化 IterationScope
        :param injector: injector.Injector 实例，提供依赖注入能力
        """
        super().__init__(injector)

    def enter(self, *bindings: Tuple[Type, Any]) -> "IterationScope":
        """
        进入一个新的作用域，绑定指定类型与实例。
        :param bindings: 类型与实例的元组，例如 (PendingFileModel, pending_file)
        :return: self
        """
        ctx = {}
        for typ, inst in bindings:
            ctx[typ] = InstanceProvider(inst)
        self._context.set(ctx)
        return self

    def __enter__(self) -> "IterationScope":
        """
        上下文进入时返回自身
        :return: IterationScope
        """
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """
        退出当前作用域，清空上下文。
        """
        self._context = None

    def get(self, key: Type, provider) -> object:
        """
        获取当前作用域中的绑定实例。
        :param key: 要获取的类型
        :param provider: provider，用于生成实例
        :return: 实例对象
        :raises UnsatisfiedRequirement: 如果当前上下文不存在
        """
        context = self._context.get()
        if context is None:
            raise UnsatisfiedRequirement(None, key)

        # 如果实例尚未创建，则通过 provider 创建
        if key not in context:
            instance = provider.get(self.injector)
            context[key] = InstanceProvider(instance)

        return context[key]
