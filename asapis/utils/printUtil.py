import os
from enum import Enum
import json

class PrintLevel(Enum):
    Silent = 0
    Normal = 1
    Verbose = 2

# Enhance "print" with a print level indication
def logger(*output, level:PrintLevel= PrintLevel.Normal, **kwargs):
    print_level = PrintLevel[os.environ["AppScan_API_Log_Level"]]
    if print_level is PrintLevel.Silent:
        return

    if level is PrintLevel.Verbose and print_level is PrintLevel.Normal:
        return
    
    print(*output, **kwargs)

def print_result(*output, **kwargs):
    print(*output, **kwargs)

def print_json(prefix:str, object:dict, **kwargs):
    print(prefix  + json.dumps(object, indent=2))

