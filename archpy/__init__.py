from os import chdir, path
from .lib.constants import *
from .lib.text import *
from .lib.file import *
from .lib.command import *
from .lib.sysinfo import *
from .lib.partitions import *
from .lib.packages import *
from .lib.config import *
from .lib.booatloaders import *
from .lib.installation import *

__version__ = '1.0.0'

# Module arguments.
arguments = {}
positionals = []
for arg in sys.argv[1:]:
    if '--' == arg[:2]:
        if '=' in arg:
            key, val = [x.strip() for x in arg[2:].split('=', 1)]
        else:
            key, val = arg[2:], True
        arguments[key] = val
    else:
        positionals.append(arg)


def run():
    chdir(path.abspath(path.dirname(__file__)))
    try:
        if len(sys.argv) < 2 or len(sys.argv) >= 4:
            Message('red_alert').print("It's only possible to pass one argument.")
        elif len(sys.argv) == 2:
            if sys.argv[1] == 'install':
                Setup(Config().new()).install()
            elif sys.argv[1] == 'sysinfo':
                print(SystemInfo().sysinfo)
            elif sys.argv[1] == 'help':
                print(
                    """
                    ## archpy install [path|url]
                        - The install command can start a new installation (if no path or url is passed in) or
                        load a installation parameters from a local or remote json file.
                        - Absolute path or url is necessary.

                    ## archpy generate config
                        - Creates a new installation parameters json file on the desired directory.
                        - In the end, user will be prompted to insert the full directory path. A json file called
                        archpy.json will be created on that path.
                    """
                )
            else:
                Message('red_alert').print('Command not valid!')
        elif len(sys.argv) == 3:
            if sys.argv[1] == 'install':
                Setup(Config().load(sys.argv[2])).install()
            elif sys.argv[1] == 'generate':
                if sys.argv[2] == 'config':
                    Config().generate()
            else:
                Message('red_alert').print('Command not valid!')
        else:
            Message('red_alert').print('Command not valid!')
    except IndexError:
        Message('red_alert').print('No command found!')
