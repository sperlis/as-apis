import os
from enum import Enum

class PrintLevel(Enum):
    Normal = 1
    Verbose = 2

# Enhance "print" with a print level indication
def out(*output, level:PrintLevel= PrintLevel.Normal, **kwargs):
    verbose = level is PrintLevel.Verbose
    in_env = "AppScan_API_Verbose" in os.environ
    if verbose and not in_env:
        return

    print(*output, **kwargs)


