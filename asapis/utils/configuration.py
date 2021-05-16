import sys
import json
import os
import os.path
import ast
import re

from asapis.utils.printUtil import PrintLevel, logger
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
        config_values = self.__handle_specials(config_values)
           
        # Process the command-line. To override config file the format must be <name>=<value>
        # value-less options can also be provided (for custom execution flags) and they are
        # added with the value of 'None'. They are added at the root of the Options object:
        #     "<val>": None
        # This is just a placeholder, to indicate that the flag was set, the value is meaningless
        # (as it does not exist)
        for val in config_values:
            val = val.lstrip('-/')
            eq = val.find('=')
            # unvalued flags
            if eq == -1:
                self.config[val] = None
            # named values
            else:
                name = val[0:eq]
                value = val[eq + 1:]
                self.__set_value(name, value)

    # Handle special options that affect following execution

    def __handle_specials(self, config_values:dict):
        specials_pattern = re.compile("(-?Verbose)|(-?Silent)|(^-?configFile=)", re.I)

        specials = list(filter(lambda option: bool(specials_pattern.match(option)), config_values))

        explicit_verbose = False
        explicit_config = None
        os.environ["AppScan_API_Log_Level"] = "Normal"
        for special in specials:
            if special.lower() == "verbose":
                os.environ["AppScan_API_Log_Level"] = "Verbose"
                logger("Print level set to Verbose", level=PrintLevel.Verbose)
                explicit_verbose = True
            elif special.lower() == "silent" and not explicit_verbose: # Verbose trumps Silent
                os.environ["AppScan_API_Log_Level"] = "Silent"
            elif not explicit_config and special.lower().count("configfile") != 0:
                # get config file from option
                # the first file is used
                explicit_config = specials_pattern.sub("", special)

        if explicit_config:
            self.__load_config(explicit_config)
        else: self.__load_default_config()
        
        return list(set(config_values) - set(specials))

    def __load_config(self, config_file_path:str):
        if not os.path.exists(config_file_path) or not os.path.isfile(config_file_path):
            self.config = default_config
            logger(f"\"{config_file_path}\" Custom file does not exist or path is not a file. Using default configuration")
        else:
            with open(config_file_path, "r") as config_file:
                self.config = json.load(config_file)
            logger(f"Using configuration file: {config_file_path}")
    
    def __load_default_config(self):
        if os.path.exists(self.default_file):
            with open(self.default_file, "r") as config_file:
                self.config = json.load(config_file)
            logger(f"Using configuration file: {self.default_file}")
        else:
            self.config = default_config
            logger(f"Using default configuration", level=PrintLevel.Verbose)


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
                logger(f"Option overriding: {param} with {new_value}", level=PrintLevel.Verbose)
            elif failed_eval:
                logger(f"Option overriding: Failed evaluating \"{value}\" for {param} of type '{member_type.__name__}'")
            else:
                logger(f"Option overriding: Type mismatch for {param}. Expecting '{member_type.__name__}' and got '{value_type.__name__}'")
        else: 
            # new member, assigned the value and type as it was evaluated
            node[member] = new_value
            logger(f"Option introducing: new {param} added with {new_value}", level=PrintLevel.Verbose)

    def print_config(self):
        logger(json.dumps(self.config, indent=2))

if __name__ == "__main__":
    Configuration = Configuration(sys.argv[1:])
    Configuration.print_config()
