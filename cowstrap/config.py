
import os

class Config(object):
    """
    Represents all persistent configuration

    :ivar config_path: the path to the configuration file (may or may not exist)
    :type config_path: string
    """

    def __init__(self, config_path):
        self.config_path = config_path
        if os.path.exists(config_path):
            self.load()

    def has_data(self, name):
        raise NotImplementedError()

    def get_data(self, name):
        raise NotImplementedError()

    def load(self):
        """
        Load the configuration from disk.
        """
        raise NotImplementedError()

    def save(self):
        """
        Save the configuration to disk.
        """
        raise NotImplementedError()
