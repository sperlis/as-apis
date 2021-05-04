import sys
import json
import os
import os.path
import ast
import re

from asapis.utils.printUtil import PrintLevel, out
from asapis.utils.defaultConfig import default_config

class Configuration:

    default_file = "./config.json"

    config = {}

    # Process the execution options.
    # If a named config file exists it gets loaded first
    # Command-line options override config file options
    # NOTE: at minimum, config-file/command-line must include authorization KeyId/KeySecret
    def __init__(self, config_values: dict):
        """Creates options object from the config file (default or named) with all the configuration items,
        overriding with any listed items (presumably from command-line parameters)

        Args:

        config_values: an array of items used to add or update the configuration
           1) named-items - in the form name=value (also name="value") where the name can be a path in the options object. 
              Value can be anything that evaluated by literal_eval (https://docs.python.org/3/library/ast.html#ast.literal_eval)
           2) flags - a single value, placed at the root of the options with a None value only to indicate it was set
        """
        config_prefix = re.compile("^-?configFile=", re.I)
        
        res = list(filter(lambda option: bool(config_prefix.match(option)), config_values))

        # read config file
        if len(res) > 0:
            file = config_prefix.sub("", res[0])
            # the first config file found is used
            self.__load_config(file)
        else: 
            self.__load_default_config()
            
        # Process the command-line. To override config file the format must be <name>=<value>
        # value-less options can also be provided (for custom execution flags) and they are
        # added with the value of 'None'. They are added at the root of the Options object:
        #     "<val>": None
        # This is just a placeholder, to indicate that the flag was set, the value is meaningless
        # (as it does not exist)
        for val in config_values:
            val = val.lstrip('-/')
            if bool(config_prefix.match(val)):
                continue
            eq = val.find('=')
            # unvalued flags
            if eq == -1:
                self.config[val] = None
            # named values
            else:
                name = val[0:eq]
                value = val[eq + 1:]
                self.__set_value(name, value)

        # Special handling for the print level which is set globally, even if access to options is not available
        # The use of os.environ allows always running in Verbose by setting the OS environment
        if "Verbose" in self.config:
            os.environ["AppScan_API_Verbose"] = ""
            out("Print level set to Verbose", level=PrintLevel.Verbose)


    def __load_config(self, config_file_path:str):
        if not os.path.exists(config_file_path) or not os.path.isfile(config_file_path):
            self.config = default_config
            out(f"\"{config_file_path}\" Custom file does not exist or path is not a file. Using default configuration")
        else:
            with open(config_file_path, "r") as config_file:
                self.config = json.load(config_file)
            out(f"Using configuration file: {config_file_path}")
    
    def __load_default_config(self):
        if os.path.exists(self.default_file):
            with open(self.default_file, "r") as config_file:
                self.config = json.load(config_file)
            out(f"Using configuration file: {self.default_file}")
        else:
            self.config = default_config
            out(f"Using default configuration", level=PrintLevel.Verbose)


    def __set_value(self, param, value):
        parts = param.split(".")
        member = parts[-1]
        del parts[-1]
        node = self.config
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

        new_value = value
        value_type = str
        failed_eval = False
        try:
            new_value = ast.literal_eval(value)
            value_type = type(new_value)
        except:
            new_value = new_value.strip("\"'")
            failed_eval = True

        if member in node:
            # member exist, so we handle existing, known type
            member_type = type(node[member])
            if value_type is member_type:
                node[member] = new_value
                out(f"Option overriding: {param} with {new_value}", level=PrintLevel.Verbose)
            elif failed_eval:
                out(f"Option overriding: Failed evaluating \"{value}\" for {param} of type '{member_type.__name__}'")
            else:
                out(f"Option overriding: Type mismatch for {param}. Expecting '{member_type.__name__}' and got '{value_type.__name__}'")
        else: 
            # new member, assigned the value and type as it was evaluated
            node[member] = new_value
            out(f"Option introducing: new {param} with {new_value} added", level=PrintLevel.Verbose)

    def print_config(self):
        out(json.dumps(self.config, indent=2))

if __name__ == "__main__":
    Configuration = Configuration(sys.argv[1:])
    Configuration.print_config()
