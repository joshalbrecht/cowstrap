
import types

import cowstrap.params.value

class StringValue(cowstrap.params.value.Value):
    """
    Represents string input value.
    """

    def __init__(self, name, **kwargs):
        cowstrap.params.value.Value.__init__(self, name, types.StringType,
            **kwargs)

    def to_type(self, string_data):
        return string_data

    def to_string(self, typed_data):
        return typed_data
