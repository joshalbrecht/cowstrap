
import cowstrap.machinedict

class Provider(object):
    """
    Provides basic interaction with a service that lets you manipulate vms

    :ivar operating_systems: a list of operating systems that can be created
    :type operating_systems: list(string)
    :ivar machine_types: a list of valid machine types (sizes, etc)
    :type machine_types: list(string)

    :ivar _machine_dict: a reference for the details of all machines that exist
    :type _machine_dict: cowstrap.machinedict.MachineDictionary
    """

    def __init__(self, operating_systems, machine_types):
        self.operating_systems = operating_systems
        self.machine_types = machine_types
        self._machine_dict = cowstrap.machinedict.MachineDictionary()

    def exists(self, name):
        """
        :param name: a unique name or id for the machine.
        :type  name: string
        :returns: True iff the machine exists in the machine dictionary
        :rtype:   boolean
        """
        return name in self._machine_dict

    def is_running(self, name):
        """
        :param name: a unique name or id for the machine.
        :type  name: string
        :returns: True iff the machine is running
        :rtype:   boolean
        """
        return self._is_running(self._get_machine(name))

    # pylint: disable=R0913
    def create(self, name, operating_system, machine_type, user_name="cowstrap",
               password='', key_path=None, host=None, port=22):
        """
        :param name: a unique name or id for the machine. Will be stored in the
        machine dictionary
        :type  name: string
        :param operating_system: which operating system to create
        :type  operating_system: string (from operating_systems)
        :param machine_type: what size/type of machine to create
        :type  machine_type: string (from machine_types)
        :param user_name: the name of the user to create
        :type  user_name: string
        :param password: what to set the user's password to
        :type  password: string
        :param key_path: path to the file with an ssh private key for the user
        :type  key_path: local_absolute_path
        :param host: dns or ip to assign to the machine, if any
        :type  host: string
        :param port: what port to run sshd on
        :type  port: int
        :returns: the machine that was created (is running now)
        :rtype:   cowstrap.machine.Machine
        """
        assert password != None or key_path != None, \
        "Must set either password or key_path for SOME kind of authentication!"
        machine_details = {
            "name": name,
            "operating_system": operating_system,
            "machine_type": machine_type,
            "user_name": user_name,
            "host": host,
            "port": port,
        }
        if password != None:
            machine_details['password'] = password
        if key_path != None:
            machine_details['key_path'] = key_path
        machine = cowstrap.machine.Machine.from_dict(machine_details)
        self._create(machine)
        self._machine_dict[machine.name] = machine
        return machine

    def start(self, name):
        """
        :param name: a unique name or id for the machine.
        :type  name: string
        :returns: the machine that was started (is running now)
        :rtype:   cowstrap.machine.Machine
        """
        self._start(self._get_machine(name))

    def stop(self, name):
        """
        Halt (shutdown) a given machine

        :param name: a unique name or id for the machine.
        :type  name: string
        """
        self._stop(self._get_machine(name))

    def terminate(self, name):
        """
        Terminate (permanently delete) a given machine

        :param name: a unique name or id for the machine.
        :type  name: string
        """
        machine = self._get_machine(name)
        self._terminate(machine)
        del self._machine_dict[machine.name]

    def _get_machine(self, name):
        """
        :param name: a unique name or id for the machine.
        :type  name: string
        :raises: cowstrap.errors.UndefinedMachineError if there is no machine
        with this name
        :returns: the machine with this name
        :rtype:   cowstrap.machine.Machine
        """
        if name not in self._machine_dict:
            raise cowstrap.errors.UndefinedMachineError(\
                    "Name not contained in machine dict", name=name)
        return self._machine_dict[name]

    #TODO: add suspend and resume operations once VMWare is supported

    def _is_running(self, machine):
        """
        :param machine: the machine instance to interact with
        :type  machine: cowstrap.machine.Machine
        :returns: True iff the machine is running
        :rtype:   boolean
        """
        raise NotImplementedError()

    def _create(self, machine):
        """
        :param machine: the machine instance to interact with
        :type  machine: cowstrap.machine.Machine
        """
        raise NotImplementedError()

    def _start(self, machine):
        """
        :param machine: the machine instance to interact with
        :type  machine: cowstrap.machine.Machine
        :returns: the machine that was started (is running now)
        :rtype:   cowstrap.machine.Machine
        """
        raise NotImplementedError()

    def _stop(self, machine):
        """
        Halt (shutdown) a given machine

        :param machine: the machine instance to interact with
        :type  machine: cowstrap.machine.Machine
        """
        raise NotImplementedError()

    def _terminate(self, machine):
        """
        Terminate (permanently delete) a given machine

        :param machine: the machine instance to interact with
        :type  machine: cowstrap.machine.Machine
        """
        raise NotImplementedError()
