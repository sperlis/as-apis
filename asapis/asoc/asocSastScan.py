from asapis.services.asoclib import ASoC
from asapis.asoc.asocScanMonitor import monitorScanProgress
from asapis.asoc.asocEnums import APIScope
from asapis.utils.printUtil import out

asoc = ASoC()

# create a SAST scan in ASoC

model = asoc.Options["asocSastScan"]["model"]

# an application (IRX) file is required, otherwise the scan cannot proceed
scanFile = asoc.Options["asocSastScan"]["file"]
if scanFile:
    scanFileId = asoc.upload(scanFile)
    if scanFileId:
        model["ApplicationFileId"] = scanFileId

# the ID can be placed directly in the model (externally) but it must exist
if not model["ApplicationFileId"]: 
    out("A required application (IRX) is missing. Exiting.")
    exit(1)
    
res = asoc.post("Scans/StaticAnalyzer", json = model)

if not res.ok:
    asoc.printResponseError(res)
    exit(1)

scanId = res.json()["Id"]

out(f"Created scan ID: {scanId}")

if asoc.Options["monitorProgress"]:
    monitorScanProgress(asoc, subjectId=scanId, scope=APIScope.Scan)
