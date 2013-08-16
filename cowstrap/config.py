
import os
import ConfigParser

import cowstrap
import cowstrap.errors

SECTION = "cowstrap"

class Config(object):
    """
    Represents all persistent configuration

    :ivar path: the path to the configuration file (may or may not exist)
    :type path: string
    """

    def __init__(self, path):
        self.path = path
        self._data = {}
        self._load()

    def has_data(self, name):
        """
        :param name: the name of the configuration variable
        :type  name: string
        :returns: True iff this config has the desired data
        :rtype:   boolean
        """
        return name in self._data

    def get_data(self, name):
        """
        :param name: the name of the configuration variable
        :type  name: string
        :raises: cowstrap.errors.BadValueError if there is no value
        :returns: the data associated with this name
        :rtype:   string
        """
        if not self.has_data(name):
            raise cowstrap.errors.BadValueError("No config value found for " + \
                                                name)
        return self._data[name]

    def set_data(self, name, value):
        """
        Will persist this value to disk.

        :param name: the name of the configuration variable
        :type  name: string
        :param value: the name of the configuration variable
        :type  value: string
        """
        self._data[name] = value
        self._save()

    def _load(self):
        """
        Load the configuration from disk.
        """
        if not os.path.exists(self.path):
            cowstrap.log.warn("Could not load config from " + self.path)
            return
        try:
            config = ConfigParser.RawConfigParser()
            config.read(self.path)
            new_data = {}
            for key in config.options(SECTION):
                new_data[key] = config.get(SECTION, key)
            self._data = new_data
        except EnvironmentError, e:
            cowstrap.log.warn("Could not load file: {0}", e)

    def _save(self):
        """
        Save the configuration to disk.
        """
        try:
            config = ConfigParser.RawConfigParser()
            config.add_section(SECTION)
            for key, value in self._data.viewitems():
                config.set(SECTION, key, value)
            with open(self.path, 'wb') as out_file:
                config.write(out_file)
        except EnvironmentError, e:
            cowstrap.log.warn("Could not save to file: {0}", e)
