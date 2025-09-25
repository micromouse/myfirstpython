from typing import TypeVar, Type, overload, Union

from excel.core.models.parse_result import CI00ReadParseResult, PL10ReadParseResult, ReadParseResult

class WriterDataSource:
    """
    Excel写入器数据源
    """
    TParseResult = TypeVar("TParseResult", bound=ReadParseResult)

    def __init__(self, ci00_data: CI00ReadParseResult = None, pl10_data: PL10ReadParseResult = None):
        """
        初始化Excel内容写处理器基类
        :param ci00_data: CI00 Sheet内容读取解析结果
        :param pl10_data: PL10 Sheet内容读取解析结果
        """
        self._ci00_data_source = ci00_data
        self._pl10_data_source = pl10_data

    @overload
    def get_data_source(self, data_type: Type[CI00ReadParseResult]) -> CI00ReadParseResult:
        ...

    @overload
    def get_data_source(self, data_type: Type[PL10ReadParseResult]) -> PL10ReadParseResult:
        ...

    def get_data_source(self, data_type=Type[TParseResult]) -> TParseResult:
        """
        获得写入处理器数据源
        :return: 写入处理器数据源
        """
        if data_type is CI00ReadParseResult:
            return self._ci00_data_source
        elif data_type is PL10ReadParseResult:
            return self._pl10_data_source
        else:
            raise ValueError(f"不支持的数据类型[{data_type}]")

    def get_common_data_source(self) -> Union[CI00ReadParseResult, PL10ReadParseResult]:
        if self._ci00_data_source:
            return self._ci00_data_source
        elif cls._pl10_data_source:
            return self._pl10_data_source
        else:
            raise ValueError("没有任何数据源可用")
