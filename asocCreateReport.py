from asoclib import ASoC
from asocEnums import ReportStatus
import requests
import time
import codecs
import os.path

asoc = ASoC()


# initialize variables from the options
appId = asoc.Options["appId"]

# the model is read as-is, but can be programatically manipulated here
config = asoc.Options["asocReport"]["model"]

reportName = asoc.Options["asocReport"]["name"] + "." + config["Configuration"]["ReportFileType"]
reportPath = os.path.join(asoc.Options["asocReport"]["path"],reportName)

# create a report for the 
res = asoc.post(f"https://cloud.appscan.com/api/v2/Reports/Security/Application/{appId}", json=config)

if (not res.ok):
    # TODO - add a clear message
    exit()

# Get the report ID from the response. 
# This ID will be used to poll for progress and download the report
reportInfo = res.json()
reportId = reportInfo["Id"]
print(f"{reportId}")

reportStatus = ReportStatus.Pending

# loop until status is other than "Pending", "Starting" or Running"
while (reportStatus.value < ReportStatus.Failed.value ):
    res = asoc.get(f"https://cloud.appscan.com/api/v2/Reports/{reportId}")
    reportInfo = res.json()
    reportStatus = ReportStatus[reportInfo["Status"]]
    progress = reportInfo["Progress"]
    print(f"Status: {reportStatus} - Progress {progress}")
    if (reportStatus is ReportStatus.Pending or reportStatus is ReportStatus.Running):
        time.sleep(10)

if(reportStatus == ReportStatus.Failed):
    print("Report creation failed")
    exit(reportStatus)

if(reportStatus == ReportStatus.Deleted):
    print("Report was already deleted")
    exit(reportStatus)

if(reportStatus == ReportStatus.Ready):
    print("Report is ready for download")

# download the report
# TODO handle very large reports (so the whole file isn't kept in memory)
res = asoc.get(f"https://cloud.appscan.com/api/v2/Reports/Download/{reportId}")
f = codecs.open(reportPath, "w", "ISO-8859-1") # this is the UNICODE encoding used in ASoC reporting
f.write(res.text)
f.close()
print(F"Report downloaded to {reportPath}")
