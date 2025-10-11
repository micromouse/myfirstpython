from decimal import Decimal
from abc import ABC
from typing import TypedDict

class PurchaseDetail(TypedDict):
    """
    采购明细模型(继承者TypedDict,Python 3.8+)
    特点：
        是字典类型的类型标注
        不能存方法，只描述数据结构
        主要作用是 类型检查和自动补全
        可以定义必需和可选字段
        对象本质还是字典
    """
    shipping_marks: str
    material_code: str
    description: str

class CI00PurchaseDetail(PurchaseDetail):
    """
    CI00采购明细模型
    """
    quantity: int
    unit_price: Decimal
    amount_usd: Decimal
    origin_country: str
    remark: str
    pass

class PL10PurchaseDetail(PurchaseDetail):
    """
    PL10采购明细模型
    """
    total_quantity: int
    total_packages: int | None
