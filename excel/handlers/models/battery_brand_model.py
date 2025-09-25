from dataclasses import dataclass

@dataclass
class BatteryBrandModel:
    """
    电池品牌信息模型
    """
    material_code: str
    """
    物料编码
    """
    model: str
    """
    电池型号
    """
    description: str
    """
    货物描述
    """
    supplier: str
    """
    供应商
    """
    brand: str
    """
    品牌
    """
