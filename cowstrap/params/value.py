
import cowstrap.errors

class Value(object):
    """
    Represents a typed, configurable, serializable, validatable input value.

    - Typed: This class is abstract. Must override with implementations for each
    specific type of data that can be configured

    - Configurable: This data is meant to come from users, and there are options
    about how they can be prompted and when

    - Serializable: All values must be able to exist in config files, and on the
    command line, in a simple string form that can be converted to and from
    the desired type

    - Validatable: Rules may be defined about what consitutes acceptable input
    for any particular type or instance

    :ivar name: the variable name
    :type name: string
    :ivar value_type: what type of data will be returned by this Value
    :type value_type: type
    :ivar _default: the default value for this value.
    Note: cannot set a default to None! Use required=False instead
    :type _default: <self.value_type>
    :ivar _validation_rules: the rules to apply when checking input
    :type _validation_rules: func(<self.value_type>) raises
    cowstrap.errors.ValidationError
    """

    def __init__(self, name, value_type, default=None, required=False, description="", validation_rules=None):
        self.name = name
        self.value_type = value_type
        self._default = default
        self._validation_rules = validation_rules
        if self._validation_rules == None:
            self._validation_rules = []

    def register(self, arg_parser):
        """
        :param arg_parser: where to add a command line argument for this value
        :type  arg_parser: argparse.ArgumentParser
        """
        raise NotImplementedError()

    def prompt(self):
        """
        Ask the user for this value

        :returns: the data from the user. Leading and trailing whitespace is
        trimmed off before returning.
        :rtype:   string
        """
        raise NotImplementedError()

    def to_type(self, string_data):
        """
        Convert from a string to value_type

        :param string_data: the string data to convert
        :type  string_data: string
        :returns: the converted value
        :rtype:   <self.value_type>
        """
        raise NotImplementedError()

    def to_string(self, typed_data):
        """
        Convert from value_type to a string

        :param typed_data: the data to convert
        :type  typed_data: <self.value_type>
        :returns: the converted value
        :rtype:   string
        """
        raise NotImplementedError()

    def validate(self, data):
        """
        Apply each of the validation rules

        :param data: the data to validate
        :type  data: <self.value_type>
        :raises: cowstrap.errors.ValidationError if any of the validation logic
        fails
        """
        for rule in self._validation_rules:
            rule(data)

    def get_default(self):
        """
        :returns: the default value
        :rtype:   <self.value_type>
        """
        return self._default

    def has_default(self):
        """
        :returns: True iff this has a non-None default value
        :rtype:   boolean
        """
        return self._default != None

