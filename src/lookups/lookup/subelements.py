from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase
from lookups.utils.boolean import boolean

FLAGS = ('skip_missing',)


class LookupModule(LookupBase):

    def _raise_terms_error(self, msg=""):
        raise LookupError("subelements lookup expects a list of two or three items, %s", msg)

    def run(self, terms, variables=None, **kwargs):

        # check lookup terms - check number of terms
        if not isinstance(terms, list) or not 2 <= len(terms) <= 3:
            self._raise_terms_error()

        # first term should be a list (or dict), second a string holding the subkey
        if not isinstance(terms[0], (list, dict)) or not isinstance(terms[1], basestring):
            self._raise_terms_error("first a dict or a list, second a string pointing to the subkey")
        subelements = terms[1].split(".")

        if isinstance(terms[0], dict):  # convert to list:
            if terms[0].get('skipped', False) is not False:
                # the registered result was completely skipped
                return []
            elementlist = []
            for key in terms[0].iterkeys():
                elementlist.append(terms[0][key])
        else:
            elementlist = terms[0]

        # check for optional flags in third term
        flags = {}
        if len(terms) == 3:
            flags = terms[2]
        if not isinstance(flags, dict) and not all([isinstance(key, basestring) and key in FLAGS for key in flags]):
            self._raise_terms_error("the optional third item must be a dict with flags %s" % FLAGS)

        # build_items
        ret = []
        for item0 in elementlist:
            if not isinstance(item0, dict):
                raise LookupBase("subelements lookup expects a dictionary, got '%s'" % item0)
            if item0.get('skipped', False) is not False:
                # this particular item is to be skipped
                continue

            skip_missing = boolean(flags.get('skip_missing', False))
            subvalue = item0
            lastsubkey = False
            sublist = []
            for subkey in subelements:
                if subkey == subelements[-1]:
                    lastsubkey = True
                if not subkey in subvalue:
                    if skip_missing:
                        continue
                    else:
                        raise LookupBase("could not find '%s' key in iterated item '%s'" % (subkey, subvalue))
                if not lastsubkey:
                    if not isinstance(subvalue[subkey], dict):
                        if skip_missing:
                            continue
                        else:
                            raise LookupBase("the key %s should point to a dictionary, got '%s'" % (subkey, subvalue[subkey]))
                    else:
                        subvalue = subvalue[subkey]
                else:  # lastsubkey
                    if not isinstance(subvalue[subkey], list):
                        raise LookupBase("the key %s should point to a list, got '%s'" % (subkey, subvalue[subkey]))
                    else:
                        sublist = subvalue.pop(subkey, [])
            for item1 in sublist:
                ret.append((item0, item1))

        return ret

