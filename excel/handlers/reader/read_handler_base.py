from injector import inject

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

class ReadhandleBase:
    """
    读Excel处理器基类
    """

    @inject
    def __init__(self, workbook: Workbook, worksheet: Worksheet):
        """
        初始化读Excel处理器基类
        :param workbook: 要读取的Excel Workbook
        :param worksheet: 要读取的Excel Worksheet
        """
        self._workbook = workbook
        self._worksheet = worksheet
