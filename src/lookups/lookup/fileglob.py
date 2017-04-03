from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import glob

from lookups.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        basedir = self.get_basedir(variables)

        ret = []
        for term in terms:
            term_file = os.path.basename(term)
            dwimmed_path = self._loader.path_dwim_relative(basedir, 'files', os.path.dirname(term))
            globbed = glob.glob(os.path.join(dwimmed_path, term_file))
            ret.extend(g for g in globbed if os.path.isfile(g))
        return ret
