
class Config(object):
    """
    Represents all persistent configuration

    :ivar config_path: the path to the configuration file (may or may not exist)
    :type config_path: string
    """

    def __init__(self):
        self.config_path = None

    # pylint: disable=R0201
    def register(self, parser):
        """
        Set up the command line parser to interact with configuration values

        :param parser: the subparser to configure
        :type  parser: argparse.ArgumentParser
        """
        parser.add_argument('-x', type=int, default=1)
        parser.add_argument('y', type=float)
        parser.set_defaults(func=foo)

