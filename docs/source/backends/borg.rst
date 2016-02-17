Borg
====

Borg_ is a fork from the backup tool attic_. It is a deduplicating compressing backup program.

.. _Borg: https://borgbackup.readthedocs.org/en/stable/
.. _attic: https://attic-backup.org/

Destinations
------------

Borg does its backups over SSH and requires the borg binary on the server.

A basic destination config:

.. code-block:: yaml

    where:
        type: ssh
        host: 192.168.2.101
        user: backup
        path: /mnt/storage/backups/zenbook
        archive-template: 'Backup-%Y-%m-%d'

        # Compression options, use ~, fast or slow.
        # ~    : uncompressed backups
        # fast : lz4 compressed backups
        # slow : lzma,8 compressed backups
        compression: fast

The path on the remote server should be an initialized borg repository. The best ways is to create it from the local host
to the remote host with ``borg init ssh://user@host/path``. If you create the repository on the remote server then
the local borg won't have a trust relation with the remote borg repository and the backup will fail.

If you have created the borg repository on the remote host then you can run borg manually first to create the trust
relation.