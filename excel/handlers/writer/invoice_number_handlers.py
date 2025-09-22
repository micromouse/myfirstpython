import os.path
import re
from typing import List

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

from excel.core.fluent_excel_writer import FluentExcelWriter
from excel.core.models.parse_result import CellparseResult, CI00ReadParseResult
from excel.core.dispatcher import Dispatcher
from excel.core.utils import Utils
from excel.handlers.writer.write_handler_base import WriteHandlerBase

@Dispatcher.register_handlers
class InvoicenumberHandlers(WriteHandlerBase):
    """
    发票号处理器
    """
    _invoice_number: str = ""

    @classmethod
    @Dispatcher.keyword("WRITE_INVOICE NO.")
    def handle_invoice_number(cls, sheet: Worksheet, cell: Cell) -> CellparseResult:
        """
        处理发票号(货代Invoice和With material code Sheet用)
        """
        sheet.cell(cell.row, cell.column + 2).value = cls._save_and_get_invoice_number()
        return CellparseResult()

    @classmethod
    def _save_and_get_invoice_number(cls) -> str:
        """
        保存并获得发票号
        :return: 发票号
        """
        # 未设置发票号,先设置发票号
        if cls._invoice_number == "":
            # 从CI00 Sheet获得发票号
            original_invoice_number = cls._get_data_source(CI00ReadParseResult)["invoice_number"]
            current_invoice_nubmers = sorted(original_invoice_number.split(","), reverse=True)
            if not current_invoice_nubmers:
                raise ValueError("CI00 Sheet未包含发票号信息")

            # 获得新的发票号、保存新发票号到已注册发票号文件
            cls._invoice_number = cls._get_new_invoice_number(current_invoice_nubmers)
            cls._save_new_invoice_number(original_invoice_number)

        return cls._invoice_number

    @classmethod
    def _get_new_invoice_number(cls, current_invoice_nubmers: List[str]) -> str:
        """
        获得新发票号
        :param current_invoice_nubmers: 当前发票号集合
        :return: 新发票号
        """
        file = Utils.get_config("registered_invoice_number_file")
        registered_invoice_numbers = Utils.get_column_values(file, 0, 3)
        unused_invoice_numbers = sorted((set(current_invoice_nubmers) - set(registered_invoice_numbers)), reverse=True)

        # 有未使用的发票号，取最大的一个
        if unused_invoice_numbers:
            new_invoice_number = unused_invoice_numbers[0]
        else:
            new_invoice_number = current_invoice_nubmers[0].strip()
            used_invoice_numbers = list({
                n for n in registered_invoice_numbers if
                n == new_invoice_number or
                n.startswith(f"{new_invoice_number}-")
            })
            new_invoice_number = f"{new_invoice_number}-{cls._get_max_suffix_number(used_invoice_numbers) + 1}"

        return new_invoice_number

    @classmethod
    def _get_max_suffix_number(cls, used_invoice_numbers: List[str]) -> int:
        """
        从已使用发票号集合中获得最大后缀号
        :param used_invoice_numbers: 已使用发票号
        :return: 已使用发票号最大后缀
        """
        suffix_numbers: List[int] = []
        for n in used_invoice_numbers:
            """
            re.match(pattern, string) → 从字符串开头匹配，只匹配开头
            re.search(pattern, string) → 整个字符串搜索，匹配任意位置
            re.fullmatch(pattern, string) → 整个字符串完全匹配            
            """
            match = re.search(r"-(\d+)$", n)
            suffix_numbers.append(int(match.group(1)) if match else 0)

        return max(suffix_numbers)

    @classmethod
    def _save_new_invoice_number(cls, original_invoice_number: str):
        def _add_new_invoice_row(sheet: Worksheet):
            new_row_index = sheet.max_row + 1
            sheet.cell(new_row_index, 1, os.path.basename(cls._get_data_source(CI00ReadParseResult)["filename"])[:4])
            sheet.cell(new_row_index, 2, cls._get_data_source(CI00ReadParseResult)["invoice_type"])
            sheet.cell(new_row_index, 3, cls._invoice_number)
            sheet.cell(new_row_index, 4, original_invoice_number)

        FluentExcelWriter() \
            .set_file(Utils.get_config("registered_invoice_number_file")) \
            .write(_add_new_invoice_row)
