
class Machine(object):
    """
    Represents the data for a machine. Should be considered immutable after
    initialization.
    """

    #this is here because we don't accidentally want to set mispelled attrs
    __slots__ = [
        'name',
        'host',
        'port',
        'operating_system',
        'user_name',
        'password',
        'key_path',
    ]

    def __init__(self):
        self.name = None
        self.host = None
        self.port = None
        self.operating_system = None
        self.user_name = None
        self.password = None
        self.key_path = None

    @staticmethod
    def from_dict(json_dict):
        """
        Initialize a machine instance from a dictionary

        :param json_dict: the data to initialize with
        :type  json_dict: dict(string, object)
        :returns: a newly initialized machine
        :rtype:   cowstrap.machine.Machine
        """
        machine = Machine()
        for key, value in json_dict.viewitems():
            setattr(machine, key, value)
        return machine
