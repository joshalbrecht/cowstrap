
class Command(object):
    """
    Represents top-level commands that can be entered by a user.

    :ivar name: name by which the user will call this command
    :type name: string
    :ivar _actions: list of actions that make up this command
    :type _actions: list(cowstrap.actions.action.Action)
    """

    def __init__(self, name, actions):
        self.name = name
        self._actions = actions

    def register(self, parser):
        """
        Set up the subparser for command line arguments

        :param parser: the subparser to configure
        :type  parser: argparse.ArgumentParser
        """
        for action in self._actions:
            action.register(parser)

    def run(self, arguments, config):
        """
        Perform the indicated command with the parsed command line args

        :param arguments: the subparser to configure
        :type  arguments: argparse.Namespace
        :param config: contains persisted user data
        :type  config: cowstrap.config.Config
        """
        previous_fields = set()
        for action in self._actions:
            action.configure(config, arguments, previous_fields)
            for field in action.generated_fields:
                previous_fields.add(field)
        for action in self._actions:
            action.perform()
