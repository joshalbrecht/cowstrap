
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

