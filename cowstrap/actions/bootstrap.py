
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
    """

    def __init__(self, allow_new=True):
        cowstrap.actions.action.Action.__init__(self, set(["machine"]))
        self._allow_new = allow_new
        self._possible_providers = [
            cowstrap.providers.local.LocalProvider(),
            cowstrap.providers.ec2.Ec2Provider(),
            #TODO: would be nice to have a Vmware provider so that I could suspend/resume machines, or docker or vagrant providers
        ]

    def register(self, parser):
        #parser.add_argument('-x', type=int, default=1)
        #parser.add_argument('y', type=float)
        pass

    def configure(self, config, arguments, previous_fields):

        #figure out if we're trying to make a new machine or use an existing one
        if self._allow_new:
            #did they specify any options about an existing machine?
            if arguments.host or arguments.machine_name:
                should_create_new_machine = False
            #did they specify any options about creating a new machine?
            elif arguments.provider or arguments.os or arguments.machine_type:
                should_create_new_machine = True
            else:
                #prompt the user
                should_create_new_machine = self.prompt_user(\
                    "should_create_new_machine", default=True)
        else:
            should_create_new_machine = False

        if should_create_new_machine:
            #figure out the provider and let it handle the rest
            provider = arguments.provider or config.provider or None
            if provider == None:
                provider = self.prompt_user(
                    "provider",
                    default=cowstrap.providers.local.LocalProvider(),
                    options=self._possible_providers)
            provider.configure(config, arguments, previous_fields)

        else:
            #is this machine in our machine dictionary?
            #if not, can we figure out the os and provider with the info given?
            #if not, prompt the user about that stuff
            #now let the provider read in any additional configuration
            pass

        #at this point, make sure we've set enough info that we can proceed
        #perhaps have a persistent dictionary of previous machines and give options to use those or a new one?
        #new/existing
        #provider
        #os
        #host/port (if existing)
        #user/(key or pass)
        pass

    def perform(self):
        #make new machine if necessary
        #ensure that the machine is in the appropriate state (running, bootstrapped)
        pass
