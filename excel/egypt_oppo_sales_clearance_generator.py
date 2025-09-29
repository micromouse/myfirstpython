from typing import Tuple, Any, List

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.appsettings import AppSettingsFactory
from excel.core.models.parse_result import PL10ReadParseResult, CI00ReadParseResult, WriteParseResult
from excel.core.models.parse_type import ParseType
from excel.core.parser import Parser
from excel.core.injectors.servicelocator import ServiceLocator
from excel.core.utils import Utils
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
            # 写[货代 Invoice, With material code, 货代 Packing] Sheet
            cls._write_sales_clearance_file(pending_file, "CI00", "货代 Invoice")
            cls._write_sales_clearance_file(pending_file, "CI00", "With material code")
            cls._write_sales_clearance_file(pending_file, "PL10", "货代 Packing")
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

    @classmethod
    def _write_sales_clearance_file(cls, pending_file: PendingFileModel, pending_sheet_name: str, write_sheetname: str):
        """
        写销售清关CI&PL文件
        :param pending_file: 待处理文件
        :param pending_sheet_name: 待处理文件Sheet名
        :param write_sheetname: 写入Excel文件Sheet名
        """
        # 读取待处理excel sheet获得待写入文件数据源
        writer_datasource = cls._read_pending_file(pending_file, pending_sheet_name)

        # 加载要写入的Excel文件Worksheet对象
        template_file = str(pending_file.brand_subcategory_path / pending_file.sales_cipl_template_name)
        workbook, worksheet = Utils.load_worksheet(template_file, write_sheetname)

        # 写入Excel Worksheet
        with ServiceLocator \
                .get_iteration_scope() \
                .enter((Workbook, workbook),
                       (Worksheet, worksheet),
                       (PendingFileModel, pending_file),
                       (WriterDataSource, writer_datasource)):
            with ServiceLocator.getservice(Parser) as parser_write:
                parser_write.parse(ParseType.WRITE, WriteParseResult)

                # 写入销售清关CI&PL文件
                write_file = str(pending_file.sales_clearance_path / "my.xlsx")
                parser_write.save(write_file)

    @staticmethod
    def _read_pending_file(pending_file: PendingFileModel, sheet_name: str) -> WriterDataSource:
        """
        读待处理文件
        :param pending_file: 待处理文件模型
        :param sheet_name: Sheet名称
        :return: 写入器数据源
        """
        workbook, worksheet = Utils.load_worksheet(str(pending_file.pending_file_path), sheet_name)
        with ServiceLocator \
                .get_iteration_scope() \
                .enter((Workbook, workbook),
                       (Worksheet, worksheet),
                       (PendingFileModel, pending_file)):
            with ServiceLocator.getservice(Parser) as parser_write:
                with ServiceLocator.getservice(Parser) as parser_read:
                    result_type = PL10ReadParseResult if sheet_name == "PL10" else CI00ReadParseResult
                    parse_result = parser_read.parse(ParseType.READ, result_type)
                    return WriterDataSource(pl10_data=parse_result) if sheet_name == "PL10" else WriterDataSource(ci00_data=parse_result)
