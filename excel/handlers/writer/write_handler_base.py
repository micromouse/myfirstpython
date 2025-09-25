from injector import inject

from excel.handlers.writer.writer_datasource import WriterDataSource

class WriteHandlerBase:
    """
    Excel内容写处理器基类
    """

    @inject
    def __init__(self, datasource: WriterDataSource):
        """
        初始化Excel内容写处理器基类
        :param datasource: Excel写入器数据源
        """
        self._datasource = datasource
