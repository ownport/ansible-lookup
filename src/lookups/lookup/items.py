from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms, **kwargs):

        return self._flatten(terms)

