from typing import Callable

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.appsettings import AppSettingsFactory
from excel.core.injectors.servicelocator import ServiceLocator
from excel.core.models.parse_result import PL10ReadParseResult, CI00ReadParseResult, WriteParseResult
from excel.core.models.parse_type import ParseType
from excel.core.parser import Parser
from excel.core.utils import Utils
from excel.handlers.injectors.servicemodule import ServiceModule
from excel.handlers.models.pending_file_model import PendingFileModel
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.services.authenticationed_phone_model_service import AuthenticationedPhonemodelService
from excel.handlers.services.battery_brand_service import BatteryBrandService
from excel.handlers.services.file_scan_service import FileScanService
from excel.handlers.services.hscode_service import HScodeService
from excel.handlers.services.registered_invoice_number_service import RegisteredInvoicNumberService
from excel.handlers.services.sales_price_table_service import SalespriceTableService
from excel.handlers.writer.invoice_number_handlers import WriteInvoicenumberHandlers

class EgytpoppoSalesclearanceGenerator:
    """
    埃及oppo销售清关文件生成器
    """
    _root_folder: str
    _handle_progress: Callable[[str], None]

    @classmethod
    def generate(cls):
        """
        生成[销售清关CI&PL]文件
        """
        # 循环处理所有采购CI&PL文件以生成响应的销售清关CI&PL文件
        pending_files = ServiceLocator.getservice(FileScanService).scan()
        for index, pending_file in enumerate(pending_files, start=1):
            try:
                cls._handle_progress(f"正在处理[{index}/{len(pending_files)}][{pending_file.pending_file_path}]文件")

                # 读 [采购CI&PL] Excel文件
                ci00_writer_datasource = cls._read_pending_file(pending_file, "CI00")
                cpl10_writer_datasource = cls._read_pending_file(pending_file, "PL10")

                # 写[货代 Invoice, 货代 Packing] Sheet
                cls._write_sales_clearance_file(pending_file, ci00_writer_datasource, cpl10_writer_datasource)

                # 保存发票号
                ServiceLocator \
                    .getservice(RegisteredInvoicNumberService) \
                    .save_new_invoice_number(
                    pending_file_model=pending_file,
                    original_invoice_number=ci00_writer_datasource.get_data_source(CI00ReadParseResult)["invoice_number"],
                    new_invoice_number=pending_file.sales_clearance_invoice_number
                )
            except Exception as e:
                cls._handle_progress(f"处理采购CI&PL文件[{pending_file.pending_file_path}]时发生异常\r\n{e}")
                raise e

        cls._handle_progress(f"已完成全部[{len(pending_files)}]个采购CI&PL文件处理")

    @classmethod
    def initial(cls, root_folder: str) -> type["EgytpoppoSalesclearanceGenerator"]:
        """
        初始化运行环境
        :param root_folder: 要处理的清关文件根目录
        """
        cls._root_folder = root_folder

        # 依赖注入
        ServiceLocator \
            .initial(ServiceModule()) \
            .register_instance(AppSettingsFactory.create(root_folder))

        # 获得相关服务实例(初始化相关数据)
        _ = ServiceLocator.getservice(BatteryBrandService)
        _ = ServiceLocator.getservice(RegisteredInvoicNumberService)
        _ = ServiceLocator.getservice(FileScanService)
        _ = ServiceLocator.getservice(HScodeService)
        _ = ServiceLocator.getservice(AuthenticationedPhonemodelService)

        return cls

    @classmethod
    def set_handle_progress(cls, func: Callable[[str], None]) -> type["EgytpoppoSalesclearanceGenerator"]:
        """
        设置处理进度回调函数
        :param func: 处理进度回调函数
        """
        cls._handle_progress = func
        return cls

    @classmethod
    def _write_sales_clearance_file(
            cls,
            pending_file: PendingFileModel,
            ci00_writer_datasource: WriterDataSource,
            pl10_writer_datasource: WriterDataSource):
        """
        写销售清关CI&PL文件
        :param pending_file: 待处理采购CI&PL文件
        :param ci00_writer_datasource: CI00 Sheet数据源
        :param pl10_writer_datasource: PL10 Sheet数据源
        :return:
        """
        template_file = pending_file.get_sales_cipl_template_file_path()
        workbook = load_workbook(template_file)
        with ServiceLocator \
                .get_iteration_scope() \
                .enter((Workbook, workbook), (PendingFileModel, pending_file)):
            # 写 [货代 Invoice] Sheet
            invoice_write_parse_result = cls._write_sales_clearance_file_sheet(workbook, ci00_writer_datasource, "货代 Invoice")
            pending_file.sales_clearance_invoice_number = invoice_write_parse_result["invoice_number"]

            # 写 [货代 Packing] Sheet
            cls._write_sales_clearance_file_sheet(workbook, pl10_writer_datasource, "货代 Packing")

            # 保存
            write_file_path = pending_file.get_sales_clearance_file_path(invoice_write_parse_result["invoice_number"])
            workbook.save(write_file_path)
            workbook.close()

    @classmethod
    def _write_sales_clearance_file_sheet(
            cls,
            workbook: Workbook,
            writer_datasource: WriterDataSource,
            sheet_name: str) -> WriteParseResult:
        """
        写销售清关CI&PL文件Sheet
        :param writer_datasource: Sheet数据源
        :param sheet_name: Sheet名称
        :return: 写Sheet结果
        """
        ServiceLocator \
            .get_iteration_scope() \
            .enter((Worksheet, workbook[sheet_name]), (WriterDataSource, writer_datasource))
        return ServiceLocator.getservice(Parser).parse(ParseType.WRITE, WriteParseResult)

    @staticmethod
    def _read_pending_file(pending_file: PendingFileModel, sheet_name: str) -> WriterDataSource:
        """
        读待处理文件
        :param pending_file: 待处理文件模型
        :param sheet_name: Sheet名称
        :return: 写入器数据源
        """
        workbook, worksheet = Utils.load_worksheet(str(pending_file.pending_file_path), sheet_name=sheet_name)
        with ServiceLocator \
                .get_iteration_scope() \
                .enter((Workbook, workbook),
                       (Worksheet, worksheet),
                       (PendingFileModel, pending_file)):
            with ServiceLocator.getservice(Parser) as parser_read:
                result_type = PL10ReadParseResult if sheet_name == "PL10" else CI00ReadParseResult
                parse_result = parser_read.parse(ParseType.READ, result_type)
                if sheet_name == "PL10":
                    return WriterDataSource(pl10_data=parse_result)
                else:
                    return WriterDataSource(ci00_data=parse_result)
