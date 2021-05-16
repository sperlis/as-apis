# as-apis
Learn AppScan APIs by example. Feel free to use or reuse, but keep in mind the code is provided according to the license. 

The intention is for you to take the scripts and use them as examples for your own scripts. While in Python, the logic is easily migrated into most languages.

For AppScan on Cloud, visit https://cloud.appscan.com/swagger/ui/index for details on the APIs.
For AppScan Enterprise, visit your local installation at https://{local}/ase/api/pages/apidocs.html for details on the APIs. (Note that "ase" may be replaced be a local instance name in your organization).

## Dependencies:
- Requests: https://requests.readthedocs.io/en/master/
Please make sure Requests is set up prior to running these scripts.

Use:
```
> pip install -r requirements.txt
```
to automate the install.

## Execution:
Example:
```
> py asocCreateReport.py
```

The intended execution is to run the individual functionality files to perform actions. Each logical action (according to my logic, which is of course different than everyone else's by definition) is in its own file. They are not necessarily atomic, but they do accomplish a specific target.

The basic execution configuration should be placed in `config.json`, read by default from the current directory. 

> **NOTE**

> You can get the sample `config.json` file programmatically:
>```
> > py config.py > config.json
>```

To use a configuration file that is not in the local directory or that uses a custom name, use the `configFile` command-line argument. This particularly useful.

Example:
```
> py asocCreateReport.py configFile='myDefaultReport.json'
```

Alternatively, the command line can be used to configure an execution, but this can be tedious for complex configuration, so the config file should always be used, and command line should only be used to override values.

All JSON file configuration items can be overridden in the command line. To override them, use the fully qualified path in the JSON object hierarchy to the specific item. For example, if we wanted to override the model item `Title` from "Report Name" to "My Special Report":
```
> py asocCreateReport.py asocReport.model.Configuration.Title="My Special Report"
```

Details about using the command-line can be found [here](./CLI.md).

> **NOTE**

> Before you proceed you should be familiar with the `Verbose` command-line option. 
> By default, the scripts only print out neccessary information. To get more information for the execution add `Verbose` to the command-line.
>```
> py asocCreateReport.py Verbose
>```
>Read more in the [CLI documentaion](CLI.md)

The config file has two types of nodes:
1. Service 
1. API models

The service nodes are general to the execution. They include things like the authentication keys required to access the service, definition of things that are common to most APIs, etc.

The API models include specific items required for specific API calls (or a set of API calls). These are both script configuration items and the API model itself. For example, the `AsocReport` node contains items such as the report file name and location (script configuration) and the `Model` object which is the actual API call body:

```
   "AsocReport": {
        "Name" : "report",
        "Path" : "./",
        "Model" : {
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
Here you can see `Name` and `Path` which tell the script where to store the file and what to call it, and the `Model` key contains the actual model as it appears in the ASoC API documentation.

### Service Nodes:
Please note that the configuration file is used by both AppScan on Cloud (ASoC) and AppScan Enterprise (ASE) scripts, which is why the sample contains both. The scripts are designed to reside together and executed from the same location, if you have both AppScan on Cloud and AppScan Enterprise and you'd like to automate both.

#### ASoC
`ASoC` object containing the Key ID and Secret required for authentication and authorizing.
#### ase
`ASE` object contains the Key ID and Secret that are required. However, since ASE allows it, the object also contains username and password. It is _**highly recommended**_ that you **do not** store usernames and passwords in configuration files. 
#### SubjectId
The ID of the subject of the API call. This can be an application ID, a scan ID, execution ID, user ID, and so on. Every item in ASoC has an ID, and can be the subject of an API call.
#### Scope
The scope is the subject _type_ of the API call. Scope currently includes Application, Scan, and ScanExecution, but the ASoC API documentation should be referred as more scopes may be available in the future. Most API calls have fixed subject (users, presences, asset-groups, etc.), however, a few (like reports) can have different subject types and the scope identifies it.
#### Host
The target host and should be in the form of `<scheme>//<host>:<port(options)>`. The default value is `https://cloud.appscan.com`. This is relevant when config file is used with ASE client, but that belongs to another project :smile:. We also use it for internal testing against development or staging environments. When working with ASoC there is no need to change this value.
#### APIVersion
_this is a placeholder for future updates_ 
#### IastConfig
_this is a placeholder for future updates_

<hr />

# The Scripts
Each script has configuration which may or may not be in the default configuration (most are).
Scripts that require an API model have a `ModelV?` in them. 
> Hint: when writing your own scripts, use the `get_model()` function to retrieve the model. It will ensure that you fetch the correct model object version from the configuration.

> Note: Only ASoC currently has a different set of API versions, so version support in not relevant for ASE

> One last Note: Object may not change 

## config.py
```
> py config.py
```
This script generates the JSON file used for configuration and writes it to stdout. The output is empty and can be saved for later update and use.

## configuration.py
```
> py configuration.py
```
When used with no command-line arguments, this script generates an empty configuration JSON and writes it to stdout. 
When used with command-line arguments, the script will update the configuration with the provided options, and output the resulting, updated, configuration.

If a config file is provided, it will be written out, with updates from the relevant provided command-line arguments.

Example: `> py configuration.py Host='https://www.example.com'` will output the default JSON configuration with the `Host` field updated to "https://www.example.com"

Example: `> py configuration.py configFile='myConfig.json' Host='https://www.example.com'` will output the content of `myConfig.json` with the `Host` field updated to "https://www.example.com"

## [ASoC Scripts](asoc.md)

## [ASE Scripts](ase.md)
