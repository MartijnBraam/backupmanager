Duplicity / Déjà Dup
====================

Duplicity is a simple tar+rsync backup utility. Déjà Dup is a graphical frontend for Duplicity.


Destinations
------------

Duplicity supports a lot of backends. See the documentation below for the one you want to use.

SSH
^^^

This is a backup uploaded with sftp (ssh file transfer protocol, not ftps)

.. code-block:: yaml

    where:
        type: ssh
        host: 192.168.2.101
        user: backup
        path: /mnt/storage/backups/zenbook

        # Compression options, use ~, fast or slow.
        # ~    : uncompressed backups
        # fast : zlib compressed backups
        # slow : bzip2,8 compressed backups
        compression: fast

Azure
^^^^^

The Azure backend requires the Microsoft Azure Storage SDK for Python
to be installed on the system.

.. code-block:: yaml

    where:
        type: azure
        account: your azure account name
        key: your azure account key
        container: the container hostname

        # Compression options, use ~, fast or slow.
        # ~    : uncompressed backups
        # fast : zlib compressed backups
        # slow : bzip2,8 compressed backups
        compression: fast

FTP / FTPS
^^^^^^^^^^

Backup to a plain old ftp or ftps server.

.. code-block:: yaml

    where:
        type: ftp # or ftps
        host: your.ftp.server.or.ip
        user: backup
        password: secret
        path: /mnt/storage/backups/zenbook

        # Compression options, use ~, fast or slow.
        # ~    : uncompressed backups
        # fast : zlib compressed backups
        # slow : bzip2,8 compressed backups
        compression: fast