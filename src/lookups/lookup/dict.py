from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms, varibles=None, **kwargs):

        # Expect any type of Mapping, notably hostvars
        if not isinstance(terms, collections.Mapping):
            raise LookupError("with_dict expects a dict")

        return self._flatten_hash_to_list(terms)
