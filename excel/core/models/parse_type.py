from enum import Enum, auto, unique

@unique
class ParseType(Enum):
    READ = auto()
    WRITE = auto()

    def __str__(self):
        return f"{self.name}_"
