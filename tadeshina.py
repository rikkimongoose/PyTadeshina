#!/usr/bin/env python
import os
import sys
import getopt
import ctypes
from ext.dirwindow import DirWindow

SETTINGS = {}

# Main code
def main():
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "doh", ["directory=", "output", "help"])
    except getopt.GetoptError as err:
        sys.stderr.write("%s\n" % str(err))
        sys.exit(2)

    OPTS = dict(OPTS)

    if '--help' in OPTS:
        show_help()
        sys.exit(0)

    if '--directory' in OPTS:
        SETTINGS["path_to_load"] = OPTS['--directory']
    elif len(ARGS) > 0:
        SETTINGS["path_to_load"] = ARGS[0]
    else:
        SETTINGS["path_to_load"] = "."
    if not os.path.exists(SETTINGS["path_to_load"]):
        sys.stderr.write('Directory "%s" is not existing.' % SETTINGS["path_to_load"])
        sys.exit(2)

    SETTINGS["debug_output"] = "--output" in OPTS

    mainWindow = DirWindow(SETTINGS["path_to_load"])
    mainWindow.mainloop()

def show_help():
    """ Show the help about the possible command line options
    """
    print """Tadeshina 0.1 alpha

    Get size of files in a directory. Usage

    python tadeshina.py %directory_name% %params%

    -h, --help - show help

    --o, --output - show output

    [%directory_name%] - show sizes in a directory
    """

if __name__ == "__main__":
    main()