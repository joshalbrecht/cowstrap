
import os

import cowstrap.providers.provider

class LocalProvider(cowstrap.providers.provider.Provider):
    """
    A 'Provider' that just runs commands on the local system
    """

    def __init__(self):
        cowstrap.providers.provider.Provider.__init__(self,
            operating_systems=[os.name],
            machine_types=['local'])

    def _is_running(self, machine):
        pass

    def _create(self, machine):
        pass

    def _start(self, machine):
        pass

    def _stop(self, machine):
        pass

    def _terminate(self, machine):
        pass
