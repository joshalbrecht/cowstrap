
import sync
import terminate

#TODO: add a suspend command

def all_commands():
    """
    :returns: list of instances of each Command provided by cowstrap
    :rtype:   list(cowstrap.Command)
    """
    return [sync.Sync(), terminate.Terminate()]
