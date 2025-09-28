import injector
from injector import Binder, SingletonScope

from excel.core.injectors.iterationscope import IterationScope
from excel.handlers.models.pending_file_model import PendingFileModel
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.services.battery_brand_service import BatteryBrandService
from excel.handlers.writer.invoice_date_handlers import InvoicedateHandlers
from excel.handlers.writer.invoice_number_handlers import InvoicenumberHandlers
from excel.handlers.writer.purchase_detail_handlers import PurchasedetailHandlers

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
        binder.bind(InvoicedateHandlers, to=InvoicedateHandlers)
        binder.bind(InvoicenumberHandlers, to=InvoicenumberHandlers)
        binder.bind(PurchasedetailHandlers, to=PurchasedetailHandlers)
        binder.bind(BatteryBrandService, to=BatteryBrandService, scope=SingletonScope)
        binder.bind(PendingFileModel, scope=IterationScope)
        binder.bind(WriterDataSource, scope=IterationScope)
