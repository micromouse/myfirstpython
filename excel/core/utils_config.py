from excel.core.models.exel_config import ExcelConfig, ConfigKey

class UtilsConfig:
    """
    excel工具 - 配置
    """
    _config: ExcelConfig = {}

    @classmethod
    def init_config(cls, key: ConfigKey, value: str) -> type["UtilsConfig"]:
        """
        设置Excel配置值
        :param key: 键
        :param value: 值
        """
        if key in cls._config:
            raise ValueError(f"键[{key}]已设置值,不能再设置")

        cls._config[key] = value
        return cls

    @classmethod
    def get_config(cls, key: ConfigKey) -> str:
        """
        获得Excel配置值
        :param key: 键
        :return: 键值
        """
        if key not in cls._config:
            raise KeyError(f"未找到配置键[{key}]值")

        return cls._config[key]
