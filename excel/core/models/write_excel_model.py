from dataclasses import dataclass

@dataclass
class WriteExcelModel:
    file: str
    sheet_index: int = 0
    sheet_name: str = None
    saveas_file: str = None
