from enum import Enum

class JobActions(Enum):
    no_action = 0
    none = 1
    run = 2
    suspend = 3


class FolderItemState(Enum):
    Unknown = 0
    Ready = 1
    Running = 3
