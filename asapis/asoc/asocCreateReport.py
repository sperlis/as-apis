import time
import codecs
import os.path

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import ReportStatusV2
from asapis.utils.printUtil import out

asoc = ASoC()


# initialize variables from the options
app_id = asoc.config["SubjectId"]
scope = asoc.config["Scope"]

# the model is used as-is, but can be programmatically manipulated here
model = asoc.get_model("AsocReport")

# create a report file name with extension based on the report type
report_type = model["Configuration"]["ReportFileType"]
report_name = asoc.config["AsocReport"]["name"]
report_name = report_name + "." + report_type.lower()

report_path = os.path.join(asoc.config["AsocReport"]["path"],report_name)

# create a report for the target scope (Application, for example). See ASoC documentation for available scopes.
res = asoc.post(f"Reports/Security/{scope}/{app_id}", json=model)

if not res.ok:
    asoc.print_response_error(res)
    exit()

# Get the report ID from the response. 
# This ID will be used to poll for progress and download the report
report_info = res.json()
report_id = report_info["Id"]
out(f"Created report ID: {report_id}")

report_status = ReportStatusV2.Pending

# loop until status is other than "Pending", "Starting" or "Running"
while report_status.value < ReportStatusV2.Failed.value:
    res = asoc.get(f"Reports/{report_id}")
    report_info = res.json()
    report_status = ReportStatusV2[report_info["Status"]]
    progress = report_info["Progress"]
    out(f"Status: {report_status} - Progress {progress}")
    if report_status in [ReportStatusV2.Pending, ReportStatusV2.Starting, ReportStatusV2.Running]:
        time.sleep(10)

if report_status == ReportStatusV2.Failed:
    out("Report creation failed")
    exit(report_status)

if report_status == ReportStatusV2.Deleted:
    out("Report was already deleted")
    exit(report_status)

if report_status == ReportStatusV2.Ready:
    out("Report is ready for download")

# download the report, "ISO-8859-1" is the encoding of the ASoC report
asoc.download(f"Reports/Download/{report_id}", report_path, "ISO-8859-1")
    
out(F"Report downloaded to {report_path}")
