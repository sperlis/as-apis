import sys
import json
import re
from distutils import util

class BaseServiceLib(object):
    # hold the execution options
    # the only mandatory fields are KeyId/KeySecret
    Options = {}

    # process the command-line options and performs the initial authorization with ASoC
    def __init__(self):
        self.getCommandLineOptions()

    # process the execution options.
    # If a config file exists it gets loaded first
    # command-line options override config file options
    # NOTE: at minimum, config file/command line must include authorization KeyId/KeySecret
    def getCommandLineOptions(self):
        if (not self.Options):
            # read config file
            self.loadConfig()
                
            # process command-line. To override config file the format must be <name>=<value>
            # if explicit name is not provided to the option, a "$clp<index>" name is generated
            index = 0
            for val in sys.argv:
                eq = val.find('=')
                if eq == -1:
                    self.Options["$clp" + str(index)] = val
                    index += 1
                else: 
                    self.setValue(val[0:eq],val[eq + 1:])

        return self.Options

    def loadConfig(self):
        # TODO allow specifying a custom config file name
        with open("config.json", "r") as config:
            self.Options = json.load(config)

    def setValue(self, param, value):
        parts = param.split(".")
        member = parts[-1]
        del parts[-1]
        node = self.Options
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]
        if value[0] in ['"','\'']:
            node[member] = value.strip("\"'")
        elif re.match("^\\d+$",value):
            node[member] = int(value)
        else:
            try:
                node[member] = bool(util.strtobool(value))
            except ValueError:
                print(f"Value is invalid: {value}\n(hint: strings should always be in double-quotes - ...=\"value\"")


