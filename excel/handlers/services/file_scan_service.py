from pathlib import Path
from typing import List, Optional

from injector import inject

from excel.appsettings import AppSettings
from excel.handlers.models.pending_file_model import PendingFileModel

class FileScanService:
    """
    文件扫描服务
    """
    _pending_files: List[PendingFileModel] = []

    @inject
    def __init__(self, appsettings: AppSettings):
        """
        初始化文件扫描服务
        :param appsettings: 应用程序配置
        """
        self._appsettings = appsettings

    def scan(self) -> List[PendingFileModel]:
        """
        扫描根目录下的所有.xlsx文件生成待处理文件集合
        :return: 待处理文件集合
        """
        if not self._pending_files:
            root_folder = Path(self._appsettings.root_folder)
            for file_path in root_folder.glob("**/*.xlsx"):
                file_model = self._extract_file(root_folder, file_path)
                if file_model:
                    self._pending_files.append(file_model)

        return self._pending_files

    @classmethod
    def _extract_file(cls, root_folder: Path, file_path: Path) -> Optional[PendingFileModel]:
        """
        从文件路径中提取文件信息
        :param file_path: 文件路径
        :return: 文件信息
        """
        relative_parts = file_path.relative_to(root_folder).parts
        if len(relative_parts) != 5:
            return None

        factory_name, brand_category, brand_subcategory, parent_foldername, filename = relative_parts[:5]
        if not parent_foldername.endswith("采购CI&PL"):
            return None

        return PendingFileModel(
            factory_name=cls._extract_factory_name(factory_name),
            brand_category=brand_category,
            brand_subcategory=brand_subcategory,
            brand_subcategory_path=file_path.parent.parent,
            sales_clearance_path=cls._extract_sales_path(file_path),
            pending_file_path=file_path
        )

    @staticmethod
    def _extract_factory_name(factoryname: str) -> str:
        """
        提取工厂名称
        :param factoryname: 原始工厂名称
        :return: 解析后的工厂名称
        """
        if factoryname.startswith("收货方：OPPO"):
            return "OPPO"
        elif factoryname.startswith("收货方：RMG"):
            return "RMG"
        else:
            raise ValueError("程序仅处理[收货方：OPPO, 收货方：RMG]")

    @staticmethod
    def _extract_sales_path(file_path: Path) -> Path:
        """
        获得销售清关CI&PL目录全路径
        :param file_path: 当前文件
        :return: 销售清关CI&PL目录全路径
        """
        sales_folder_name = file_path.parent.name.replace("采购CI&PL", "销售清关CI&PL")
        sales_path = file_path.parent.parent / sales_folder_name
        if not sales_path.exists():
            raise FileNotFoundError(f"采购CI&PL文件[{file_path}]所在销售清关CI&PL目录[{sales_path}]不存在")

        return sales_path