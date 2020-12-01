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
    # NOTE: at miniumum, config file/command line must include authorization KeyId/KeySecret
    def getCommandLineOptions(self):
        if (not self.Options):
            # read config file
            self.loadConfig()
                
            # process command-line. To override config file the format must be <name>=<value>
            # if explicit name is not provided to the option, a "$clp<index>" name is gerneated
            index = 0
            for val in sys.argv:
                eq = val.find('=')
                if eq == -1:
                    self.Options["$clp" + str(index)] = val
                    index += 1
                else: 
                    self.setValue(val[0:eq],val[eq+1:])

        return self.Options

    def loadConfig(self):
        config = open("config.json","r")
        self.Options = json.load(config)
        config.close()

    def setValue(self, param, value):
        parts = param.split(".")
        memeber = parts[-1]
        del parts[-1]
        node = self.Options
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]
        if value.startswith("\""):
            node[memeber] = value.strip("\"")
        elif re.match("\\d+",value):
            node[memeber] = int(value)
        else:
            try:
                node[memeber] = bool(util.strtobool(value))
            except ValueError:
                print(f"Value is invalid: {value}\n(hint: strings should always be in double-quotes - ...=\"value\"")

    # provides an option value given a specific name
    def Option(self, name):
        if (self.Options):
            return self.Options[name]
