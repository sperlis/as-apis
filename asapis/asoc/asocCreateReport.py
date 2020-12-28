import time
import codecs
import os.path

from asapis.services.asoclib import ASoC
from asapis.asoc.asocEnums import ReportStatus
from asapis.utils.printUtil import out

asoc = ASoC()


# initialize variables from the options
appId = asoc.Options["subjectId"]
scope = asoc.Options["scope"]

# the model is used as-is, but can be programmatically manipulated here
config = asoc.Options["asocReport"]["model"]

# create a report file name with extension based on the report type
reportType = config["Configuration"]["ReportFileType"]
reportName = asoc.Options["asocReport"]["name"]
reportName = reportName + "." + reportType.lower()

reportPath = os.path.join(asoc.Options["asocReport"]["path"],reportName)

# create a report for the target scope (Application, for example). See ASoC documentation for available scopes.
res = asoc.post(f"Reports/Security/{scope}/{appId}", json=config)

if not res.ok:
    asoc.printResponseError(res)
    exit()

# Get the report ID from the response. 
# This ID will be used to poll for progress and download the report
reportInfo = res.json()
reportId = reportInfo["Id"]
out(f"Created report ID: {reportId}")

reportStatus = ReportStatus.Pending

# loop until status is other than "Pending", "Starting" or "Running"
while reportStatus.value < ReportStatus.Failed.value:
    res = asoc.get(f"Reports/{reportId}")
    reportInfo = res.json()
    reportStatus = ReportStatus[reportInfo["Status"]]
    progress = reportInfo["Progress"]
    out(f"Status: {reportStatus} - Progress {progress}")
    if reportStatus in [ReportStatus.Pending, ReportStatus.Starting, ReportStatus.Running]:
        time.sleep(10)

if reportStatus == ReportStatus.Failed:
    out("Report creation failed")
    exit(reportStatus)

if reportStatus == ReportStatus.Deleted:
    out("Report was already deleted")
    exit(reportStatus)

if reportStatus == ReportStatus.Ready:
    out("Report is ready for download")

# download the report
# TODO handle very large reports (so the whole file isn't kept in memory)
res = asoc.get(f"Reports/Download/{reportId}")

# this is the UNICODE encoding used in ASoC reporting
with codecs.open(reportPath, "w", "ISO-8859-1") as reportFile:
    reportFile.write(res.text)
    
out(F"Report downloaded to {reportPath}")
