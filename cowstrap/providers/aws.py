
import cowstrap.providers.provider

class AwsProvider(cowstrap.providers.provider.Provider):
    """
    A simple interface to the EC2 service

    :ivar _aws_access_key: The 'Access Key' string from AWS.
    :type _aws_access_key: string
    :ivar _aws_secret_key: The 'Secret Key' string from AWS.
    :type _aws_secret_key: string
    """

    def __init__(self, aws_access_key, aws_secret_key):
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        cowstrap.providers.provider.Provider.__init__(self,
        operating_systems=['ubuntu_12.04', 'windows_10'],
        machine_types=['m1.micro'])

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
