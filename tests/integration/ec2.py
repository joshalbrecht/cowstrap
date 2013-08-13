
import cowstrap.config
import cowstrap.commands.sync

class FakeArgs(object):
    pass

def test_sync():
    """
    Test that the fully configured Sync command will create a running instance
    in EC2
    """

    config = cowstrap.config.Config()
    args = FakeArgs()
    args.provider = 'aws'
    command = cowstrap.commands.sync.Sync()
    command.run(args, config)

if __name__ == '__main__':
    test_sync()
