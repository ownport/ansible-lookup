from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):

        if not isinstance(terms, list):
            raise LookupError("with_indexed_items expects a list")

        items = self._flatten(terms)
        return zip(range(len(items)), items)

