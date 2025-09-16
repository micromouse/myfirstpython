from typing import Dict, Any

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from excel.core.dispatcher import Dispatcher

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
        self._result: Dict[str, Any] = {}

    def parse(self) -> Dict[str, Any]:
        """
        解析Excel
        :return: 解析结果
        """
        current_row_index = 1
        while current_row_index <= self.sheet.max_row:
            next_row_index = current_row_index + 1

            # 处理当前行所有单元格内容
            for cell in self.sheet[current_row_index]:
                # 单元格有内容才处理
                if cell.value is not None:
                    value = str(cell.value).strip()
                    handler = Dispatcher.get_handler(value)
                    if handler:
                        parse_result = handler(self.sheet, cell)
                        self._merge_parse_result(parse_result.result)
                        if parse_result.next_row_index > current_row_index or parse_result.next_row_index == 0:
                            if parse_result.next_row_index > current_row_index:
                                next_row_index = parse_result.next_row_index
                            break

            # 下一个要处理的Excel行
            current_row_index = next_row_index

        return self._result

    def _merge_parse_result(self, this_result: Dict[str, Any]):
        """
        合并当前单元格解析结果
        :param this_result: 当前单元格解析结果
        """
        for key, value in this_result.items():
            if key in self._result:
                raise ValueError(f"重复的Key: {key}")
            self._result[key] = value

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
