from dataclasses import dataclass, field
from typing import Dict

@dataclasses
class CellparseResult:
    """
    单元格内容解析结果
    """
    result: Dict[str, Any] = field(default_factory=dict)
    next_row_index: int = 0
