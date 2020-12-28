from enum import Enum

class ReportStatus(Enum):
    Pending = 1
    Starting = 2
    Running = 3
    Failed = 4
    Ready = 5
    Deleted = 6

class APIScope(Enum):
    Application = 1
    Scan = 2
    Execution = 3

class ExecutionProgress(Enum):
    Pending = 1
    Running = 2
    UnderReview = 3 
    RunningManually = 4
    Paused = 5
    Completed = 6
    Unknown = 7

class Technology(Enum):
    DynamicAnalyzer = 1
    StaticAnalyzer = 2
    MobileAnalyzerAndroid = 3
    MobileAnalyzerIos = 4
    IFA = 5
    DastAutomation = 6
    IASTAnalyzer = 7
