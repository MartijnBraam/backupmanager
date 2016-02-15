import argparse
import yaml
import os
from shutil import copyfile
import logging
import subprocess
import backupmanager.tools.borg as borg
import backupmanager.common as common


def main():
    parser = argparse.ArgumentParser(description="Backup manager")
    parser.add_argument('--config', '-c', help="Config file location", default="/etc/backup.yml")
    parser.add_argument('--quiet', '-q', help="Raise loglevel to warning", action="store_true")
    parser.add_argument('--debug', '-d', help="Set loglevel to debug", action="store_true", default=False)
    parser.add_argument('command', choices=["init", "run", "info", "verify"])

    args = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(level=logging.INFO)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug logging enabled")

    if not os.path.isfile(args.config):
        logging.error("Config file does not exist at {}".format(args.config))
        logging.warning("You can create a config file scaffolding with 'backupmanager init'")
        exit(1)

    with open(args.config) as config_file:
        config = yaml.load(config_file)
    tool = config['tool']

    if tool == "borg":
        tool = borg
    else:
        logging.error("The tool '{}' is not supported".format(tool))

    if args.command == "info":
        tool.info(config)

    elif args.command == "init":
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        if not os.path.isfile('/etc/backup.yml'):
            logging.info('Creating /etc/backup.yml from template')
            copyfile(os.path.join(dir_path, 'backup.yml.dist'), '/etc/backup.yml')
        else:
            logging.warning('/etc/backup.yml exists already, skipping')

    elif args.command == "run":
        common.verify_config(config)
        if config['hooks']['pre-backup']:
            logging.info('Running pre-backup scripts')
            for hook in config['hooks']['pre-backup']:
                logging.info('Running {}'.format(hook))
                try:
                    subprocess.check_output(hook, shell=True)
                except subprocess.CalledProcessError as e:
                    common.failure(config, e.output)
        tool.run(config)
        if config['hooks']['post-backup']:
            logging.info('Running post-backup scripts')
            for hook in config['hooks']['post-backup']:
                logging.info('Running {}'.format(hook))
                try:
                    subprocess.check_output(hook, shell=True)
                except subprocess.CalledProcessError as e:
                    common.failure(config, e.output)

    elif args.command == "verify":
        common.verify_config(config)
        tool.verify(config)


if __name__ == "__main__":
    main()
