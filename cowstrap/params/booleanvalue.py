
import types

import cowstrap.params.value

class BooleanValue(cowstrap.params.value.Value):
    """
    Represents boolean input value.
    """

    def __init__(self, name, **kwargs):
        cowstrap.params.value.Value.__init__(self, name, types.BooleanType,
            **kwargs)

    def to_type(self, string_data):
        if string_data.lower() in ('y', 'yes', 't', 'true'):
            return True
        elif string_data.lower() in ('n', 'no', 'f', 'false'):
            return False
        else:
            raise cowstrap.errors.ValidationError("Please enter true or false")

    def to_string(self, typed_data):
        return str(typed_data).lower()
