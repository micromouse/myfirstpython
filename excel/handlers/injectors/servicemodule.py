import injector
from injector import Binder, NoScope, SingletonScope
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.injectors.iterationscope import IterationScope
from excel.core.parser import Parser
from excel.handlers.models.pending_file_model import PendingFileModel
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.reader.invoice_date_handlers import ReadInvoicedateHandlers
from excel.handlers.reader.purchase_detail_handlers import ReadPurchaseDetailHandlers
from excel.handlers.reader.total_handlers import ReadTotalHandlers
from excel.handlers.services.authenticationed_phone_model_service import AuthenticationedPhonemodelService
from excel.handlers.services.battery_brand_service import BatteryBrandService
from excel.handlers.services.file_scan_service import FileScanService
from excel.handlers.services.hscode_service import HScodeService
from excel.handlers.services.registered_invoice_number_service import RegisteredInvoicNumberService
from excel.handlers.services.sales_price_table_service import SalespriceTableService
from excel.handlers.writer.invoice_date_handlers import WriteInvoicedateHandlers
from excel.handlers.writer.invoice_number_handlers import WriteInvoicenumberHandlers
from excel.handlers.writer.purchase_detail_handlers import WritePurchasedetailHandlers

class ServiceModule(injector.Module):
    """
    服务模块，注入中心
    """

    def configure(self, binder: Binder) -> None:
        """
        服务注册配置器
        :param binder: injector绑定器
        :return: None
        """
        # 读写Excel处理器
        binder.bind(WriteInvoicedateHandlers, to=WriteInvoicedateHandlers, scope=NoScope)
        binder.bind(WriteInvoicenumberHandlers, to=WriteInvoicenumberHandlers, scope=NoScope)
        binder.bind(WritePurchasedetailHandlers, to=WritePurchasedetailHandlers, scope=NoScope)
        binder.bind(ReadInvoicedateHandlers, to=ReadInvoicedateHandlers, scope=NoScope)
        binder.bind(ReadPurchaseDetailHandlers, to=ReadPurchaseDetailHandlers, scope=NoScope)
        binder.bind(ReadTotalHandlers, to=ReadTotalHandlers, scope=NoScope)

        # 服务
        binder.bind(BatteryBrandService, to=BatteryBrandService, scope=SingletonScope)
        binder.bind(FileScanService, to=FileScanService, scope=SingletonScope)
        binder.bind(RegisteredInvoicNumberService, to=RegisteredInvoicNumberService, scope=SingletonScope)
        binder.bind(HScodeService, to=HScodeService, scope=SingletonScope)
        binder.bind(AuthenticationedPhonemodelService, to=AuthenticationedPhonemodelService, scope=SingletonScope)
        binder.bind(SalespriceTableService, to=SalespriceTableService, scope=IterationScope)

        # 解析Excel
        binder.bind(Parser, to=Parser, scope=NoScope)
        binder.bind(Workbook, scope=IterationScope)
        binder.bind(Worksheet, scope=IterationScope)
        binder.bind(PendingFileModel, scope=IterationScope)
        binder.bind(WriterDataSource, scope=IterationScope)
