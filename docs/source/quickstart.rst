Quickstart
==========

This is the quick start guide for deploying backupmanager on a computer.

Requirements and Installation
-----------------------------

Backup Manager requires at least Python 3.4 and pip3.
These dependencies are in the repositories for:

* Debian 8 and higher
* Archlinux

For debian run::

    $ apt-get install python3-pip
    $ pip3 install backupmanager
    $ backupctl init

This will install backupmanager and create a example ``/etc/backup.yml`` configured for borg

It is also important to install the backup tool itself. In this example Borg. The easiest way to install borg is using
the static linked binary::

    $ wget https://github.com/borgbackup/borg/releases/download/1.0.0rc1/borg-linux64
    $ chmod +x borg-linux64
    $ mv borg-linux64 /usr/local/bin/borg

Repeat the borg installation steps for the server that is used as backup destination. Borg requires the binary both on
the server and the client.

Configuration
-------------

In the example the host that needs backup is `zenbook` and the backup destination is `192.168.2.101`

First make sure you can ssh login from `zenbook` to `192.168.2.101` with publickey authentication::

    $ ssh-keygen
    $ ssh-copy-id backupuser@192.168.2.101

The backups will be stored in `/mnt/storage/backups/zenbook` on the backup destination in this example. The backup
destination directory needs to exist so create it first. Then on `zenbook` run::

    $ borg init ssh://backupuser@192.168.2.101/mnt/storage/backups/zenbook

If you run the borg init command locally on the backup destination server then the borg client on `zenbook` won't have
a trust relation with the remote borg repository and the backup will fail until you run one backup manually.

Now you need to enter the backup destination details in ``/etc/backup.yml``. Open the file and modify the values under
`where:` to the correct values for your backup server.

.. code-block:: yaml

    where:
        type: ssh
        host: 192.168.2.101
        user: backupuser
        path: /mnt/storage/backups/zenbook
        archive-template: 'Backup-%Y-%m-%d'

        # Compression options, use ~, fast or slow.
        # ~    : uncompressed backups
        # fast : lz4 compressed backups
        # slow : lzma,8 compressed backups
        compression: fast

The `archive-template` will be used to generate the backup name for each backup. The default is good for most cases.
It is possible to use a single repository for multiple clients and then you need to use different `archive-template`
values so two clients don't create the same archive. It is not advised to use a single repository for multiple clients
in most cases because you can't backup with two clients to the same repository at the same time. The first client will
hold an exclusive lock on the whole repository while backupping and the second client will fail.

The `compression` setting manages, you guessed it, the compression type. It is possible to run borg without compression
to save a little bit of cpu time but that will easily double the bandwidth and storage required for the backup. The
`fast` compression is enough if you have a fast link between the client and the server and no disk storage problems.
You can use `slow` compression if you backup over a very slow internet link but it will use a lot more memory and cpu
while backupping.

Enabling the backup
-------------------

The last thing that is needed is starting the backup somehow. You can manually start the backup with::

    $ backupctl run

You can also put that command in cron for a quick and dirty backup setup. If the linux distribution on your client
(`zenbook` in the example) has systemd as init system then `backupctl` can create a systemd service and timer for you::

    $ backupctl setup-systemd

This will create a daily backuptask managed with systemd. Now you can wait or start the backup with::

    $ systemctl start backup

Viewing backup status
---------------------

If one or more backups have run then you can view the backup status with::

    $ backupctl info

It will display a list of backups and some global statistics about the backups.