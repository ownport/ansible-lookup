from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        my_list = terms[:]
        if len(my_list) == 0:
            raise LookupError("nested requires at least one element in the nested list")

        my_list.reverse()
        result = my_list.pop()
        while len(my_list) > 0:
            result2 = self._combine(result, my_list.pop())
            result = result2

        new_result = []
        for x in result:
            new_result.append(self._flatten(x))
        return new_result


