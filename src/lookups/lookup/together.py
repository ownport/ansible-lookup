from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from itertools import izip_longest

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

class LookupModule(LookupBase):
    """
    Transpose a list of arrays:
    [1, 2, 3], [4, 5, 6] -> [1, 4], [2, 5], [3, 6]
    Replace any empty spots in 2nd array with None:
    [1, 2], [3] -> [1, 3], [2, None]
    """

    def run(self, terms, variables=None, **kwargs):

        my_list = terms[:]
        if len(my_list) == 0:
            raise LookupError("together requires at least one element in each list")

        return [self._flatten(x) for x in izip_longest(*my_list, fillvalue=None)]

