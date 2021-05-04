default_config = {
    "ASoC" : {
        "KeyId": "",
        "KeySecret": "",
        "Host": "",
        "APIVersion": "2"
    },
    "ASE" : {
        "KeyId": "",
        "KeySecret": "",
        "Username": "",
        "Password": "",
        "Host": "",
        "Instance": "ase",
        "Verify": True
    },
    "SubjectId": "",
    "Scope": "",
    "IASTConfig": "",
    "Host": "",
    "AsocReport": {
        "Name" : "report",
        "Path" : "./",
        "ModelV2" : {
                "Configuration": {
                    "Summary": True,
                    "Details": True,
                    "Discussion": True,
                    "Overview": True,
                    "TableOfContent": True,
                    "Advisories": True,
                    "FixRecommendation": True,
                    "History": True,
                    "Coverage": True,
                    "IsTrialReport": True,
                    "MinimizeDetails": False,
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
    },
    "AsocDastScan": {
        "File": "",
        "LoginFile": "",
        "ModelV2": {
            "ScanFileId": "",
            "TestOnly": False,
            "StartingUrl": "",
            "LoginUser": "",
            "LoginPassword": "",
            "TestPolicy": "",
            "ExtraField": "",
            "ScanType": "Production",
            "PresenceId": "00000000-0000-0000-0000-000000000000",
            "IncludeVerifiedDomains": True,
            "HttpAuthUserName": "",
            "HttpAuthPassword": "",
            "HttpAuthDomain": "",
            "OnlyFullResults": True,
            "TestOptimizationLevel": "NoOptimization",
            "LoginSequenceFileId": "00000000-0000-0000-0000-000000000000",
            "ScanName": "",
            "EnableMailNotification": True,
            "Locale": "en-US",
            "AppId": "",
            "Execute": True,
            "Personal": False,
            "ClientType": "ASoC-API-Samples"
          }
    },
    "AsocSastScan": {
        "File": "",
        "ModelV2": {
            "ApplicationFileId": "",
            "ScanName": "",
            "EnableMailNotification": True,
            "Locale": "en-US",
            "AppId": "",
            "Execute": True,
            "Personal": False,
            "ClientType": "ASoC-API-Samples"
        }
    },
    "ScanMonitor": {
        "Automatic": False,
        "Continuos": False,
        "TimeSpanSeconds": 100
    },
    "AseDastScan": {
        "Template": "Regular Scan",
        "TestPolicy": "Default", # policy ID - Application Only
        "Folder": "",       # ASE folder ID
        "Application": "",  # No application specified
        "Name": "My Scan",
        "Description": "",
        "Contact": "",
        "AutoConfig": True,
        "AutoRun": True,
        "Configuration": [
            ["StartingUrl","",False],
            ["LoginUsername","",False],
            ["LoginPassword","",True],
            ["LoginMethod","",False],
            ["CustomHeaders","",False],
            ["TestOptimizationConfiguration","",False],
            ["AccountLockout","",False],
            ["AdditionalDomains","",False],
            ["Exclusions","",False],
            ["//ScanConfiguration/Communication/NumberOfThreads",None,False]
        ]
    }
}
	
