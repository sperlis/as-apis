from asapis.services.asoclib import ASoC
from asapis.asoc.asocScanMonitor import monitorScanProgress
from asapis.asoc.asocEnums import APIScope
from asapis.utils.printUtil import out

asoc = ASoC()

# create a DAST scan in ASoC

model = asoc.Options["asocDastScan"]["model"]

# if a login-file is set, first upload it to ASoC
loginFile = asoc.Options["asocDastScan"]["loginFile"]
if loginFile:
    loginFileId = asoc.upload(loginFile)
    if loginFileId:
        model["LoginSequenceFileId"] = loginFileId
    else:
        out("Login file upload has failed. Stopping execution.")
        exit(1)

# if a scan-file (a .scan or .scant files) are set, upload them to ASoC
scanFile = asoc.Options["asocDastScan"]["file"]
if scanFile:
    scanFileId = asoc.upload(scanFile)
    if scanFileId:
        model["ScanFileId"] = scanFileId

if scanFile:
    res = asoc.post("Scans/DynamicAnalyzerWithFile", json = model)
else:
    res = asoc.post("Scans/DynamicAnalyzer", json = model)

if not res.ok:
    asoc.printResponseError(res)
    exit(1)

scanId = res.json()["Id"]

out(f"Created scan ID: {scanId}")

if asoc.Options["monitorProgress"]:
    monitorScanProgress(asoc, subjectId=scanId, scope=APIScope.Scan)
