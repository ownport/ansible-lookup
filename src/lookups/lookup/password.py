from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import string
import random

from string import ascii_letters, digits

from lookups.lookup import LookupError
from lookups.lookup import LookupBase
from lookups.parsing.splitter import parse_kv
from lookups.utils.encrypt import do_encrypt
from lookups.utils.path import makedirs_safe

DEFAULT_LENGTH = 20
DEFAULT_PASSWORD_CHARS = ascii_letters + digits + ".,:-_"
VALID_PARAMS = frozenset(('length', 'encrypt', 'chars'))


def _parse_parameters(term):
    # Hacky parsing of params
    # See https://github.com/ansible/ansible-modules-core/issues/1968#issuecomment-136842156
    # and the first_found lookup For how we want to fix this later
    first_split = term.split(' ', 1)
    if len(first_split) <= 1:
        # Only a single argument given, therefore it's a path
        relpath = term
        params = dict()
    else:
        relpath = first_split[0]
        params = parse_kv(first_split[1])
        if '_raw_params' in params:
            # Spaces in the path?
            relpath = ' '.join((relpath, params['_raw_params']))
            del params['_raw_params']

            # Check that we parsed the params correctly
            if not term.startswith(relpath):
                # Likely, the user had a non parameter following a parameter.
                # Reject this as a user typo
                raise LookupError('Unrecognized value after key=value parameters given to password lookup')
        # No _raw_params means we already found the complete path when
        # we split it initially

    # Check for invalid parameters.  Probably a user typo
    invalid_params = frozenset(params.keys()).difference(VALID_PARAMS)
    if invalid_params:
        raise LookupError('Unrecognized parameter(s) given to password lookup: %s' % ', '.join(invalid_params))

    # Set defaults
    params['length'] = int(params.get('length', DEFAULT_LENGTH))
    params['encrypt'] = params.get('encrypt', None)

    params['chars'] = params.get('chars', None)
    if params['chars']:
        tmp_chars = []
        if ',,' in params['chars']:
            tmp_chars.append(u',')
        tmp_chars.extend(c for c in params['chars'].replace(',,', ',').split(',') if c)
        params['chars'] = tmp_chars
    else:
        # Default chars for password
        params['chars'] = ['ascii_letters', 'digits', ".,:-_"]

    return relpath, params


class LookupModule(LookupBase):

    def random_password(self, length=DEFAULT_LENGTH, chars=DEFAULT_PASSWORD_CHARS):
        '''
        Return a random password string of length containing only chars.
        NOTE: this was moved from the old ansible utils code, as nothing
              else appeared to use it.
        '''

        password = []
        while len(password) < length:
            new_char = os.urandom(1)
            if new_char in chars:
                password.append(new_char)

        return ''.join(password)

    def random_salt(self):
        salt_chars = ascii_letters + digits + './'
        return self.random_password(length=8, chars=salt_chars)

    def run(self, terms, variables=None, **kwargs):

        ret = []

        for term in terms:
            relpath, params = _parse_parameters(term)

            # get password or create it if file doesn't exist
            path = self._loader.path_dwim(relpath)
            if not os.path.exists(path):
                pathdir = os.path.dirname(path)
                try:
                    makedirs_safe(pathdir, mode=0o700)
                except OSError as e:
                    raise LookupError("cannot create the path for the password lookup: %s (error was %s)" % (pathdir, str(e)))

                chars = "".join(getattr(string, c, c) for c in params['chars']).replace('"', '').replace("'", '')
                password = ''.join(random.choice(chars) for _ in range(params['length']))

                if params['encrypt'] is not None:
                    salt = self.random_salt()
                    content = '%s salt=%s' % (password, salt)
                else:
                    content = password
                with open(path, 'w') as f:
                    os.chmod(path, 0o600)
                    f.write(content + '\n')
            else:
                content = open(path).read().rstrip()

                password = content
                salt = None

                try:
                    sep = content.rindex(' salt=')
                except ValueError:
                    # No salt
                    pass
                else:
                    salt = password[sep + len(' salt='):]
                    password = content[:sep]

                if params['encrypt'] is not None and salt is None:
                    # crypt requested, add salt if missing
                    salt = self.random_salt()
                    content = '%s salt=%s' % (password, salt)
                    with open(path, 'w') as f:
                        os.chmod(path, 0o600)
                        f.write(content + '\n')

            if params['encrypt']:
                password = do_encrypt(password, params['encrypt'], salt=salt)

            ret.append(password)

        return ret
