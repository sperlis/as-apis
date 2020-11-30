from enum import Enum

class ReportStatus(Enum):
    Pending = 1
    Starting = 2
    Running = 3
    Failed = 4
    Ready = 5
    Deleted = 6
