from typing import Dict, Any

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.Utils import Utils
from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_type import ParseType
import excel.core.Utils

class Parser:
    """
    Excel解析器
    """

    @classmethod
    def from_file(cls, filename: str, sheet_name: str) -> "Parser":
        """
        从文件加载Excel解析器
        :param filename: 文件名
        :param sheet_name: sheet名
        :return: Parser实例
        """
        workbook = load_workbook(filename)
        if sheet_name not in workbook:
            raise ValueError(f"Sheet [{filename} - {sheet_name}] 不存在")
        return cls(workbook[sheet_name], workbook)

    def __init__(self, sheet: Worksheet, workbook: Workbook = None):
        """
        初始化Excel解析器
        :param sheet: 要解析的Excel Worksheet
        """
        self.sheet = sheet
        self.workbook = workbook

    def save(self, filename: str):
        """
        保存Workbook
        :param filename: 文件名
        """
        self.workbook.save(filename)

    def parse(self, type: ParseType) -> Dict[str, Any]:
        """
        解析Excel
        :return: 解析结果
        """
        final_result: Dict[str, Any] = {}

        # 循环整个Sheet
        current_row_index = 1
        while current_row_index <= self.sheet.max_row:
            next_row_index = current_row_index + 1

            # 处理当前行所有单元格内容
            for cell in self.sheet[current_row_index]:
                # 单元格有内容才处理
                if cell.value is not None:
                    value = Utils.get_cell_value(self.sheet, cell)
                    handler = Dispatcher.get_handler(f"{type}{value}")

                    # 需要处理单元格内容时才处理
                    if handler:
                        handle_result = handler(self.sheet, cell)
                        Utils.merge_parse_result(final_result, handle_result.result)
                        if handle_result.next_row_index > current_row_index:
                            next_row_index = handle_result.next_row_index
                            break
                        elif handle_result.next_row_index == 0:
                            break

            # 下一个要处理的Excel行
            current_row_index = next_row_index

        return final_result

    def __enter__(self):
        """
        执行上下文管理
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        支持上下文管理
        """
        if self.workbook:
            self.workbook.close()
