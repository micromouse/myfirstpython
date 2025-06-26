# 文件演示
import os.path
from collections.abc import Iterable

def create_file():
    """
    建立文件
    :return: 新文件名
    """
    with open("./Resources/NameList.txt", 'w') as file:
        file.writelines(["beijing\n", "shanghai\n", "guangzhou\n"])
    return "./Resources/NameList.txt"

def append_file(filename: str, lines: Iterable[str]):
    """
    向文件追加内容
    :param filename: 文件名
    :param lines: 要追加的内容集合
    """
    with open(filename, 'a') as file:
        file.writelines(lines)

def remove_file(filename: str) -> bool:
    """
    删除文件
    :param filename: 文件名
    :return: 是否成功删除
    """
    # 文件存在，删除文件
    if os.path.exists(filename):
        os.remove(filename)
        return True

    # 文件不存在，删除失败
    return False

# 建立新文件
filename = create_file()
print(f"建立了新文件：{filename}")

# 追加文件内容
append_file("./Resources/append_namelist.txt", ["sichuan\n", "chongqing\n"])
append_file("./Resources/append_namelist.txt", ["guizhou\n", "yunnan\n"])
print("已追加文件[../Resources/append_namelist.txt]内容")
