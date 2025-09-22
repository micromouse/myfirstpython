from typing import Dict, Any, TypeVar, Type, overload

from excel.core.models.parse_result import CI00ReadParseResult, PL10ReadParseResult, ReadParseResult

TParseResult = TypeVar("TParseResult", bound=ReadParseResult)

class WriteHandlerBase:
    _ci00_data_source: CI00ReadParseResult = None
    _pl10_data_source: PL10ReadParseResult = None

    @overload
    @classmethod
    def _get_data_source(cls, data_type: Type[CI00ReadParseResult]) -> CI00ReadParseResult:
        ...

    @overload
    @classmethod
    def _get_data_source(cls, data_type: Type[PL10ReadParseResult]) -> PL10ReadParseResult:
        ...
    
    @classmethod
    def set_data_source(cls, ci00_data: CI00ReadParseResult = None, pl10_data: PL10ReadParseResult = None):
        """
        设置写入处理器数据源
        :param ci00_data: CI00 Sheet数据源
        :param pl10_data: PL10 Sheet数据源
        """
        cls._ci00_data_source = ci00_data
        cls._pl10_data_source = pl10_data

    @classmethod
    def _get_data_source(cls, data_type=Type[TParseResult]) -> TParseResult:
        """
        获得写入处理器数据源
        :return: 写入处理器数据源
        """
        if data_type is CI00ReadParseResult:
            return cls._ci00_data_source
        elif data_type is PL10ReadParseResult:
            return cls._pl10_data_source
        else:
            raise ValueError(f"不支持的数据类型[{data_type}]")
