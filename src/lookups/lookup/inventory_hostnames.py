from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from lookups.lookup import LookupBase
from ansible.inventory import Inventory

class LookupModule(LookupBase):

    def get_hosts(self, variables, pattern):
        hosts = []
        if pattern[0] in ('!','&'):
            obj = pattern[1:]
        else:
            obj = pattern

        if obj in variables['groups']:
            hosts = variables['groups'][obj]
        elif obj in variables['groups']['all']:
            hosts = [obj]
        return hosts

    def run(self, terms, variables=None, **kwargs):

        host_list = []

        for term in terms:
            patterns = Inventory.order_patterns(Inventory.split_host_pattern(term))

            for p in patterns:
                that = self.get_hosts(variables, p)
                if p.startswith("!"):
                    host_list = [ h for h in host_list if h not in that]
                elif p.startswith("&"):
                    host_list = [ h for h in host_list if h in that ]
                else:
                    host_list.extend(that)

        # return unique list
        return list(set(host_list))
