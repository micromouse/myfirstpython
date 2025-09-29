from injector import inject
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.handlers.models.writer_datasource import WriterDataSource

class WriteHandlerBase:
    """
    Excel内容写处理器基类
    """

    @inject
    def __init__(self, workbook: Workbook, worksheet: Worksheet, datasource: WriterDataSource):
        """
        初始化Excel内容写处理器基类
        :param workbook: 要写入的Workbook
        :param worksheet: 要写入的Worksheet
        :param datasource: Excel写入器数据源
        """
        self._workbook = workbook
        self._worksheet = worksheet
        self._datasource = datasource
