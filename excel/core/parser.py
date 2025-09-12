from typing import Dict, Any
from openpyxl.worksheet.worksheet import Worksheet
from excel.core.dispatcher import Dispatcher

class Parser:
    """
    Excel解析器
    """

    def __init__(self, sheet: Worksheet):
        """
        初始化Excel解析器
        :param sheet: 要解析的Excel Worksheet
        """
        self.sheet = sheet
        self.result = Dict[str, Any]

    def parse(self):
        """
        解析Excel
        :return:
        """
        current_row_index = 1
        max_row_index = self.sheet.max_row
        while current_row_index <= max_row_index:
            next_row_index = current_row_index + 1

            # 处理当前行所有单元格内容
            for cell in self.sheet[current_row_index]:
                if cell.value is not None:
                    value = str(cell.value).strip()
                    handler = Dispatcher.get_handler(value)
                    if not handler:
                        parse_result = handler(self.sheet, cell)
                        self.merge_parse_result(parse_result.result)
                        if parse_result.next_row_index > current_row_index or parse_result.next_row_index == 0:
                            if parse_result.next_row_index > current_row_index:
                                next_row_index = parse_result.next_row_index
                            break

            # 下一个要处理的Excel行
            current_row_index = next_row_index

    def merge_parse_result(self, this_result: Dict[str, Any]):
        """
        合并当前单元格解析结果
        :param this_result: 当前单元格解析结果
        """
        for key, value in this_result.items():
            if key in self.result:
                raise ValueError(f"重复的Key: {key}")
            self.result[key] = value
