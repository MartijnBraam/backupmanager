#!/usr/bin/env python3

from setuptools import setup

setup(
        name='backupmanager',
        version='0.2.4',
        packages=['backupmanager', 'backupmanager.tools'],
        url='https://github.com/MartijnBraam/backupmanager',
        license='MIT',
        author='Martijn Braam',
        author_email='martijn@brixit.nl',
        description='A wrapper to unify configuration/running backup tools',
        install_requires=[
            'humanize',
            'plumbum',
            'PyYAML',
            'tabulate'
        ],
        entry_points={
            'console_scripts': [
                'backupmanager = backupmanager.__main__:main'
            ]
        },
        keywords=["backup", "linux", "manager"],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Development Status :: 4 - Beta",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: MIT License"
        ],
)
