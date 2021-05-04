from asapis.services.asoclib import ASoC
from asapis.asoc.asocScanMonitor import monitor_scan_progress
from asapis.asoc.asocEnums import APIScopeV2
from asapis.utils.printUtil import out

asoc = ASoC()

# Create a SAST scan in ASoC

model = asoc.get_model("AsocSastScan")

# An application file (IRX) is required, otherwise the scan cannot proceed
scan_file = asoc.config["AsocSastScan"]["file"]
if scan_file:
    scan_file_id = asoc.upload(scan_file)
    if scan_file_id:
        model["ApplicationFileId"] = scan_file_id

# The ID can be placed directly in the model (externally) but it must exist
if not model["ApplicationFileId"]: 
    out("A required application file (IRX) is missing. Exiting.")
    exit(1)
    
res = asoc.post("Scans/StaticAnalyzer", json = model)

if not res.ok:
    asoc.print_response_error(res)
    exit(1)

scan_id = res.json()["Id"]

out(f"Created scan ID: {scan_id}")

if asoc.config["ScanMonitor"]["Automatic"]:
    monitor_scan_progress(asoc, subject_id=scan_id, scope=APIScopeV2.Scan)
