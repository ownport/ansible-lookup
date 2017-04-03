from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase
from lookups.utils.listify import listify_lookup_plugin_terms

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

            if isinstance(term, basestring):
                # convert a variable to a list
                term2 = listify_lookup_plugin_terms(term, templar=self._templar, loader=self._loader)
                # but avoid converting a plain string to a list of one string
                if term2 != [ term ]:
                    term = term2

            if isinstance(term, list):
                # if it's a list, check recursively for items that are a list
                term = self._do_flatten(term, variables)
                ret.extend(term)
            else:
                ret.append(term)

        return ret


    def run(self, terms, variables, **kwargs):

        if not isinstance(terms, list):
            raise LookupError("with_flattened expects a list")

        return self._do_flatten(terms, variables)

