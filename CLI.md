# API Command-Line

As noted, the command-line allows setting options.
The design is that all configuration is contained within a Options object, which gets populated from a configuration files and the command-line.
The configuration file can be expanded, but there are some applicative options that must be there for proper operation of the scripts (as they are, before you branch and make them your own :smile:).

Most of the command-line arguments are related to the performing operations. However, there are those that affect the general behavior:

1. namedConfigFile - this option allows you to specific a configuration file. Usage: `namedConfigFile="<path_to_file>"`

1. Verbose - this option outputs extended information regarding the execution. Usage: `Verbose`

Example:
```
> py asocCreateReport.py namedConfigFile="./reportConfig.json"
Using configuration file: ./reportConfig.json

> py asocCreateReport.py namedConfigFile="./reportConfig.json" Verbose
Using configuration file: ./reportConfig.json
Print level set to Verbose
```

## Terminology: Options vs Flags
Options are named values. They can have different values, and are accessed by their name. `namedConfigFile` above is a type of option whose value can be the path to any file.

Flags are switches that are either there or not. `Verbose` is a type of flag. It's simple appearance in the command-line indicates a state. 

## Command-line Values
For option values, we rely on [ast.literal_eval()](https://docs.python.org/3/library/ast.html#ast.literal_eval). While far from perfect, it does keep the code simple. The values can be anything that can be processed by [ast.literal_eval()](https://docs.python.org/3/library/ast.html#ast.literal_eval) with a fallback to [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str).

It also keeps the explanation simple :smile:

For example: `starts="('Jan 1', 'Feb 1', 'Mar 1')"`

Will get evaluated to a [tuple](https://docs.python.org/3/library/stdtypes.html#tuple):
```
>>> starts[0]
    'Jan 1'
>>> starts[1]
    'Feb 1'
>>> starts[2]
    'Mar 1'
```
Just like it would in code.

`starts="{'day1':'Jan 1', 'day2':'Feb 1', 'day3':'Mar 1'}"`

Will get evaluated to a [dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict):
```
>>> starts["day1"]
    'Jan 1'
>>> starts["day2"]
    'Feb 1'
>>> starts["day3"]
    'Mar 1'
```
Again, just like it would in code.

## Overriding Options
Any option in the configuration file can be overridden using the command-line:

 `> py myScript.py subjectId='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'`

will override the value of `subjectId` key in the options object.

To update values in internal object, the qualified path can be used:

`> py myScript.py asocDastScan.model.StartingUrl='https://demo.testfire.net'`

will override the `StartingUrl` key in the `model` member's object, under `asocDastScan`

As noted above, the evaluation of the value provided uses [ast.literal_eval()](https://docs.python.org/3/library/ast.html#ast.literal_eval). This means tha the data type is significant. Since the configuration JSON file provides us with a hint to the value type required, the processing will require that data type.

Example 1:
```
⋮
   "asocDastScan": {
        "file":"",
        "loginFile":"",
        "model": {
            "StartingUrl": "https://demo.testfire.net",
            ⋮
            "IncludeVerifiedDomains": true,
⋮
```
to update the staring URL, use a string:

`> py myScript.py asocDastScan.model.StartingUrl='https://demo.testfire.net'`

In this case, since the string is continuos you can do away with the quotes:

`> py myScript.py asocDastScan.model.StartingUrl=https://demo.testfire.net`

(since the fallback type is [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) and `StartingUrl` is a string, this will work)

To update the verified domains inclusion flag, use a bool:

`> py myScript.py asocDastScan.model.IncludeVerifiedDomains=True`

Note the capital T (for `True`). Since is a _literal_ evaluation, it must match Python syntax to work. using a lowercase t (for `true`) will yield:

`Option overriding: Failed evaluating "true" for asocDastScan.model.IncludeVerifiedDomains of type 'bool'`

Failing to match a type can cause another error. Calling:

`> py myScript.py asocDastScan.model.IncludeVerifiedDomains=4`

Will yield this error:

`Option overriding: Type mismatch for asocDastScan.model.IncludeVerifiedDomains. Expecting 'bool' and got 'int'`

### Overriding whole objects
This is, of course an option. However, it is _strongly recommended_ not to exercise this option.
When overriding objects there is no type-checking and the objects aren't merged, they are completely overridden.

Existing config:
```
⋮
"asoc" : {
        "KeyId":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "KeySecret":"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    },
⋮
```

Command-line:

`> py myScript.py asoc={"KeyId":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx","KeySecret":"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"}`

This will work OK. However, this will also work OK:

`> py myScript.py asoc={"KeyId":True,"KeySecret":False}`

but of course, break the logic of the application. Avoid this unless any other object is completely unreasonable.

## Custom Options
Any command-line option set in the form form of name=value will be treated as a configuration item and added to the options object in __relative hierarchy__.

This means that the periods in the name are treated as paths in the options object:
Example: `> py myScript.py doAlerts=True`
```
asoc = ASoC()
shouldDoAlerts = asoc["doAlerts"]
```
However, `> py myScript.py custom.doAlerts=True`
```
asoc = ASoC()
shouldDoAlerts = asoc["custom"]["doAlerts"]
```
This also allows you to set your own custom object:

`> py myScript.py custom="{'doAlerts':True,'volume':'VeryLoud'}`

Code will be:
```
asoc = ASoC()
shouldDoAlerts = asoc.Options["custom"]["doAlerts"]
howLoud = asoc.Options["custom"]["volume"]
```
## Custom Flags
You can create your own custom flags to use in your own code simply by specifying them on the command line. They are added, as-is, to the root of the options object and to use them simple check they exist or not.
For example: `> py myScript.py doAlerts`

In the code, you can simple check:
```
asoc = ASoC()
shouldDoAlerts = 'doAlerts' in asoc.Options
```
Flags are not hierarchial. This means that a flag name can contain dots:

Example: `> py myScript.py do.Alerts`

```
asoc = ASoC()
shouldDoAlerts = 'do.Alerts' in asoc.Options
```