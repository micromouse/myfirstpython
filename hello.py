from PersonInfo import PersonInfo
from typing import List, Any, Dict

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

def remove_suffix(text: str, suffixs: List[str]):
    """
    删除字符串末尾的子字符串集合
    :param text: 源字符串
    :param suffixs: 要删除的子字符串集合
    :return: 删除所有字符串集合后的字符串
    """
    for suffix in suffixs:
        if text.endswith(suffix):
            """
            text[start:stop]
            start 是起始索引（包含）
            stop 是结束索引（不包含）
            如果不写 start，默认是从开头开始
            如果 stop 是负数，表示“从字符串尾部往前数”            
            """
            text = text[:-len(suffix)].strip()

    return text.strip()

def get_keys(headers: List[Dict[str, str]]) -> List[str]:
    """
    从列头词典列表中获得key集合
    :param headers: 列头词典列表
    :return: key集合
    """
    return [list(header.keys())[0] for header in headers]

def get_column_headers(headers: List[Dict[str, str]]) -> List[str]:
    """
    从列头词典列表中获得列头值集合
    :param headers: 列头词典列表
    :return: 列头值集合
    """
    return [list(header.values())[0] for header in headers]

def extract_values_by_keys(record: Dict[str, str], keys: List[str]) -> List[str]:
    """
    按照指定键列表的顺序，从字典中提取对应的值。
    :param record: 包含多个键值对的字典
    :param keys: 要提取的键列表，按此顺序提取值
    :return: 提取出的值列表，对应于给定的键顺序
    """
    return [record[key] for key in keys]

def find_list(items: List[Dict], name: str) -> Dict:
    matches_item = [item for item in items if item["name"] == name]
    if matches_item:
        return matches_item[0]
    else:
        raise KeyError(f"没有找到当前购买方: {name}")

def throw_inner_exception(item: Any) -> float:
    """
    获得开票金额
    :param item: 开票项
    :return: 开票金额
    """
    try:
        return float(item.children()[6].get_text().replace(",", "").replace(" ", ""))
    except Exception as e:
        raise RuntimeError(f"获得当前项[{item.get_html()}]开票金额时发生错误") from e
