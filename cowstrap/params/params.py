
import copy
import os
import logging
import argparse

import cowstrap
import cowstrap.errors
import cowstrap.params.input

class Params(object):
    """
    Represents ALL configuration for a given run, including command line
    arguments, values from configuration files, and those input by users. Works
    as follows:

    Register all of the "values" that you want to include. The set of values
    must be known BEFORE any command-line arguments are parsed, so the caller
    is responsible for anything that could add new command-line arguments (ex:
    if you have a configurable plugin directory, apply that configuration
    first and then have each of the plugins register the values that they
    care about.)

    After all values are registered, call parse_arguments() to generate the
    Input(), which allows you to access any of the values.

    :ivar description: the purpose of the program. Will be printed with help.
    :type description: string
    :ivar config_path: location to look for configuration
    :type config_path: path
    :ivar _values: the set of all values that have been registered (mapped by
    name)
    :type _values: dict(string, cowstrap.params.value.Value)
    """

    def __init__(self, description, config_path=None):
        self.description = description
        self._values = {}
        if config_path == None:
            home = os.path.expanduser("~")
            #TODO: change file extension depending on OS
            config_path = os.path.join(home, 'cowstrap.ini')

        self.register_value(cowstrap.params.booleanvalue.BooleanValue(
            "interactive", default=True))
        self.register_value(cowstrap.params.filevalue.FileValue(
            "config", default=config_path))
        self.register_value(cowstrap.params.stringvalue.StringValue(
            "log_level"))

    def register_value(self, value):
        """
        Add a value to the set that will be parsed from arguments/config/user.

        Register all values that you might care about.

        :param value: the value that you may want some data for.
        :type  value: cowstrap.params.value.Value
        :raises: cowstrap.errors.DuplicateValueError
        """
        if value.name in self._values:
            raise cowstrap.errors.BadValueError("Duplicated " + value.name)
        self._values[value.name] = value

    def parse_arguments(self):
        """
        Call this after all values have been registered. No more can be
        registered after this point.
        """

        #read in any command line arguments
        arg_parser = argparse.ArgumentParser(description=self.description)
        for value in self._values.viewvalues():
            #TODO: go make this
            value.register(arg_parser)
        #TODO: if interactive is true, make sure that didn't throw an exception, except perhaps for --help?
        args = arg_parser.parse_args()

        #go load the config if it exists
        config = cowstrap.config.Config(args.config)

        #set log level ASAP (now)
        log_level_string = "INFO"
        if args.log_level:
            log_level_string = args.log_level
        elif config.has_data("log_level"):
            log_level_string = config.get_data("log_level")
        cowstrap.log.setLevel(getattr(logging, log_level_string.upper()))

        #create and return the input
        return cowstrap.params.input.Input(
            #TODO: clean up the way these special args are handled
            copy.deepcopy(self._values), args, config, is_interactive)

