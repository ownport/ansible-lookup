from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from itertools import product

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

class LookupModule(LookupBase):
    """
    Create the cartesian product of lists
    [1, 2, 3], [a, b] -> [1, a], [1, b], [2, a], [2, b], [3, a], [3, b]
    """

    def run(self, terms, variables=None, **kwargs):

        my_list = terms[:]
        if len(my_list) == 0:
            raise LookupError("with_cartesian requires at least one element in each list")

        return [self._flatten(x) for x in product(*my_list)]

