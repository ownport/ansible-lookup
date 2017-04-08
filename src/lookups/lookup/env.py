from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []
        for term in terms:
            var = term.split()[0]
            ret.append(os.getenv(var, ''))

        return ret
