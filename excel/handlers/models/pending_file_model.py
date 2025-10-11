from dataclasses import dataclass
from pathlib import Path

@dataclass
class PendingFileModel:
    """
    待处理文件模型(OPPO,RMG)
    """
    factory_name: str
    """
    工厂名称(OPPO,RMG)
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

    def get_sales_cipl_template_file_path(self) -> Path:
        """
        获得销售CI&PL模板.xlsx文件Path
        :return: 销售CI&PL模板.xlsx文件Path
        """
        return self.brand_subcategory_path / "销售CI&PL模板.xlsx"

    def get_sales_price_table_file_path(self) -> Path:
        """
        获得销售价目表.xlsx文件Path
        :return: 销售价目表.xlsx文件Path
        """
        return self.brand_subcategory_path / "销售价目表.xlsx"

    def get_sales_clearance_file_path(self, invoice_number: str) -> Path:
        """
        获得清关CI&PL文件Path
        :param invoice_number: 发票号
        :return: 清关CI&PL文件Path
        """
        filename = f"(草稿版){self.pending_file_path.stem}{invoice_number}.xlsx"
        return self.sales_clearance_path / filename
