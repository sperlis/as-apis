import time
from datetime import datetime

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import APIScope, ExecutionProgress
from asapis.utils.printUtil import out

def handleStatus(message, scope:APIScope) -> bool:
    """Prints the progress message according to the scope and gets the ExecutionProgress
        Args:

            message: object containing response status message
            scope: the API scope of the original request

        Returns:

            ExecutionProgress of the status message
    """
    execProg = ExecutionProgress.Unknown
    pauseReason = ""
    if scope is APIScope.Scan:
        execProg = ExecutionProgress[message["LatestExecution"]["ExecutionProgress"]]
        pauseReason = message["LatestExecution"]["PauseReason"]
    else:
        execProg = ExecutionProgress[message["ExecutionProgress"]]
        pauseReason = message["PauseReason"]

    out(f"{datetime.now()} - {scope.name} Progress is set to: {execProg.name}")
    if execProg is ExecutionProgress.Paused:
        out(f"{scope.name} paused due to: {pauseReason}")

    return execProg

def monitorScanProgress(asoc:ASoC, subjectId:str = None, scope:APIScope = None, continuos:bool = None, timeSpan:int = None):
    """Checks for scan progress. Can be called externally.
    Arguments kept as None will be assigned a value from the configured settings.

    Args:

        subjectId: the ID of the subject of the call (depending on scope)
        scope: the scope of the API call
        continuos: whether to repeat until completed
        timeSpan: number of seconds between progress checks (if continuos)

    """
    if continuos is None:
        continuos = asoc.Options["asocMonitorScan"]["continuos"]
    if timeSpan is None:
        timeSpan = asoc.Options["asocMonitorScan"]["timeSpanSeconds"]

    if subjectId is None:
        subjectId = asoc.Options["subjectId"]

    if scope is None:
        scope = APIScope[asoc.Options["scope"]]

    scopeString = ""
    if scope is APIScope.Execution:
        scopeString = "Execution/"
    
    # this will be either "Scans/<subjectId>" or "Scans/Execution/<subjectId>"
    requestLine = f"Scans/{scopeString}{subjectId}"

    while True:
        res = asoc.get(requestLine)
        if not res.ok:
            if res.status_code == 403:
                out(f"Unauthorized. Check that scan or execution exists and you have access to it (ASoC returns a 403 either way)")
            else:
                asoc.printResponseError(res)
            exit(1)

        status = res.json()

        execProg = handleStatus(status, scope)
        if execProg is ExecutionProgress.Completed or not continuos:
            break
        time.sleep(timeSpan)

# we execute this only if script is used specifically
# otherwise, we just export the functions and let the main script call them if needed
if __name__ == "__main__":
    asoc = ASoC()
    # we just call the function to use the configured settings
    monitorScanProgress(asoc)