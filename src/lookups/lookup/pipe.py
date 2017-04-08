from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import subprocess

from lookups.lookup import LookupError
from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []
        for term in terms:
            '''
            http://docs.python.org/2/library/subprocess.html#popen-constructor

            The shell argument (which defaults to False) specifies whether to use the 
            shell as the program to execute. If shell is True, it is recommended to pass 
            args as a string rather than as a sequence

            https://github.com/ansible/ansible/issues/6550
            '''
            term = str(term)

            p = subprocess.Popen(term, cwd=self._loader.get_basedir(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout, stderr) = p.communicate()
            if p.returncode == 0:
                ret.append(stdout.decode("utf-8").rstrip())
            else:
                raise LookupError("lookup_plugin.pipe(%s) returned %d" % (term, p.returncode))
        return ret
