from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

CREDSTASH_INSTALLED = False

try:
    import credstash
    CREDSTASH_INSTALLED = True
except ImportError:
    CREDSTASH_INSTALLED = False


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        if not CREDSTASH_INSTALLED:
            raise LookupError('The credstash lookup plugin requires credstash to be installed.')

        ret = []
        for term in terms:
            try:
                val = credstash.getSecret(term, **kwargs)
            except credstash.ItemNotFound:
                raise LookupError('Key {0} not found'.format(term))
            except Exception as e:
                raise LookupError('Encountered exception while fetching {0}: {1}'.format(term, e.message))
            ret.append(val)

        return ret
