from typing import Dict, Any, TypeVar, Type

from injector import inject
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import SheetParseResult
from excel.core.models.parse_type import ParseType
from excel.core.utils import Utils

class Parser:
    """
    Excel解析器
    """
    TParseResult = TypeVar("TParseResult", bound=SheetParseResult)

    @inject
    def __init__(self, workbook: Workbook, worksheet: Worksheet):
        """
        初始化Excel解析器
        :param workbook: Excel Workbook
        :param worksheet: Excel Worksheet
        """
        self._workbook = workbook
        self._worksheet = worksheet

    def save(self, filename: str):
        """
        保存Workbook
        :param filename: 文件名
        """
        self._workbook.save(filename)

    def parse(self, type: ParseType, result_type: Type[TParseResult]) -> TParseResult:
        """
        解析Excel
        :return: 解析结果
        """
        final_result: Dict[str, Any] = {}

        # 循环整个Sheet
        current_row_index = 1
        while current_row_index <= self._worksheet.max_row:
            next_row_index = current_row_index + 1

            # 处理当前行所有单元格内容
            for cell in self._worksheet[current_row_index]:
                # 单元格有内容才处理
                if cell.value is not None:
                    value = Utils.get_cell_value(self._worksheet, cell)
                    handler = Dispatcher.get_handler(f"{type}{value}")

                    # 需要处理单元格内容时才处理
                    if handler:
                        handle_result = handler(cell)
                        Utils.merge_parse_result(final_result, handle_result.result)
                        if handle_result.next_row_index > current_row_index:
                            next_row_index = handle_result.next_row_index
                            break
                        elif handle_result.next_row_index == 0:
                            break

            # 下一个要处理的Excel行
            current_row_index = next_row_index

        return result_type(**final_result)

    def __enter__(self):
        """
        执行上下文管理
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        支持上下文管理
        """
        if self._workbook:
            self._workbook.close()
