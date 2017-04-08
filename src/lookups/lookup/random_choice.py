from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import random

from lookups.lookup import LookupBase

# useful for introducing chaos ... or just somewhat reasonably fair selection
# amongst available mirrors
#
#    tasks:
#        - debug: msg=$item
#          with_random_choice:
#             - one
#             - two 
#             - three

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        return [ random.choice(terms) ]

