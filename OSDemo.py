# os相关方法演示
import os.path

def show_fileinfo():
    """
    显示文件信息
    """
    filePath = os.path.join("./Resources", "NameList.txt")
    print(f"[{filePath}]的绝对路径是：{os.path.abspath(filePath)}")
    print(f"[{filePath}]的文件名是：{os.path.basename(filePath)}")
    print(f"[{filePath}]是否文件名：{os.path.isfile(filePath)}")
    print(f"[{filePath}]是否目录名：{os.path.isdir(filePath)}")

def create_file_or_folder():
    """
    建立文件或目录
    """
    # 建立新目录
    newdir = os.path.join("./Resources", "child1")
    if not os.path.exists(newdir):
        os.mkdir(newdir)

    # 建立新文件
    newfile = os.path.join("./Resources", "newfile.txt")
    if not os.path.exists(newfile):
        with open(newfile, "w"):
            pass

def remove_file_or_folder():
    """
    删除文件或目录
    """
    child1dir = os.path.join("./Resources", "child1")
    if os.path.exists(child1dir):
        os.removedirs(child1dir)

    file = os.path.join("./Resources", "newfile.txt")
    if os.path.exists(file):
        os.remove(file)

def traversal_folder():
    """
    遍历目录
    """
    for root, dirs, files in os.walk("./", topdown=True):
        print(f"当前目录：{root}")
        # 输出所有文件
        for name in files:
            print(f"文件：{os.path.abspath(os.path.join(root, name))}")

        # 输出所有目录名
        for name in dirs:
            print(f"子目录：{os.path.join(root, name)}")

# 显示文件信息
show_fileinfo()

# 建立文件/目录
create_file_or_folder()

# 删除文件/目录
remove_file_or_folder()

# 遍历目录
traversal_folder()
