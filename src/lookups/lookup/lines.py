from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import subprocess
from lookups.lookup import LookupError
from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []
        for term in terms:
            p = subprocess.Popen(term, cwd=self._loader.get_basedir(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout, stderr) = p.communicate()
            if p.returncode == 0:
                ret.extend(stdout.splitlines())
            else:
                raise LookupError("lookup.lines(%s) returned %d" % (term, p.returncode))
        return ret
