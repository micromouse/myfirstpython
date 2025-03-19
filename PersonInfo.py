import json

class PersonInfo:
    """
    个人信息类，用于存储和管理个人基本信息。

    :cvar species：表示物种类型
    """
    species: str = "人类"

    def __init__(self, name: str, age: int = 18):
        """
        初始化个人信息
        :param name: 名称
        :param age: 年龄
        """
        self.name = name
        self.age = age
        self.gender = "男"
        self.city = "北京"

    # 打印个人信息(实例方法)
    def greet(self):
        """
        打印人员信息
        """
        _json = json.dumps(self.__dict__, ensure_ascii=False)
        print("你好，我的个人信息是：{}, 姓名 = {}, 年龄= {}".format(_json, self.name, self.age))

    @classmethod
    def set_species(cls, species):
        """
        设置种族类方法
        :param species: 种族
        """
        cls.species = species
        print(f"类变量species值已更新为：{cls.species}")

    @classmethod
    def create_person(cls, p: dict):
        """
        建立人员信息类方法
        :param p: 人员信息词典
        :return: 人员信息
        """
        # 检查字典p中是否包含name和age键
        if "name" not in p or "age" not in p:
            raise ValueError("字典p中必须包含 'name' 和 'age' 键")

        return cls(p["name"], p["age"])

    @staticmethod
    def is_audit(age: int) -> bool:
        """
        是否成年人静态方法
        :param age: 年龄
        :return: 年龄大于18岁返回True，否则返回False
        """
        return age > 18

    @staticmethod
    def is_valid_name(name):
        """
        判断姓名是否有效的静态方法
        :param name: 姓名
        :return: 姓名不为空字符串返回True，否则返回False
        """
        return name != ""
