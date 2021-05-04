from enum import Enum

######################################################
#
# The enums in this file are taken directly from the
# ASoC API models. 
#
class ReportStatusV2(Enum):
    Pending = 1
    Starting = 2
    Running = 3
    Failed = 4
    Ready = 5
    Deleted = 6

class APIScopeV2(Enum):
    Application = 1
    Scan = 2
    Execution = 3

class ExecutionProgressV3(Enum):
    Pending = 1
    Running = 2
    UnderReview = 3 
    RunningManually = 4
    Paused = 5
    Completed = 6
    Unknown = 7

class TechnologyV2(Enum):
    DynamicAnalyzer = 1
    StaticAnalyzer = 2
    MobileAnalyzerAndroid = 3
    MobileAnalyzerIos = 4
    IFA = 5
    DastAutomation = 6
    IASTAnalyzer = 7
