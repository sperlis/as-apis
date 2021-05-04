## asoclib.py
```
> py asoclib.py
or
> py asoclib.py ASoC.KeyId="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" ASoC.KeySecret="********************************************"
```
This script allows you to generate an Access Token from an API Key to be used. It can not be used in subsequent calls to other scripts, but it can be useful if you're generating REST calls yourself using another tool.

A side affect is also validation of connectivity and correctness of the API Key. Useful if you're having problems with extensions or plugins.

## asocUploadFile.py
```
> py asocCreateReport.py filePath="<file_to_upload>"
```
This script is used to upload a file for future use. 

For example, running a SAST scan requires an IRX file to be uploaded first. The file can be provided to the script, but the actions can be separated. The resulting ID can be provided to `asocSastScan.py` directly, so the upload action isn't part of that script's execution (see `asocSastScan.py` documentation for a better explanation).

The output of the script is the ID of the uploaded file. Save this ID for future use (you have 30 minutes before file is automatically deleted).

## asocCreateReport.py
```
> py asocCreateReport.py
```
This script is used to generate a report. There are three steps - create the report, poll the status until the report is ready, and download the report.
#### Configuration: `AsocCreateReport`
1. `Name` is the report file name. There is no need to add a suffix, as the report file type will be automatically appended (html, pdf, etc.).
1. `Path` is the store location of the resulting report.
1. `ModelV?` is the actual REST API JSON model that is used. You can set defaults here, and override with the command-line.

## asocDastScan.py
```
> py asocDastScan.py
```
This script is used to execute a DAST scan. Optionally, it can upload a scan/scant (template) file and/or a recorded login file before executing the scan.
#### Configuration: `AsocDastScan`
1. `File` is the path to the scan or scant files that is to be used as the base of the scan (file must end with )
1. `LoginFile` is the path to a recorded login file.
1. `ModelV?` is the actual REST API model that is used. The IDs of the uploaded files will be added automatically, or you can use IDs of previously uploaded files set directly in the model.

## asocSastScan.py
```
> py asocSastScan.py
```
This script is used to execute a SAST scan. Unlike DAST where a related file is optional, SAST _requires_ a application file (IRX) to be uploaded. The IRX is generated using the SAClient command-line tool that can be downloaded here: [SAST Client Util / CLI](https://cloud.appscan.com/ui-v2/home/plugins). Once created, the IRX can be uploaded separately and the resulting ID provided to the script. If the path to the IRX is provided to `asocSastScan.py` it will be automatically uploaded and the ID used to create the scan.
#### Configuration: `AsocSastScan`
1. `File` is the path to the IEX files to be used in the scan. If set, it will be automatically uploaded.
1. `ModelV?` is the actual REST API model that is used. The ID of the uploaded file will be added automatically, or you can use an ID of a previously uploaded file set directly in the model.

## asocScanMonitor.py
```
> py asocScanMonitor.py
```
This script is used to monitor the progress of scans as they are executed. 

If set to automatic, a monitoring will start automatically after starting a scan. 

#### Configuration: `AsocScanMonitor`
1. `Automatic` will start monitoring automatically after starting a DAST or SAST scans.
1. `Continuos` will repeatably poll (in `TimeSpanSeconds` intervals) for the scan status (and not just once and then exit).
1. `TimeSpanSeconds` indicates how ofter to poll for progress, if `Continuos` is set to `True`. The time span is in seconds.

Examples:

Once:
```
> py asocScanMonitor.py SubjectId="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" AsocMonitorScan.Continuos=False
```
Repeated (every 100 seconds):
```
> py asocScanMonitor.py SubjectId="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" AsocMonitorScan.Continuos=True AsocMonitorScan.TimeSpanSeconds=100
```

## 