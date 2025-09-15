from decimal import Decimal
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
    hs_code: str
    model: str
    material_code: str
    description: str
    quantity: int
    unit_price: Decimal
    amount_usd: Decimal
    origin_country: str
