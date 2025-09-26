from dataclasses import dataclass
from pathlib import Path

@dataclass
class PendingFileModel:
    """
    待处理文件模型
    """
    factory_name: str
    """
    工厂名称
    """
    brand_category: str
    """
    品牌大类
    """
    brand_subcategory: str
    """
    品牌子类
    """
    brand_subcategory_path: Path
    """
    品牌全路径子类目录
    """
    sales_clearance_path: Path
    """
    销售清关CI&PL全路径目录
    """
    pending_file_path: Path
    """
    待处理文件名称
    """
    sales_cipl_template_name = "销售CI&PL模板.xlsx"
    """
    销售CI&PL模板.xlsx文件名
    """
    sales_price_table_name = "销售价目表.xlsx"
    """
    销售价目表.xlsx文件名
    """
