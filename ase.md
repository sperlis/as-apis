## aselib.py
```
> py aselib.py

More Examples:
> py aselib.py ASE.KeyId="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ASE.KeySecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

> py aselib.py ASE.Username="xx..xx" ASE.Password="**..**"
```
This script allows you to generate an `asc_session_id` from a username/password or Key ID and Secret. It can not be used in subsequent calls to other scripts, but it can be useful if you're generating REST calls yourself using another tool.

A side affect is also validation of connectivity and correctness of the credentials. Useful if you're having problems with extensions or plugins.

#### Configuration: `ASE`
1. `Host` is the name of the server. Required for ASE.
1. `Instance` is the instance ID which is defaulted to `ase` but can be changed by the customer (set in the Config Wizard)
1. `Verify` is used when the server-side certificate is self-signed or you'd like to ignore any errors

## aseDastScanCreate.py
```
> py aseDastScanCreate.py
```

In AppScan Enterprise, creating a scan is a 3 step operation. The first is to create the scan job, the second is to configure it, and a third is to run it.
This script is the first step in the chain creating a scan job (also known as "folder item") in a selected folder. It can also be associated with an application.

An ASE scan job must start with a basic template ID and with a selected test policy. There are defaults, but they must be explicitly identified.

#### Configuration: `AseDastScan`
1. `Template` is the name or ID of the base template. The API requires an ID, but the script will attempt to translate a name to an ID (for human friendliness)
1. `TestPolicy` is the name or ID of the test policy to be used. As with the template, the script will accept a name instead of an ID and translate it
1. `Folder` is the path of the folder to place the scan job. These can be in named-path form (`ASE/Users/MyFolder`) or the IDs of these folders (`1/2/17`)
1. `Application` is an optional association of the job with an application. You can specify a name or ID
1. `Name` is the name of the scan, and __must__ be unique in the folder. Using a duplicate name will result in a `409 CONFLICT` response code
1. `Description` is an optional description of the scan
1. `Contact` is an options field that provides a contact name for the scan. This is different from the creator of the scan which is set automatically.
1. `AutoConfig` instructs the script to proceed to the configuration operation automatically
1. `AutoRun` instructs the script to proceed to the run operation
1. `Configuration` is the list of configuration items to update in the job configuration, on top of the base template and any dast.config file that was associated with the scan. The structure of the configuration items is a 3 member tuple: `(name,value,encrypted)` (`encrypted` is only relevant if the value was copied from an existing scan template).

>Configuration items have an affinity to the scan-template format of AppScan Standard. To update items, the path is the xpath of the item in the scan-template XML.
>
>For example, setting the starting URL use the path `//ScanConfiguration/Application/StartingUrls` with the value `<StaringUrl>https://www.example.com</StartingUrl>`. 
>
>For convenience, there are shorthand names for the common configuration items.
>
>For example, the starting URL is shorthand `StartingUrl` and the value can simply be set to `https://www.example.com`. The server will insert them into the correct location in the scan-template. See the API documentation for the full list of shorthand names.

## aseDastScanConfig.py
```
> py aseDastScanConfig.py

to specify scan jon to configure
> py aseDastScanConfig.py SubjectId="{folder_item_i}"

to specify a starting point URL
> py aseDastScanConfig.py SubjectId="{folder_item_i}" AseDastScan.Configuration=[("StartingUrl","https://www.example.com",False)]

to specify a starting point URL and additional domains
> py aseDastScanConfig.py SubjectId="{folder_item_i}" AseDastScan.Configuration=[("AdditionalDomains","<AdditionalServers><AdditionalServer>.example.com</AdditionalServer><AdditionalServer>www.example.org</AdditionalServer></AdditionalServers>",False)]



```