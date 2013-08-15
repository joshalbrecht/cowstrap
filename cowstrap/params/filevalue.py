
import os

import cowstrap.errors
import cowstrap.params.stringvalue

class FileValue(cowstrap.params.stringvalue.StringValue):
    """
    Represents boolean input value.
    """

    def __init__(self, name, must_exist=False, **kwargs):
        self.must_exist = must_exist
        validation_rules = kwargs.get('validation_rules', [])
        validation_rules.append(self._check_existance)
        kwargs['validation_rules'] = validation_rules
        cowstrap.params.stringvalue.StringValue.__init__(self, name, **kwargs)

    def _check_existance(self, data):
        """
        Validate that a file exists if desired
        """
        if self.must_exist:
            if not os.path.exists(data):
                raise cowstrap.errors.ValidationError("Does not exist {}"\
                    .format(data))

