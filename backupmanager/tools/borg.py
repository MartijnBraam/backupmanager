import logging
from plumbum.commands.processes import ProcessExecutionError
import datetime
import humanize
from tabulate import tabulate
import backupmanager.common as common


def info(config):
    from plumbum.cmd import borg
    print('Backup tool: borg')
    print('Repository:  {}'.format(borg_repository(config)))
    repository = borg_repository(config)
    logging.debug('Borg repository: {}'.format(repository))

    logging.debug('Executing borg list...')
    borg_list = borg['list', repository]
    list = borg_list()
    logging.debug('Received list')
    if len(list.strip()) == 0:
        print("No backups have been created yet.")
        return
    table = []
    for archive in list.split("\n"):
        if archive.strip() != "":
            name, date = archive.split(maxsplit=1)
            date = parse_borg_date(date)
            table.append([name, humanize.naturaltime(date)])

    last_archive = table[-1][0]
    last_archive = get_borg_archive_info(config, last_archive)

    print(last_archive)

    print()
    print("List of stored backups:")
    print(tabulate(reversed(table), headers=['Name', 'Date']))


def run(config):
    from plumbum.cmd import borg
    logging.info('Starting borg backup to {}'.format(borg_repository(config)))
    archive_name = datetime.datetime.now().__format__(config['where']['archive-template'])
    archive = '{}::{}'.format(borg_repository(config), archive_name)
    with open('/tmp/borg-exclude-file', 'w') as exclude_file:
        if config['what']['exclude']:
            exclude_file.writelines(config['what']['exclude'])
        exclude_file.write("\n")
        if config['what']['exclude-files']:
            for f in config['what']['exclude-files']:
                with open(f) as input_file:
                    exclude_file.write(input_file.read())
                    exclude_file.write("\n")
    command = borg['create', archive, '--exclude-from', '/tmp/borg-exclude-file', '--exclude-caches']

    arguments = []
    if config['where']['compression'] == 'fast':
        arguments.append('-C')
        arguments.append('lz4')
    if config['where']['compression'] == 'slow':
        arguments.append('-C')
        arguments.append('lzma,8')

    if config['what']['include']:
        arguments.extend(config['what']['include'])
    if config['what']['include-files']:
        for f in config['what']['include-files']:
            with open(f) as input_file:
                arguments.extend(input_file.readlines())
    try:
        command(tuple(arguments))
    except ProcessExecutionError as e:
        logging.error('Backup failed, borg returned error')
        result = e.stdout + e.stderr
        common.failure(config, result)

    logging.info('Borg backup complete')
    cleanup(config)


def verify(config):
    pass


def cleanup(config):
    from plumbum.cmd import borg
    logging.info('Starting borg pruning')
    prune = borg['prune', borg_repository(config)]

    command = [
        '--keep-daily',
        config['retention']['daily-backups'],
        '--keep-weekly',
        config['retention']['weekly-backups'],
        '--keep-monthly',
        config['retention']['monthly-backups']
    ]

    if config['retention']['only-prefix']:
        command.append(['--prefix', config['retention']['only-prefix']])
    prune(tuple(command))
    logging.info('Borg pruning complete')


def borg_repository(config):
    dest = config['where']
    return "{type}://{user}@{host}{path}".format(**dest)


def parse_borg_date(datestring):
    _, datestring = datestring.split(maxsplit=1)
    return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')


def get_borg_archive_info(config, archive):
    repo = borg_repository(config)
    info_command = borg['info', '{}::{}'.format(repo, archive)]
    raw = info_command()
    part = raw.split("\n\n", 1)
    result = part[1]
    result = result.replace("This archive", "Last archive")
    return result
