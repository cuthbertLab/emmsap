import os
import sys
from sys import version_info as _pyver
if _pyver[0] <= 2 or (_pyver[0] == 3 and _pyver[1] <= 3):
    raise ImportError("Emmsap requires Python 3.4 or higher. Exiting.")

if __name__ == '__main__' and __package__ in (None, ''):
    packageDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(packageDir)
    __package__ = 'emmsap'
    import emmsap

from . import updateDB


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Commands are: updateDB...well that's it...")
    else:
        command = sys.argv[1]
        if command.lower() == 'updatedb':
            updateDB.updateDatabase()
