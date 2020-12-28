import json
import os
import os.path
import ast

from asapis.utils.printUtil import PrintLevel, out

class OptionsProcessor:

    root = os.path.dirname(os.path.abspath(__file__))
    __defaultConfigFile = os.path.join(root,"../../data/config.json")

    # process the execution options.
    # if a named config file exists it gets loaded first
    # command-line options override config file options
    # NOTE: at minimum, config file/command line must include authorization KeyId/KeySecret
    @staticmethod
    def getOptions(configValues: dict)-> dict:
        """Creates options object from the config file (default or named) with all the configuration items,
        overriding with any listed items (presumably from command-line parameters)

        Args:

        configValue: an array of items used to add or update the configuration
           1) named-items - in the form name=value (also name="value") where the name can be a path in the options object. 
              Value can be anything that evaluated by literal_eval (https://docs.python.org/3/library/ast.html#ast.literal_eval)
           2) flags - a single value, placed at the root of the options with a None value only to indicate it was set
        """

        options = {}
        configPrefix = "namedConfigFile="
        res = list(filter(lambda option: option.startswith(configPrefix), configValues))

        # read config file
        if len(res) > 0:
            # the first config file found is used
            options = OptionsProcessor.__loadConfig(res[0][len(configPrefix):])
        else: 
            options = OptionsProcessor.__loadConfig()
            
        # process command-line. To override config file the format must be <name>=<value>
        # value-less options can also be provided (for custom execution flags) and they are
        # added with the value of 'None'. They are added at the root of the Options object:
        #     "<val>": None
        # this is just a placeholder, to indicate that the flag was set, the value is meaningless
        # (as it does not exist)
        for val in configValues:
            val = val.lstrip('-')
            if val.startswith(configPrefix):
                continue
            eq = val.find('=')
            # unvalued flags
            if eq == -1:
                options[val] = None
            # named values
            else:
                name = val[0:eq]
                value = val[eq + 1:]
                OptionsProcessor.__setValue(options, name, value)

        # Special handling for the print level which is set globally, even if access to options is not available
        # The use of os.environ allows always running in Verbose by setting the OS environment
        if "Verbose" in options:
            os.environ["AppScan_API_Verbose"] = ""
            out("Print level set to Verbose", level=PrintLevel.Verbose)

        return options

    @staticmethod
    def __loadConfig(configFilePath = None):
        if configFilePath is None:
            configFilePath = OptionsProcessor.__defaultConfigFile
            out(f"Using configuration file: {configFilePath}")
        elif not os.path.exists(configFilePath) or not os.path.isfile(configFilePath):
            configFilePath = OptionsProcessor.__defaultConfigFile
            out(f"\"{configFilePath}\" Custom file does not exist or path is not a file. Reverting to local {OptionsProcessor.__defaultConfigFile}.")
        else:
            out(f"Using configuration file: {configFilePath}")

        options = {}
        with open(configFilePath, "r") as config:
            options = json.load(config)

        return options

    @staticmethod
    def __setValue(options, param, value):
        parts = param.split(".")
        member = parts[-1]
        del parts[-1]
        node = options
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

        newValue = value
        valueType = str
        failedEval = False
        try:
            newValue = ast.literal_eval(value)
            valueType = type(newValue)
        except:
            newValue = newValue.strip("\"'")
            failedEval = True

        # handle existing, known type
        if member in node:
            memberType = type(node[member])
            if valueType is memberType:
                node[member] = newValue
                out(f"Option overriding: {param} with {newValue}", level=PrintLevel.Verbose)
            elif failedEval:
                out(f"Option overriding: Failed evaluating \"{value}\" for {param} of type '{memberType.__name__}'")
            else:
                out(f"Option overriding: Type mismatch for {param}. Expecting '{memberType.__name__}' and got '{valueType.__name__}'")
        else: # new member, assigned the value and type as it was evaluated
            node[member] = newValue
            out(f"Option introducing: new {param} with {newValue} added", level=PrintLevel.Verbose)

