#!/usr/bin/env python3

from distutils.core import setup

setup(
        name='backupmanager',
        version='0.1.0',
        packages=['backupmanager', 'backupmanager.tools'],
        url='https://github.com/MartijnBraam/backupmanager',
        license='MIT',
        author='Martijn Braam',
        author_email='martijn@brixit.nl',
        description='A wrapper to unify configuration/running backup tools',
        entry_points={
            'console_scripts': [
                'backupmanager = backupmanager.__main__:main'
            ]
        }
)
