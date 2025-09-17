from enum import Enum, auto

class ParseType(Enum):
    READ = auto()
    WRITE = auto()

    def __str__(self):
        return f"{self.name}_"
