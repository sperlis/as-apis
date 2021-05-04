import time
from datetime import datetime

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import APIScopeV2, ExecutionProgressV3
from asapis.utils.printUtil import out

def handle_status(message, scope:APIScopeV2) -> ExecutionProgressV3:
    """Prints the progress message according to the scope and gets the ExecutionProgress
        Args:

            message: object containing response status message
            scope: the API scope of the original request

        Returns:

            ExecutionProgress of the status message
    """
    exec_prog = ExecutionProgressV3.Unknown
    pause_reason = ""
    if scope is APIScopeV2.Scan:
        exec_prog = ExecutionProgressV3[message["LatestExecution"]["ExecutionProgress"]]
        pause_reason = message["LatestExecution"]["PauseReason"]
    else:
        exec_prog = ExecutionProgressV3[message["ExecutionProgress"]]
        pause_reason = message["PauseReason"]

    out(f"{datetime.now()} - {scope.name} Progress is set to: {exec_prog.name}")
    if exec_prog is ExecutionProgressV3.Paused:
        out(f"{scope.name} paused due to: {pause_reason}")

    return exec_prog

def monitor_scan_progress(asoc:ASoC, subject_id:str = None, scope:APIScopeV2 = None, continuos:bool = None, time_span:int = None):
    """Checks for scan progress. Can be called externally.
    Arguments kept as None will be assigned a value from the configured settings.

    Args:

        subjectId: the ID of the subject of the call (depending on scope)
        scope: the scope of the API call
        continuos: whether to repeat until completed
        timeSpan: number of seconds between progress checks (if continuos)

    """
    if continuos is None:
        continuos = asoc.config["MonitorScan"]["Continuos"]
    if time_span is None:
        time_span = asoc.config["MonitorScan"]["TimeSpanSeconds"]

    if subject_id is None:
        subject_id = asoc.config["SubjectId"]

    if scope is None:
        scope = APIScopeV2[asoc.config["Scope"]]

    scope_string = ""
    if scope is APIScopeV2.Execution:
        scope_string = "Execution/"
    
    # This will be either "Scans/<subjectId>" or "Scans/Execution/<subjectId>"
    request_line = f"Scans/{scope_string}{subject_id}"

    while True:
        res = asoc.get(request_line)
        if not res.ok:
            if res.status_code == 403:
                out(f"Unauthorized. Check that scan or execution exists and you have access to it (ASoC returns a 403 either way)")
            else:
                asoc.print_response_error(res)
            exit(1)

        status = res.json()

        exec_prog = handle_status(status, scope)
        if exec_prog is ExecutionProgressV3.Completed or not continuos:
            break
        time.sleep(time_span)

# We execute this only if the script is used specifically
# Otherwise, we just export the functions and let the main script call them if needed
if __name__ == "__main__":
    asoc = ASoC()
    # we just call the function to use the configured settings
    monitor_scan_progress(asoc)
