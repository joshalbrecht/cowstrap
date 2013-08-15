
import cowstrap.providers.local
import cowstrap.providers.aws
import cowstrap.actions.action

class Bootstrap(cowstrap.actions.action.Action):
    """
    Ensure that a machine is up and running all required software:
    - (some package manager)
    - sshd
    - puppet

    Produces a single 'machine' field by which later stages may interact with
    the bootstrapped machine.

    :ivar _allow_new: whether to allow the creation of new machines or not
    :type _allow_new: Boolean
    :ivar _possible_providers: mapping from provider name -> provider. Defines
    the providers that we can possibly interact with.
    :type _possible_providers: dict(string, cowstrap.providers.provider.Provider)

    these are set while configuring:

    :ivar _should_create_new_machine: whether we should make a new machine or
    use an existing one
    :type _should_create_new_machine: boolean
    :ivar _provider: which provider to use for this run
    :type _provider: cowstrap.providers.provider.Provider
    """

    def __init__(self, allow_new=True):
        cowstrap.actions.action.Action.__init__(self, set(["machine"]))
        self._allow_new = allow_new
        self._possible_providers = {
            'local': cowstrap.providers.local.LocalProvider(),
            'aws':   cowstrap.providers.aws.AwsProvider(),
            #TODO: would be nice to have a Vmware provider so that I could suspend/resume machines, or docker or vagrant providers
        }

        self._provider = None
        self._should_create_new_machine = None

    def register(self, parser):
        for provider in self._possible_providers.values():
            provider.register(parser)

        #parser.add_argument('-x', type=int, default=1)
        #parser.add_argument('y', type=float)
        pass

    def configure(self, config, arguments, previous_fields):

        #figure out the provider and let it handle the rest
        provider_name = arguments.provider or config.provider or None
        if provider_name == None:
            self._provider = self.prompt_user(
                "provider",
                default='local',
                options=self._possible_providers)
        else:
            self._provider = self._possible_providers[provider_name]
        self._provider.configure(config, arguments, previous_fields)

        #figure out if we're trying to make a new machine or use an existing one
        self._should_create_new_machine = self._prompt_for_should_create()

        #if we're trying to make a new machine, make sure enough details are set
        if self._should_create_new_machine:
            self._prompt_for_new_machine_details()
        #otherwise make sure they set enough information to identify the machine
        else:
            self._prompt_for_identifying_machine_details()

    def perform(self):
        #make new machine if necessary
        #ensure that the machine is in the appropriate state (running, bootstrapped)
        pass

    def _prompt_for_should_create(self, ):
        if self._allow_new:
            #did they specify any options about creating a new machine?
            if arguments.os or arguments.machine_type:
                should_create_new_machine = True
            else:
                #prompt the user
                should_create_new_machine = self.prompt_user(\
                    "should_create_new_machine", default=True)
        else:
            should_create_new_machine = False
        return should_create_new_machine

