
import cowstrap.actions.action

class Synchronize(cowstrap.actions.action.Action):
    """
    Ensure that the machine development environment is up to date. This entails:

    - Checking out the correct git project and branch/tag
    - Applying any puppet scripts in that checkout to the machine
    """

    def __init__(self):
        cowstrap.actions.action.Action.__init__(self, set(["machine"]))

    def configure(self, config, arguments, previous_fields):
        #github project and branch/tag
        #puppet directories if non-standard
        pass
