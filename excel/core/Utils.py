from typing import Dict, Any
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

class Utils:
    """
    excel工具
    """

    @staticmethod
    def get_cell_value(sheet: Worksheet, cell: Cell, default: str = "") -> str:
        """
        获得单元格的值,如果是合并单元格取起始位置的值
        :param sheet: Worksheet
        :param cell: 要获取值的单元格
        :param default: 默认值,缺省为空字符串
        :return: 单元格值
        """
        value = default

        # 单元格有值
        if cell.value is not None:
            value = str(cell.value)
        else:
            # 单元格无值看是否在合并单元格中
            for merged_range in sheet.merged_cells.ranges:
                if (merged_range.min_row <= cell.row <= merged_range.max_row and
                        merged_range.min_col <= cell.column <= merged_range.max_col):
                    value = str(sheet.cell(merged_range.min_row, merged_range.min_col).value)

        # 单元格无值且不在合并单元格中
        return value.strip()

    @staticmethod
    def merge_parse_result(to_result: Dict[str, Any], this_result: Dict[str, Any]):
        """
        合并当前单元格解析结果
        :param to_result: 需要合并到的结果词典
        :param this_result: 当前单元格解析结果
        """
        for key, value in this_result.items():
            if key in to_result:
                raise ValueError(f"重复的Key: {key}")

            to_result[key] = value
