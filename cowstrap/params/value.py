
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

    def __init__(self, name, value_type, default=None, description=None,
            long_help=None, validation_rules=None, choices=None,
            choice_descriptions=None):
        self.name = name
        self.value_type = value_type
        self._description = description
        self._long_help = long_help
        self._choices = choices
        self._choice_descriptions = choice_descriptions
        self._default = default
        self._validation_rules = validation_rules
        if self._validation_rules == None:
            self._validation_rules = []

        self._argument_name = "--" + self.name\
            .replace(".", "-").replace("_", "-")

        if self.has_default():
            self._argument_default = self.to_string(self.get_default())
        else:
            self._argument_default = None

        if choices != None:
            self._argument_choices = choices.keys()
        else:
            self._argument_choices = None

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

    def register(self, arg_parser):
        """
        :param arg_parser: where to add a command line argument for this value
        :type  arg_parser: argparse.ArgumentParser
        """
        arg_parser.add_argument(
            name=self._argument_name,
            action='store',
            default=self._argument_default,
            choices=self._argument_choices,
            help=self._description,
            dest=self.name
        )

    def prompt(self):
        """
        Continue asking the user for the value until they reply with valid
        input.
        :returns: the valid input typed by the user. Guaranteed that this will
        NOT cause an exception when passed to self.to_value
        :rtype:   string
        """
        message = None
        while True:
            user_input = self._prompt(message)
            try:
                converted_data = self.to_type(user_input)
                self.validate(converted_data)
                return user_input
            except cowstrap.errors.ValidationError, e:
                message = \
                    "Invalid input: {}\nPlease try again (ctrl + c to quit): " \
                    .format(str(e))

    def _prompt(self, message=None):
        """
        Ask the user for this value

        :param message: the message to print to the user, asking them for data
        :type  message: string
        :returns: the data from the user. Leading and trailing whitespace is
        trimmed off before returning.
        :rtype:   string
        """
        if message == None:
            example_value = "*****"
            summary_line = ""
            if self._description != None:
                summary_line = "\n  Summary: " + self._description
            help_line = ""
            if self._long_help != None:
                help_line = "\n  Help: " + self._long_help
            default_line = ""
            if self._argument_default != None:
                example_value = self._argument_default
                default_line = "\n  Default (press enter to use this): " + \
                    self._argument_default
            choice_line = ""
            if self._choices:
                choice_num = 1
                choice_strs = []
                for choice in self._choices.keys():
                    if self._choice_descriptions == None:
                        descr = ""
                    else:
                        if choice in self._choice_descriptions:
                            descr = ": " + self._choice_descriptions[choice]
                        else:
                            descr = ": (no description)"
                    choice_str = "{}. {}{}".format(choice_num, choice, descr)
                    if choice_num != None:
                        choice_str = "         " + choice_str
                    choice_strs.append(choice_str)
                    choice_num += 1
                choice_line = "\n  Choices: " + choice_strs.pop(0) + \
                    "\n".join(choice_strs)
            message = \
"""A value is required for {0}.
  Type: {1}{2}{3}{4}{5}

  If you would like to avoid this message in the future, specify the option on the command line:
    {6}="{7}"
  or specify it in the config file like this:
    {8} = "{9}"
Please provide a value: """.format(self.name, self.value_type, summary_line,
                help_line, default_line, choice_line, self._argument_name,
                example_value, self.name, example_value)
        self._output(message)
        user_data = raw_input()
        return user_data.trim()

    # pylint: disable=R0201
    def _output(self, message):
        """
        Just here for testing.
        """
        print message
