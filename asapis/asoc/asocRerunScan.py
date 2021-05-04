import requests

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import APIScopeV2, TechnologyV2
from asapis.utils.printUtil import out
from asapis.asoc.asocScanMonitor import monitor_scan_progress

asoc = ASoC()

# Rerun a previously created scan

scan_id = asoc.config["SubjectId"]

res = asoc.get(f"Scans/{scan_id}")

if not res.ok:
    asoc.print_response_error(res)
    exit(1)

scan_data = res.json()

technology:TechnologyV2 = TechnologyV2[scan_data["Technology"]]

# First, we update any changes to the scan
# The update model allows us to change the name of the scan name, 
# sending email notifications, and the Presence ID (for DAST scans)
update_model = {
    "Name": scan_data["Name"],
    "EnableMailNotifications": scan_data["EnableMailNotification"],
    "PresenceId": scan_data["Id"]
}
model = None
if technology is TechnologyV2.DynamicAnalyzer:
    model = asoc.get_model("AsocDastScan")
else:
    model = asoc.config("AsocSastScan")

changed = False

# for static analysis we only change the name and 
if update_model["Name"] != model["Name"]:
    changed = True
    update_model["Name"] = model["Name"]
if update_model["EnableMailNotifications"] != model["EnableMailNotifications"]:
    changed = True
    update_model["EnableMailNotifications"] = model["EnableMailNotifications"]

# dynamic may update the Presence ID as well, which is irrelevant for SAST scans
if model["PresenceId"] and update_model["PresenceId"] != model["PresenceId"]:
    changed = True
    update_model["PresenceId"] = model["PresenceId"]

# if no changes were configured, we skip the update
if changed:
    res = asoc.put(f"Scans/{scan_id}", json=update_model)


rerun_model = {
    "FileId": "",
    "ClientType": "ASoC-API-Samples"
}

# for static analysis, it only makes to run a rescan with a new IRX
# we need to upload it here
if technology is TechnologyV2.StaticAnalyzer:
    scan_file = asoc.config["asocSastScan"]["file"]
    if scan_file:
        scan_file_id = asoc.upload(scan_file)
        if scan_file_id:
            model["ApplicationFileId"] = scan_file_id
    # this will either be the file we just uploaded, or an ID configured externally
    # from un uploaded file
    rerun_model["FileId"] = model["ApplicationFileId"]

res = asoc.post(f"Scans/{scan_id}/Executions", json=rerun_model)

if not res.ok:
    asoc.print_response_error(res)
    exit(1)

out(f"Reran scan ID: {scan_id}")

if asoc.config["ScanMonitor"]["Automatic"]:
    monitor_scan_progress(asoc, subject_id=scan_id, scope=APIScopeV2.Scan)
