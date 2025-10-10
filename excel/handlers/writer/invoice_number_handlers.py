from injector import inject
from openpyxl.cell.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel.core.dispatcher import Dispatcher
from excel.core.models.parse_result import CellparseResult, CI00ReadParseResult, WriteParseResult
from excel.handlers.models.pending_file_model import PendingFileModel
from excel.handlers.models.writer_datasource import WriterDataSource
from excel.handlers.services.registered_invoice_number_service import RegisteredInvoicNumberService
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class WriteInvoicenumberHandlers(WriteHandlerBase):
    """
    发票号处理器
    """
    _invoice_number: str = ""

    @inject
    def __init__(
            self,
            registered_invoice_number_service: RegisteredInvoicNumberService,
            workbook: Workbook,
            worksheet: Worksheet,
            datasource: WriterDataSource,
            pending_file_model: PendingFileModel):
        """
        初始化发票号处理器
        :param registered_invoice_number_service: 已注册发票号服务
        :param datasource: Excel写入器数据源
        :param pending_file_model: 待处理采购CI&PL文件模型
        """
        super().__init__(workbook, worksheet, datasource)
        self._registered_invoice_number_service = registered_invoice_number_service
        self._pending_file_model = pending_file_model

    @Dispatcher.keyword("WRITE_INVOICE NO.")
    def handle_invoice_number(self, cell: Cell) -> CellparseResult:
        """
        处理发票号(货代Invoice和With material code Sheet用)
        """
        self._worksheet.cell(cell.row, cell.column + 2).value = self._save_and_get_invoice_number()
        self._workbook["With material code"].cell(cell.row, cell.column + 2).value = self._save_and_get_invoice_number()
        write_parse_result = dict(WriteParseResult(invoice_number=self._invoice_number))
        return CellparseResult(write_parse_result, next_row_index=cell.row)

    def _save_and_get_invoice_number(self) -> str:
        """
        保存并获得发票号
        :return: 发票号
        """
        # 未设置发票号,先设置发票号
        if self._invoice_number == "":
            # 从CI00 Sheet获得发票号
            original_invoice_number = self._datasource.get_data_source(CI00ReadParseResult)["invoice_number"]
            current_invoice_nubmers = sorted(original_invoice_number.split(","), reverse=True)
            if not current_invoice_nubmers:
                raise ValueError("CI00 Sheet未包含发票号信息")

            # 获得新的发票号、保存新发票号到已注册发票号文件
            WriteInvoicenumberHandlers._invoice_number = self._registered_invoice_number_service.get_new_invoice_number(current_invoice_nubmers)
            self \
                ._registered_invoice_number_service \
                .save_new_invoice_number(self._pending_file_model, original_invoice_number, self._invoice_number)

        return self._invoice_number
