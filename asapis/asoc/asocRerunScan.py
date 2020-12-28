import requests

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import APIScope, Technology
from asapis.utils.printUtil import out
from asapis.asoc.asocScanMonitor import monitorScanProgress

asoc = ASoC()

# rerun a previously created scan

scanId = asoc.Options["subjectId"]

res = asoc.get(f"Scans/{scanId}")

if not res.ok:
    asoc.printResponseError(res)
    exit(1)

scanData = res.json()

technology:Technology = Technology[scanData["Technology"]]

# First, we update any changes to the scan
# The update model allows us to change the name of the scan name, 
# sending email notifications, and the Presence ID (for DAST scans)
updateModel = {
    "Name": scanData["Name"],
    "EnableMailNotifications": scanData["EnableMailNotification"],
    "PresenceId": scanData["Id"]
}
model = None
if technology is Technology.DynamicAnalyzer:
    model = asoc.Options["asocDastScan"]["model"]
else:
    model = asoc.Options["asocSastScan"]["model"]

changed = False

# for static analysis we only change the name and 
if updateModel["Name"] != model["Name"]:
    changed = True
    updateModel["Name"] = model["Name"]
if updateModel["EnableMailNotifications"] != model["EnableMailNotifications"]:
    changed = True
    updateModel["EnableMailNotifications"] = model["EnableMailNotifications"]

# dynamic may update the Presence ID as well, which is irrelevant for SAST scans
if model["PresenceId"] and updateModel["PresenceId"] != model["PresenceId"]:
    changed = True
    updateModel["PresenceId"] = model["PresenceId"]

# if no changes were configured, we skip the update
if changed:
    res = asoc.put(f"Scans/{scanId}", json=updateModel)


rerunModel = {
    "FileId": "",
    "ClientType": "ASoC-API-Samples"
}

# for static analysis, it only makes to run a rescan with a new IRX
# we need to upload it here
if technology is Technology.StaticAnalyzer:
    scanFile = asoc.Options["asocSastScan"]["file"]
    if scanFile:
        scanFileId = asoc.upload(scanFile)
        if scanFileId:
            model["ApplicationFileId"] = scanFileId
    # this will either be the file we just uploaded, or an ID configured externally
    # from un uploaded file
    rerunModel["FileId"] = model["ApplicationFileId"]

res = asoc.post(f"Scans/{scanId}/Executions", json=rerunModel)

if not res.ok:
    asoc.printResponseError(res)
    exit(1)

out(f"Reran scan ID: {scanId}")

if asoc.Options["monitorProgress"]:
    monitorScanProgress(asoc, subjectId=scanId, scope=APIScope.Scan)
