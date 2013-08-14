
class PleaseImplementForMe(NotImplementedError):
    """
    The usage of this error signals that this code should be implemented.

    Please create an implementation and send me a pull request :)
    """

class CowstrapError(Exception):
    """
    Base class for all errors from Cowstrap
    """
    def __init__(self, description, **kwargs):
        Exception.__init__(self)
        self.description = description
        self.kwargs = kwargs

    def __str__(self, ):
        return "{}: {}. Details: {}"\
        .format(self.__class__, self.description, self.kwargs)

class UndefinedMachineError(CowstrapError):
    """
    Raised if a machine is not in the machine dictionary, or is misconfigured
    """
    def __init__(self, description="Machine was not defined", **kwargs):
        CowstrapError.__init__(self, description, **kwargs)

class BadInputError(CowstrapError):
    """
    Raised if the user inputs something of the wrong type or otherwise wrong
    """
    def __init__(self, description="Bad input", **kwargs):
        CowstrapError.__init__(self, description, **kwargs)
