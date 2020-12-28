# asoc-apis
Learn ASoC APIs by example. Feel free to use or reuse, but keep in mind the code is provided according to the license. 

The intention is for you to take the scripts and use them as examples for your own scripts. While in Python, the logic is easily migrated into most languages.

Visit https://cloud.appscan.com/swagger/ui/index for details on how to use the APIs.

## Dependencies:
- Requests: https://requests.readthedocs.io/en/master/
Please make sure Requests is set up prior to running these scripts.

## Execution:
Example:
```
py asocCreateReport.py
```

The intended execution is to run the individual functionality files to perform actions. Each logical action (according to my logic, which is of course different than everyone else's by definition) is in its own file. They are not necessarily atomic, but they do accomplish a specific target.

The basic execution configuration should be placed in `config.json`, read by default from the current directory. 

> **NOTE**

> To use a configuration file that is not in the local directory or that uses a custom name, use the `namedConfigFile` command-line argument.

> Example:
>```
>py asocCreateReport.py namedConfigFile='myDefaultReport.json'
>```

Alternatively, the command line can be used to configure an execution, but this can be tedious for complex configuration, so the config file should always be used, and command line should only be used to override values.

All JSON file configuration items can be overridden in the command line. To override them, use the fully qualified path in the JSON object hierarchy to the specific item. For example, if we wanted to override the model item `Title` from "Report Name" to "My Special Report":
```
py asocCreateReport.py asocReport.model.Configuration.Title="My Special Report"
```

More details on using the command-line can be found [here](./CLI.md).

The config file has two types of nodes:
1. Service 
1. API models

The service nodes are general to the execution. They include things like the keys required to accessing the service, definition of things that are common to most APIs, etc.

The API models include specific items required for specific API calls (or a set of API calls). These are both script configuration items and the API model itself. For example, the `asocReport` node contains items such as the report file name and location (script configuration) and the `model` object which is the actual API call body:

```
   "asocReport": {
        "name" : "report",
        "path" : "./",
        "model" : {
            "Configuration": {
                "Summary": true,
                "Details": true,
                "Discussion": true,
                "Overview": true,
                "TableOfContent": true,
                "Advisories": true,
                "FixRecommendation": true,
                "History": true,
                "Coverage": true,
                "IsTrialReport": true,
                "MinimizeDetails": false,
                "ReportFileType": "Html",
                "Title": "Report Name",
                "Notes": "Notes",
                "Locale": "en-US"
            },
            "OdataFilter": "",
            "ApplyPolicies": "None",
            "SelectPolicyIds": [
                "00000000-0000-0000-0000-000000000000"
            ]
        }
```
Here you can see `name` and `path` which tell the script where to store the file and what to call it, and the `model` key contains the actual model as it appears in the ASoC API documentation.

### Service Nodes:
Please note that the configuration file is used by both ASoC and ASE scripts, which is why the sample contains both. The scripts are designed to reside together and executed from the same location, if you have both AppScan on Cloud and AppScan Enterprise and you'd like to automate both.

#### asoc
`asoc` object contains the Key ID and Secret that are required.
#### ase
`ase` object contains the Key ID and Secret that are required. However, since ASE allows it, the object also contains username and password. It is _**highly recommended**_ that you do not store usernames and passwords in configuration files. ASE, since it's a local service, also requires the specific host to be used. 
#### subjectId
The ID of the subject of the API call. This can be an application ID, a scan ID, execution ID, user ID, and so on. Every item in ASoC has an ID, and can be the subject of an API call.
#### scope
The scope is the subject _type_ of the API call. Scope currently includes Application, Scan, and ScanExecution, but the ASoC API documentation should be referred as more scopes may be available in the future. Most API calls have fixed subject (users, presences, asset-groups, etc.), however, a few (like reports) can have different subject types and the scope identifies it.
#### host
The target host and should be in the form of `<scheme>//<host>:<port(options)>`. The default value is `https://cloud.appscan.com`. This is relevant when config file is used with ASE client, but that belongs to another project :smile:. We also use it for internal testing against development or staging environments. When working with ASoC there is no need to change this value.
#### apiVersion
_this is a placeholder for future updates_ 
#### iastConfig
_this is a placeholder for future updates_

<hr />

## asocCreateReport.py
```
py asocCreateReport.py
```
This script is used to generate a report. There are three steps - create the report, poll the status until the report is ready, and download the report.
#### Configuration:
`name` is the report file name. There is no need to add a suffix, as the report file type will be automatically appended (html, pdf, etc.).

`path` is the store location of the resulting report.

`model` is the actual REST API JSON model that is used. You can set defaults here, and override with the command-line.

