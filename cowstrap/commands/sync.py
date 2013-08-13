
import cowstrap.actions.bootstrap
import cowstrap.actions.synchronize
import cowstrap.commands.command

class Sync(cowstrap.commands.command.Command):
    """
    User command to synchronize the development environment of a given machine.
    """

    def __init__(self, ):
        cowstrap.commands.command.Command.__init__(self, "sync", [
            cowstrap.actions.bootstrap.Bootstrap(allow_new=True),
            cowstrap.actions.synchronize.Synchronize(),
        ])
