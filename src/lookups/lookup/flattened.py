from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase


class LookupModule(LookupBase):

    def _check_list_of_one_list(self, term):
        # make sure term is not a list of one (list of one..) item
        # return the final non list item if so

        if isinstance(term,list) and len(term) == 1:
            term = term[0]
            if isinstance(term,list):
                term = self._check_list_of_one_list(term)

        return term

    def _do_flatten(self, terms, variables):

        ret = []
        for term in terms:
            term = self._check_list_of_one_list(term)

            if term == 'None' or term == 'null':
                # ignore undefined items
                break

            if isinstance(term, list):
                # if it's a list, check recursively for items that are a list
                term = self._do_flatten(term, variables)
                ret.extend(term)
            else:
                ret.append(term)

        return ret


    def run(self, terms, variables=None, **kwargs):

        if not isinstance(terms, list):
            raise LookupError("flattened expects a list")

        return self._do_flatten(terms, variables)

