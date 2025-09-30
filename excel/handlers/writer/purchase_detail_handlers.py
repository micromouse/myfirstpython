from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.writer.write_handler_base import WriteHandlerBase

class WritePurchasedetailHandlers(WriteHandlerBase):
    """
    采购明细处理器
    """

    def __init__(self, workbook: Workbook, worksheet: Worksheet, datasource: WriterDataSource):
        """
        初始化Excel内容写处理器基类
        :param workbook: 要写入的Workbook
        :param worksheet: 要写入的Worksheet
        :param datasource: Excel写入器数据源
        """
        super().__init__(workbook, worksheet, datasource)

    def _insert_blank_rows(self, worksheet: Worksheet, index: int, count: int):
        """
        插入空白行
        :param worksheet: Excel Worksheet
        :param index: 插入行索引(在索引位置前插入空白行)
        :param count: 行数
        """
        worksheet.delete_rows(index, 1)
        worksheet.insert_rows(index, count)

        # 重置新插入行的行高
        for row_index in range(index, index + count + 5):
            worksheet.row_dimensions[row_index].height = None

        return self
