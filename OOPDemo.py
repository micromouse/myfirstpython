# 面向对象概念(继承、多态、封装)演示
from abc import abstractmethod, ABC

class AnimalBase(ABC):
    """
    ABC 代表 Abstract Base Class（抽象基类），它是 abc 模块中的一个类，专门用于定义抽象类。
    Python 提供 ABC 让开发者可以创建不能直接实例化的类，而只能被继承，并要求子类实现特定的方法。
    在 Python 中，我们可以通过 ABC 来创建抽象类，目的是：
        让子类必须实现某些方法，确保代码一致性。
        不能直接实例化抽象类，防止错误使用。
    动物基类
    """

    def __init__(self, name: str, color: str = "none"):
        """
        初始化动物基类
        :param name: 名称
        :param color: 颜色
        """
        self.name = name
        self._color = color

    @property
    def color(self) -> str:
        """
        获得动物颜色
        :return: 动物颜色
        """
        return self._color

    @color.setter
    def color(self, value: str):
        """
        设置动物颜色
        :param value: 动物颜色
        """
        self._color = value

    @abstractmethod
    def speak(self):
        """
        说话(抽象方法),子类必须实现
        """

class DogAnimal(AnimalBase):
    """
    狗
    """

    def speak(self):
        """
        狗说话
        """
        self.__initial_speak()
        print(f"{self.name} says woof")

    def __initial_speak(self):
        """
        私有方法(只能在DogAnimal内部调用),初始化speak
        """
        print(f"initial {self.name} speak")

class CatAnimal(AnimalBase):
    """
    猫
    """

    def __init__(self, name: str, color: str, bread: str):
        """
        初始化猫
        :param name: 名称
        :param color: 颜色
        """
        super().__init__(name, color)
        self._bread = bread

    @property
    def bread(self) -> str:
        """
        获得猫的交配信息
        :return: 猫的交配信息
        """
        return self._bread

    @bread.setter
    def bread(self, value: str):
        """
        设置猫的交配信息
        :param value: 猫的交配信息
        """
        self._bread = value

    def speak(self):
        """
        猫说话
        """
        print(f"{self.name} says Meow，bread is {self.bread}")

def animal_sound(animal: AnimalBase):
    """
    使用多态让不同动物实现说话
    :param animal: 具体动物
    """
    animal.speak()
    print(f"{animal.name}的颜色是{animal.color}")

# 狗说话
dog = DogAnimal("旺财")
dog.speak()

# 猫说话
cat = CatAnimal("咪咪", "none", "公猫")
cat.bread += "2.0"
cat.speak()

# 使用多态让不同动物说话
print("使用多态让不同动物说话")
animal_sound(DogAnimal("阿福", "black"))
animal_sound(CatAnimal("波斯", "yellow", "母猫"))
