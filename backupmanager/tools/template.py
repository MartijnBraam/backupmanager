def info(config):
    """ Display backup status and list
    This command should display some basic information about the backup like size, location and other backup software
    specific stuff. It should also display a list of backups that are successfully run.
    """
    pass


def run(config):
    """ Run the backup configuration
    This should start the backup tool and run a backup, no cleaning of old backups yet. that is done in the cleanup()
    function
    """
    pass


def verify(config):
    """ Run a basic sanity test on the configuration.
    The include and exclude paths are already checked in the main
    script. You should also check if the backup software is installed here.
    """
    pass


def cleanup(config):
    """ Clean up old backups from the archive location
    """
    pass
