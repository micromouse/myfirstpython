from typing import Generic, Type, TypeVar, Callable, Any, Optional, Dict

TResult = TypeVar("TResult")

class ClassProperty(Generic[TResult], property):
    """
    类属性
    """

    def __init__(self, fget: Callable[[Type], TResult]):
        """
        初始化类属性
        :param fget: 被注解的属性
        """
        super().__init__(fget)

    def __get__(self, instance: Optional[Any], owner: Optional[Type] = None) -> TResult:
        """
        拦截属性访问，把无论是类访问还是实例访问都统一转化成“调用类方法”
        :param instance: 如果是通过 实例访问，就是实例对象；如果是通过 类访问，就是 None。
        :param owner: 拥有这个属性的类。即使通过实例访问，也会传入对应的类。
        :return: 类属性值
        """
        # self.fget 就是应用了 ClassProperty 注解的函数
        return self.fget(owner)

class ClassPropertyDemo:
    """
    类属性演示
    """
    _user: Dict[str, Any] = {
        "name": "abc",
        "age": 18
    }

    # noinspection PyMethodParameters
    @ClassProperty
    def user(cls) -> Dict[str, Any]:
        return cls._user

ClassPropertyDemo.user = {"name": "c", "age": 20}
print(ClassPropertyDemo.user["age"])
