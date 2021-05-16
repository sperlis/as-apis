import json
import time
from datetime import datetime

from asapis.services.aselib import ASE
from asapis.ase.aseEnums import FolderItemState
from asapis.utils.printUtil import logger

def handle_status(message) -> FolderItemState:
    """Prints the progress message according to the scope and gets the ExecutionProgress
        Args:

            message: object containing response status message

        Returns:

            ExecutionProgress of the status message
    """
    exec_prog = FolderItemState[message["content-scan-job"]["state"]["name"]]

    logger(f"{datetime.now()} - Progress is set to: {exec_prog.name}")

    return exec_prog

def monitor_scan_progress(ase:ASE, folder_item_id:str = None, continuos:bool = None, time_span:int = None):
    """Checks for scan progress. Can be called externally.
    Arguments kept as None will be assigned a value from the configured settings.

    Args:

        folder_item_id: FolderItem ID of the item to be monitored (usually scan or report pack)
        continuos: whether to repeat until completed
        timeSpan: number of seconds between progress checks (if continuos)

    """
    if continuos is None:
        continuos = ase.config["ScanMonitor"]["Continuos"]
    if time_span is None:
        time_span = ase.config["ScanMonitor"]["TimeSpanSeconds"]

    if folder_item_id is None:
        folder_item_id = ase.config["SubjectId"]

    while True:
        res = ase.get(f"folderitems/{folder_item_id}")
        if not res.ok:
            if res.status_code == 403:
                logger(f"Unauthorized. Check that scan exists and you have access to it")
            else:
                ase.print_response_error(res)
            exit(1)

        status = res.json()

        state = handle_status(status)
        if state is FolderItemState.Ready or not continuos:
            break
        time.sleep(time_span)

# We execute this only if the script is used specifically
# Otherwise, we just export the functions and let the main script call them if needed
if __name__ == "__main__":
    ase = ASE()
    # we just call the function to use the configured settings
    monitor_scan_progress(ase)
