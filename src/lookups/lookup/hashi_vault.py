from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from lookups.lookup import LookupError
from lookups.lookup import LookupBase


HASHI_VAULT_ADDR = 'http://127.0.0.1:8200'
if os.getenv('VAULT_ADDR') is not None:
    HASHI_VAULT_ADDR = os.environ['VAULT_ADDR']


class HashiVault:
    def __init__(self, **kwargs):
        try:
            import hvac
        except ImportError:
            raise LookupError("Please pip install hvac to use this module")

        self.url = kwargs.pop('url')
        self.secret = kwargs.pop('secret')
        self.token = kwargs.pop('token')

        self.client = hvac.Client(url=self.url, token=self.token)

        if self.client.is_authenticated():
            pass
        else:
            raise LookupError("Invalid Hashicorp Vault Token Specified")

    def get(self):
        data = self.client.read(self.secret)
        if data is None:
            raise LookupError("The secret %s doesn't seem to exist" % self.secret)
        else:
            return data['data']['value']


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        vault_args = terms[0].split(' ')
        vault_dict = {}
        ret = []

        for param in vault_args:
            key, value = param.split('=')
            vault_dict[key] = value

        vault_conn = HashiVault(**vault_dict)

        for term in terms:
           key = term.split()[0]
           value = vault_conn.get()
           ret.append(value)
        return ret
