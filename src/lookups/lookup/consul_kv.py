from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

'''
Lookup plugin to grab metadata from a consul key value store.
============================================================

Plugin will lookup metadata for a playbook from the key value store in a
consul cluster. Values can be easily set in the kv store with simple rest
commands e.g.

curl -X PUT -d 'some-value' http://localhost:8500/v1/kv/ansible/somedata

this can then be looked up in a playbook as follows

- debug: msg='key contains {{item}}'
  with_consul_kv:
    - 'key/to/retrieve'


Parameters can be provided after the key be more specific about what to retrieve e.g.

- debug: msg='key contains {{item}}'
  with_consul_kv:
    - 'key/to recurse=true token=E6C060A9-26FB-407A-B83E-12DDAFCB4D98')}}'

recurse: if true, will retrieve all the values that have the given key as prefix
index: if the key has a value with the specified index then this is returned
       allowing access to historical values.
token: acl token to allow access to restricted values.

By default this will lookup keys via the consul agent running on http://localhost:8500
this can be changed by setting the env variable 'ANSIBLE_CONSUL_URL' to point to the url
of the kv store you'd like to use.

'''

######################################################################

import os
from urlparse import urlparse
from lookups.lookup import LookupError
from lookups.lookup import LookupBase

try:
    import json
except ImportError:
    import simplejson as json

try:
    import consul
    HAS_CONSUL = True
except ImportError as e:
    HAS_CONSUL = False


class LookupModule(LookupBase):

    def __init__(self, loader=None, templar=None, **kwargs):

        super(LookupModule, self).__init__(loader, templar, **kwargs)

        self.agent_url = 'http://localhost:8500'
        if os.getenv('ANSIBLE_CONSUL_URL') is not None:
            self.agent_url = os.environ['ANSIBLE_CONSUL_URL']

    def run(self, terms, variables=None, **kwargs):

        if not HAS_CONSUL:
            raise LookupError('python-consul is required for consul_kv lookup. see http://python-consul.readthedocs.org/en/latest/#installation')

        u = urlparse(self.agent_url)
        consul_api = consul.Consul(host=u.hostname, port=u.port)

        values = []
        try:
            for term in terms:
                params = self.parse_params(term)
                results = consul_api.kv.get(params['key'],
                                            token=params['token'],
                                            index=params['index'],
                                            recurse=params['recurse'])
                if results[1]:
                    # responds with a single or list of result maps
                    if isinstance(results[1], list):
                        for r in results[1]:
                            values.append(r['Value'])
                    else:
                        values.append(results[1]['Value'])
        except Exception as e:
            raise LookupError(
                "Error locating '%s' in kv store. Error was %s" % (term, e))

        return values

    def parse_params(self, term):
        params = term.split(' ')

        paramvals = {
            'key': params[0],
            'token': None,
            'recurse': False,
            'index': None
        }

        # parameters specified?
        try:
            for param in params[1:]:
                if param and len(param) > 0:
                    name, value = param.split('=')
                    assert name in paramvals, "% not a valid consul lookup parameter" % name
                    paramvals[name] = value
        except (ValueError, AssertionError) as e:
            raise LookupError(e)

        return paramvals
