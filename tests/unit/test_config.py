
import random
import string
import os
import tempfile
from nose.tools import assert_raises, assert_equals

import cowstrap.errors
import cowstrap.config

_multiprocess_can_split_ = True

NAME = "helloness"
VALUE = "some value"

def test_get_data():
    with EphemeralConfig() as config:
        assert_raises(cowstrap.errors.BadValueError, config.get_data,
                      "something")
        config.set_data(NAME, VALUE)
        assert_equals(config.get_data(NAME), VALUE)

class EphemeralConfig(cowstrap.config.Config):
    """Cleans up after the file"""

    def __init__(self, ):
        chars = string.ascii_lowercase + string.digits
        size = 32
        random_string = ''.join(random.choice(chars) for x in range(size))
        temp_file = os.path.join(tempfile.gettempdir(), random_string)
        cowstrap.config.Config.__init__(self, temp_file)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, value, traceback):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

