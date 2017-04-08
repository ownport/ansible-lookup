from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import shelve
import os

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

class LookupModule(LookupBase):


    def read_shelve(self, shelve_filename, key):
        """
        Read the value of "key" from a shelve file
        """
        d = shelve.open(shelve_filename)
        res = d.get(key, None)
        d.close()
        return res

    def run(self, terms, variables=None, **kwargs):

        if not isinstance(terms, list):
            terms = [ terms ]

        ret = []

        for term in terms:
            playbook_path = None
            relative_path = None

            paramvals = {"file": None, "key": None}
            params = term.split()

            try:
                for param in params:
                    name, value = param.split('=')
                    assert(name in paramvals)
                    paramvals[name] = value

            except (ValueError, AssertionError) as e:
                # In case "file" or "key" are not present
                raise LookupError(e)

            file = paramvals['file']
            key = paramvals['key']
            basedir_path  = self._loader.path_dwim(file)

            # Search also in the role/files directory and in the playbook directory
            if 'role_path' in variables:
                relative_path = self._loader.path_dwim_relative(variables['role_path'], 'files', file)
            if 'playbook_dir' in variables:
                playbook_path = self._loader.path_dwim_relative(variables['playbook_dir'],'files', file)

            for path in (basedir_path, relative_path, playbook_path):
                if path and os.path.exists(path):
                    res = self.read_shelve(path, key)
                    if res is None:
                        raise LookupError("Key %s not found in shelve file %s" % (key, file))
                    # Convert the value read to string
                    ret.append(str(res))
                    break
            else:
                raise LookupError("Could not locate shelve file in lookup: %s" % file)

        return ret
