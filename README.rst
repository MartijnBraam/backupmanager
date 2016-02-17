Backupmanager
=============

See pythonhosted_ for the documentation

.. _pythonhosted: http://pythonhosted.org/backupmanager/

This is a tool to control various backup programs (at least that's the idea, only borg is supported at the moment)
Backupmanager uses the config file `/etc/backup.yml` (by default) to read what to backup and where to and it will pass
the correct arguments to the selected backup tool.

Installation
------------

Install backupmanager with `pip3 install backupmanager`. Now you can use `backupmanager init` to create a template config
file in `/etc/backup.yml`

ToDo
----

* Write full support for duplicity
* Add support for encryption options
* Backup restore
* Backup integrity verify