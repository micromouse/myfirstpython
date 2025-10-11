from typing import Callable, Self

from openpyxl.worksheet.worksheet import Worksheet

from excel.core.models.write_excel_model import WriteExcelModel
from excel.core.utils import Utils

class FluentExcelWriter:
    """
    支持流式调用的Excel写入器
    """

    def __init__(self):
        """
        初始化支持流式调用的Excel写入器
        """
        self._file = ""
        self._sheet_index: int = 0
        self._sheet_name = ""
        self._saveas_file = ""

    def set_file(self, file: str) -> Self:
        """
        设置文件名
        """
        self._file = file
        return self

    def set_sheet_index(self, sheet_index: int) -> Self:
        """
        设置Sheet Index
        """
        self._sheet_index = sheet_index
        return self

    def set_sheet_name(self, sheet_name: str) -> Self:
        """
        设置Sheet名称
        """
        self._sheet_name = sheet_name
        return self

    def set_saveas_file(self, saveas_file: str) -> Self:
        """
        设置另存为文件名
        """
        self._saveas_file = saveas_file
        return self

    def init(self, file: str, sheet_index: int = 0, sheet_name: str = "", saveas_file: str = "") -> Self:
        """
        一次初始化文件、sheet index、sheet名称、另存为文件名
        """
        self._file = file
        self._sheet_index = sheet_index
        self._sheet_name = sheet_name
        self._saveas_file = saveas_file
        return self

    def write(self, func: Callable[[Worksheet], None]):
        """
        回调函数写入实际内容
        """
        model = WriteExcelModel(self._file, self._sheet_index, self._sheet_name, self._saveas_file)
        Utils.write_excel(model, func)
