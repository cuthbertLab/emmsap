import getpass
import os
from typing import TypedDict

from .exceptions import EMMSAPException


class PasswordDict(TypedDict):
    database: str
    host: str
    user: str
    password: str


def readEMMSAPPasswordFile(userdir=''):
    '''
    Read a .emmsap_password file in the form

    database=emmsap
    host=localhost
    user=username
    password=PASSWORD
    '''
    if not userdir:
        username = getpass.getuser()
        # likely to be /Library/Webserver on Mac
        userdir = os.path.expanduser('~' + username)

    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    # logging.debug(username)

    password_file = userdir + os.path.sep + '.emmsap_password'

    if not os.path.exists(password_file):
        raise EMMSAPException(
            'Cannot read password file! put it in a file in the home directory '
            + 'called .emmsap_password. Home directory is: '
            + userdir
        )

    with open(password_file) as f:
        pwContents = f.readlines()

    pw_dict: PasswordDict = {
        'password': '',
        'host': 'localhost',
        'username': 'emmsap_user',
        'database': 'emmsap',
    }

    for i, p in enumerate(pwContents):
        p = p.strip()
        if '=' in p:
            key, value = p.split('=', 1)
            if key in ('password', 'host', 'username', 'database'):
                # noinspection PyTypedDict
                pw_dict[key] = value
        else:
            pw_dict['password'] = p

    return pw_dict
