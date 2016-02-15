import logging
import os
import subprocess


def failure(config, error):
    logging.fatal('Backup failure')
    logging.fatal(error)
    if 'errors' in config:
        if config['errors']['execute']:
            for command in config['errors']['execute']:
                try:
                    proc = subprocess.Popen(command, shell=True, universal_newlines=True, stdin=subprocess.PIPE)
                    proc.communicate(error)
                except subprocess.CalledProcessError as e:
                    logging.fatal('Error handler failed: {}'.format(command))
    exit(1)


def verify_config(config):
    what = config['what']
    if not what['include'] and not what['include-files']:
        logging.error('No include files specified in backup config')
        exit(1)
    if what['include']:
        for path in what['include']:
            if not os.path.isdir(path):
                logging.error('{} is not a valid directory'.format(path))
                exit(1)
    if what['include-files']:
        for file in what['include-files']:
            if not os.path.isfile(file):
                logging.error('{} does not exist'.format(file))
                exit(1)
    if what['exclude']:
        for path in what['exclude']:
            if not os.path.isdir(path):
                logging.error('{} is not a valid directory'.format(path))
                exit(1)
    if what['exclude-files']:
        for file in what['exclude-files']:
            if not os.path.isfile(file):
                logging.error('{} does not exist'.format(file))
                exit(1)
