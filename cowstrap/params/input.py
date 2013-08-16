
import cowstrap
import cowstrap.errors

class Input(object):
    """
    Represents all user input (in any form) for this run of the program.

    Use "has_data" and "get_data" to access the values. See below for usage.

    :ivar _values: the set of all values that have been registered (mapped by
    name)
    :type _values: dict(string, cowstrap.params.value.Value)
    :ivar _args: the parsed arguments
    :type _args: argparse.Namespace
    :ivar _config: the configuration that was loaded
    :type _config: cowstrap.config.Config
    :ivar _is_interactive: whether to ever prompt the user
    :type _is_interactive: boolean
    :ivar _user_input: the data input by the user when they were prompted
    :type _user_input: dict(string, string)
    """

    def __init__(self, values, args, config, is_interactive=True):
        self._values = values
        self._args = args
        self._config = config
        self._is_interactive = is_interactive
        self._user_input = {}

    # pylint: disable=R0913
    def has_data(self, name, allow_defaults=True, allow_args=True,
        allow_config=True, allow_user=True, require_valid=True):
        """
        Check if there is data defined. Each of the locations of data can be
        toggled as to whether they count as defining the data or not.

        :param name: the value to check
        :type  name: string
        :param allow_defaults: whether default values count as data
        :type  allow_defaults: boolean
        :param allow_args: whether values from the command linecount as data
        :type  allow_args: boolean
        :param allow_config: whether default values from the config as data
        :type  allow_config: boolean
        :param allow_user: whether values from the user count as data
        :type  allow_user: boolean
        :param require_valid: whether values must be valid to count
        :type  require_valid: boolean
        :raises: cowstrap.errors.BadValueError if you pass an undefined name
        :returns: whether there is data defined (in the sense specified)
        :rtype:   boolean
        """
        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)
        if not self._is_interactive:
            allow_user = False
        if allow_defaults and self._has_default(name):
            return True
        if allow_args and self._has_arg(name, require_valid):
            return True
        if allow_config and self._has_config(name, require_valid):
            return True
        if allow_user and self._has_user(name):
            return True
        return False

    def get_data(self, name, required=False, persist=False):
        """
        Return the most specific data that was set. Priority, from highest to
        lowest is as follows:

        - user input
        - arguments
        - configuration
        - defaults

        If there is NO value, will prompt the user for data and cache their
        response if the value is marked as required, or the required flag was
        passed in

        If there is a value, but it fails validation, will print a warning and
        prompt the user.

        The user will never be prompted if the run is marked as not interactive.
        In that case, the run will fail instead.

        If the user successfully sets the variable and persist is True, it will
        be saved to

        :raises: cowstrap.errors.BadValueError if you pass an undefined name, or
        if this is a non-interactive run and there was no value for something
        that is required
        :returns: the data for this value
        :rtype:   <self._values[name].value_type>
        """

        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)

        result = None

        if self._has_user(name):
            result = self._get_user(name)

        if self._has_arg(name, require_valid=True):
            result = self._get_arg(name)
        elif self._has_arg(name, require_valid=False):
            value_from_args = getattr(self._args, name)
            cowstrap.log.warn(
                "Arguments contained an invalid value ({}) for {}".format(
                    value_from_args, name))

        if self._has_config(name, require_valid=True):
            result = self._get_config(name)
        elif self._has_config(name, require_valid=False):
            value_from_conf = self._config.get_data(name)
            cowstrap.log.warn(
                "Config contained an invalid value ({}) for {}".format(
                    value_from_conf, name))

        if self._has_default(name):
            result = self._get_default(name)

        #if we got to this point, there was no data defined
        if result == None:
            #bail if there is no user to query
            if not self._is_interactive:
                if required:
                    raise cowstrap.errors.BadValueError("Not defined: " + name)
                else:
                    return None

            #ask the user what they want to do about the missing value
            value = self._values[name]
            user_input = value.prompt()
            result = value.to_type(user_input)
            self._user_input[name] = user_input

        #persist the value if appropriate
        if result != None and persist:
            self._config.set_data(value.to_string(result))
            self._config.save()

        return result

    def _has_default(self, name):
        """
        Note that default values are always valid.

        :param name: the value name
        :type  name: string
        :returns: True iff there is a default value set
        :rtype:   boolean
        """
        return self._values[name].has_default()

    def _has_user(self, name):
        """
        Note that user values are always valid.

        :param name: the value name
        :type  name: string
        :returns: True iff there is a value set by the user
        :rtype:   boolean
        """
        return name in self._user_input

    def _has_config(self, name, require_valid=True):
        """
        :param name: the value name
        :type  name: string
        :param require_valid: whether only valid entries count or not
        :type  require_valid: boolean
        :returns: True iff there is a value set in the config
        :rtype:   boolean
        """
        if self._config.has_data(name):
            if require_valid:
                try:
                    self._get_config(name)
                    return True
                except cowstrap.errors.ValidationError:
                    return False
            else:
                return True
        return False

    def _has_arg(self, name, require_valid=True):
        """
        :param name: the value name
        :type  name: string
        :param require_valid: whether only valid entries count or not
        :type  require_valid: boolean
        :returns: True iff there is a value set in the arguments
        :rtype:   boolean
        """
        data = getattr(self._args, name)
        if data != None:
            if require_valid:
                try:
                    self._get_arg(name)
                    return True
                except cowstrap.errors.ValidationError:
                    return False
            else:
                return True
        return False

    def _get_user(self, name):
        """
        Note that user values are always valid.

        :param name: the value name
        :type  name: string
        :raises: cowstrap.errors.BadValueError if you pass an undefined name
        :returns: the data for this value
        :rtype:   <self._values[name].value_type>
        """
        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)
        return self._values[name].to_type(self._user_input[name])

    def _get_default(self, name):
        """
        Note that default values are always valid.

        :param name: the value name
        :type  name: string
        :raises: cowstrap.errors.BadValueError if you pass an undefined name
        :returns: the data for this value
        :rtype:   <self._values[name].value_type>
        """
        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)
        return self._values[name].get_default()

    def _get_config(self, name):
        """
        :param name: the value name
        :type  name: string
        :raises: cowstrap.errors.BadValueError if you pass an undefined name
        :raises: cowstrap.errors.ValidationError if the data is invalid
        :returns: the data for this value
        :rtype:   <self._values[name].value_type>
        """
        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)
        string_data = self._config.get_data(name)
        converted_value = self._values[name].to_type(string_data)
        self._values[name].validate(converted_value)
        return converted_value

    def _get_arg(self, name):
        """
        :param name: the value name
        :type  name: string
        :raises: cowstrap.errors.BadValueError if you pass an undefined name
        :raises: cowstrap.errors.ValidationError if the data is invalid
        :returns: the data for this value
        :rtype:   <self._values[name].value_type>
        """
        if name not in self._values:
            raise cowstrap.errors.BadValueError("Not defined: " + name)
        string_data = getattr(self._args, name)
        converted_value = self._values[name].to_type(string_data)
        self._values[name].validate(converted_value)
        return converted_value
