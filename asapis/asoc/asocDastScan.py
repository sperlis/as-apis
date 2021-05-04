from asapis.services.asoclib import ASoC
from asapis.asoc.asocScanMonitor import monitor_scan_progress
from asapis.asoc.asocEnums import APIScopeV2
from asapis.utils.printUtil import out

asoc = ASoC()

# create a DAST scan in ASoC

model = asoc.get_model("AsocDastScan")

# if a login-file is set, first upload it to ASoC
login_file = asoc.config["AsocDastScan"]["loginFile"]
if login_file:
    login_file_id = asoc.upload(login_file)
    if login_file_id:
        model["LoginSequenceFileId"] = login_file_id
    else:
        out("Login file upload has failed. Stopping execution.")
        exit(1)

# if a scan-file (a .scan or .scant files) are set, upload them to ASoC
scan_file = asoc.config["AsocDastScan"]["File"]
if scan_file:
    scan_file_id = asoc.upload(scan_file)
    if scan_file_id:
        model["ScanFileId"] = scan_file_id

if scan_file:
    res = asoc.post("Scans/DynamicAnalyzerWithFile", json = model)
else:
    res = asoc.post("Scans/DynamicAnalyzer", json = model)

if not res.ok:
    asoc.print_response_error(res)
    exit(1)

scan_id = res.json()["Id"]

out(f"Created scan ID: {scan_id}")

if asoc.config["ScanMonitor"]["Automatic"]:
    monitor_scan_progress(asoc, subject_id=scan_id, scope=APIScopeV2.Scan)
