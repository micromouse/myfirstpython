from PersonInfo import PersonInfo
from typing import List

def add(a, b):
    print(f"即将输出a+b的值：\na={a}, b={b}")
    return a + b

if __name__ == "__main__":
    print("hello", end=" ")
    print("world", end=" ")
    print("!")

# 定义一个函数add(a,b)，返回两个数的和
_sum = add(2, 3)
print(f"2 + 3 = {_sum}")

# 使用for循环打印1到10
print("即将打印1到10：")
for i in range(10):
    print(f"{i}", end=" ")

# 创建字典存储姓名和年龄并打印
person = {
    "name": "张三",
    "age": 20
}
print(f"\n我的身份信息：{person}, 姓名 = {person['name']}, 年龄 = {person['age']}")
print("我的身份信息：{}, 姓名 = {}, 年龄 = {}".format(person, person["name"], person["age"]))

# PersonInfo Class
p1 = PersonInfo("李四")
p2 = PersonInfo("张三", age=20)
p3 = PersonInfo("王五", 30)
p2.city = "成都"
p3.city = "绵阳"
p1.greet()
p2.greet()
p3.greet()

# 使用类名调用类方法
PersonInfo.set_species("外星人")

# 使用类方法创建PersonInfo实例
p4 = PersonInfo.create_person({"name": "赵二", "age": 30})
print("使用PersonInfo.create_person创建了PersonInfo实例：", end=" ")
p4.greet()

# 使用类方法创建PersonInfo实例，错误使用：字典缺少 'name' 或 'age'
try:
    p5 = PersonInfo.create_person({"name": "赵二"})
except ValueError as e:
    print(f"错误：{e}")

print(f"名称'李四'是有效的:{PersonInfo.is_valid_name('李四')}")
print(f"名称''是无效的:{PersonInfo.is_valid_name('')}")

# 使用类名调用类方法
print(f"20岁算成年吗：{PersonInfo.is_audit(20)}")

def find_excel_files(root_dir):
    """
    获得根目录下的所有excel文件
    :param root_dir: 根目录
    :return: excel文件集合
    """
    excel_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(('.xls', '.xlsx', '.xlsm')):
                excel_files.append(os.path.join(dirpath, filename))
    return excel_files
