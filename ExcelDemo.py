"""
使用xlwings控制excel演示
"""
import xlwings
from pathlib import Path

class ExcelDemo:
    """
    Excel演示类
    """

    @staticmethod
    def create_excel(file: str):
        """
        建立excel文件
        :param file: 文件名
        """
        # 自动建立目录
        ExcelDemo.__create_folder(file)

        # 创建excel文件
        with xlwings.App(visible=False) as app:
            with app.books.add() as book:
                sheet = book.sheets[0]

                # 写入内容
                sheet.range("A1").value = "姓名"
                sheet.range("B1").value = "年龄"
                sheet.range("A2").value = "张三"
                sheet.range("B2").value = 20

                # 保存文件
                book.save(file)

    @staticmethod
    def __create_folder(file: str):
        path = Path(file)

        # 文件存在抛出文件存在异常
        if path.exists() and path.is_file():
            raise FileExistsError(f"文件[{file}]已存在")

        # 目录不存在自动创建目录
        # parents=True 表示创建所有父目录，exist_ok=True 表示目录已存在也不会报错
        path.parent.mkdir(parents=True, exist_ok=True)
