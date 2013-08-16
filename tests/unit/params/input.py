
from nose.tools import assert_raises

import cowstrap.errors
import cowstrap.config
import cowstrap.params.stringvalue
import cowstrap.params.input

NAME = "helloness"

def test_has_data_with_invalid_value_name():
    inp = make_input()
    assert_raises(inp.has_data(NAME+"invalid"), cowstrap.errors.BadValueError)

def test_has_default_data():
    pass

def test_has_valid_user_data():
    pass

def test_has_invalid_user_data():
    pass

def make_values(**kwargs):
    return {NAME: cowstrap.params.stringvalue.StringValue(NAME, **kwargs)}

def make_args(**kwargs):
    pass

def make_config(**kwargs):
    #TODO: mock the load and save methods here
    return cowstrap.config.Config("/not/a/valid/path")

def make_input(value_kwargs=None, arg_kwargs=None, config_kwargs=None):
    if value_kwargs == None:
        value_kwargs = {}
    if arg_kwargs == None:
        arg_kwargs = {}
    if config_kwargs == None:
        config_kwargs = {}
    return cowstrap.params.input.Input(
        make_values(**value_kwargs),
        make_args(**arg_kwargs),
        make_config(**config_kwargs)
    )

