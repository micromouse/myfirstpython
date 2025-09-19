from typing import Dict, Any

class WriteHandlerBase:
    _data_source: Dict[str, Any] = {}

    @classmethod
    def set_data_source(cls, data: Dict[str, Any]):
        """
        设置写入处理器数据源
        :param data: 数据源
        """
        cls._data_source = data

    @classmethod
    def _get_data_source(cls):
        """
        获得写入处理器数据源
        :return: 写入处理器数据源
        """
        if not cls._data_source:
            raise ValueError("没有设置写入处理器")

        return cls._data_source
