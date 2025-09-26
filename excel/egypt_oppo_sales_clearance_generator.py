from os import write

from excel.appsettings import AppSettingsFactory
from excel.core.models.parse_result import PL10ReadParseResult, CI00ReadParseResult, WriteParseResult
from excel.core.models.parse_type import ParseType
from excel.core.parser import Parser
from excel.core.servicelocator import ServiceLocator
from excel.handlers.injectors.servicemodule import ServiceModule
from excel.handlers.models.pending_file_model import PendingFileModel
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.services.battery_brand_service import BatteryBrandService
from excel.handlers.services.file_scan_service import FileScanService
from excel.handlers.services.registered_invoice_number_service import RegisteredInvoicNumberService

class EgytpoppoSalesclearanceGenerator:
    """
    埃及oppo销售清关文件生成器
    """

    @classmethod
    def generate(cls, root_folder: str):
        """
        生成[销售清关CI&PL]文件
        :param root_folder: 要处理的清关文件根目录
        """
        # 初始化运行环境
        cls._initial(root_folder)

        # 循环处理所有采购CI&PL文件以生成响应的销售清关CI&PL文件
        for pending_file in ServiceLocator.getservice(FileScanService).scan():
            # 注入当前待处理文件
            ServiceLocator.register_instance(pending_file)

            # 写[货代 Invoice] Sheet
            cls._read_pending_file(pending_file, "CI00")
            cls._write_sales_clearance_file(pending_file, "货代 Invoice")
            break

    @staticmethod
    def _initial(root_folder: str):
        """
        初始化运行环境
        :param root_folder: 要处理的清关文件根目录
        """
        # 依赖注入
        ServiceLocator \
            .initial(ServiceModule()) \
            .register_instance(AppSettingsFactory.create(root_folder))

        # 获得相关服务实例(初始化相关数据)
        _ = ServiceLocator.getservice(BatteryBrandService)
        _ = ServiceLocator.getservice(RegisteredInvoicNumberService)
        _ = ServiceLocator.getservice(FileScanService)

    @staticmethod
    def _read_pending_file(pending_file: PendingFileModel, sheet_name: str):
        """
        读待处理文件
        :param pending_file: 待处理文件模型
        :param sheet_name: Sheet名称
        """
        with Parser(str(pending_file.pending_file_path), sheet_name) as parser_read:
            result_type = PL10ReadParseResult if sheet_name == "PL10" else CI00ReadParseResult
            parse_result = parser_read.parse(ParseType.READ, result_type)
            if result_type is CI00ReadParseResult:
                ServiceLocator.register_instance(WriterDataSource(ci00_data=parse_result))
            else:
                ServiceLocator.register_instance(WriterDataSource(pl10_data=parse_result))

    @staticmethod
    def _write_sales_clearance_file(pending_file: PendingFileModel, sheet_name: str):
        """
        写销售清关CI&PL文件
        :param pending_file:
        :param sheet_name:
        """
        template_file = str(pending_file.brand_subcategory_path / pending_file.sales_cipl_template_name)
        with Parser(template_file, sheet_name) as parser_write:
            parser_write.parse(ParseType.WRITE, WriteParseResult)

            # 写入销售清关CI&PL文件
            write_file = str(pending_file.sales_clearance_path / "my.xlsx")
            parser_write.save(write_file)
