import os
from enum import Enum

class PrintLevel(Enum):
    Normal = 1
    Verbose = 2

def out(*output, level:PrintLevel= PrintLevel.Normal, **kwargs):
    verbose = level is PrintLevel.Verbose
    inEnv = "AppScan_API_Verbose" in os.environ
    if verbose and not inEnv:
        return

    print(*output, **kwargs)


