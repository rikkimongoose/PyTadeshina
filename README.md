PyTadeshina
=========

A cross-platform util for estimating the file size and delete the useless ones.

Requirements:
* Python 2.7+
* tkInter

Usage
====

    python tadeshina.py %directory_name% [-h] [-s]

    -h, --help - show help

    -s, --silent - delete files without prompt

    [%directory_name%] - start from this directory

License
====

This software is released under the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).

External code
==

* [send2trash 1.2.0](https://pypi.python.org/pypi/Send2Trash) by [Hardcoded Software](http://www.hardcoded.net) was used for "Delete to Recycle" command.
