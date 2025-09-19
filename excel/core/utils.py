from typing import Dict, Any

from excel.core.utils_config import UtilsConfig
from excel.core.utils_currency_formatter import UtilsCurrencyFormatter
from excel.core.utils_excel import UtilsExcel

class Utils(UtilsCurrencyFormatter, UtilsExcel, UtilsConfig):
    """
    excel工具
    """

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
