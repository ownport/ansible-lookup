from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import logging
from abc import ABCMeta, abstractmethod

from lookups.six import with_metaclass

logger = logging.getLogger(__name__)

__all__ = ['LookupBase']


class LookupError(Exception):
    pass


class LookupBase(with_metaclass(ABCMeta, object)):
    def __init__(self, loader=None, templar=None, **kwargs):
        self._loader = loader
        self._templar = templar

    def get_basedir(self, variables):
        if 'role_path' in variables:
            return variables['role_path']
        else:
            return self._loader.get_basedir()

    @staticmethod
    def _flatten(terms):
        ret = []
        for term in terms:
            if isinstance(term, (list, tuple)):
                ret.extend(term)
            else:
                ret.append(term)
        return ret

    @staticmethod
    def _combine(a, b):
        results = []
        for x in a:
            for y in b:
                results.append(LookupBase._flatten([x,y]))
        return results

    @staticmethod
    def _flatten_hash_to_list(terms):
        ret = []
        for key in terms:
            ret.append({'key': key, 'value': terms[key]})
        return ret

    @abstractmethod
    def run(self, terms, variables=None, **kwargs):
        """
        When the playbook specifies a lookup, this method is run.  The
        arguments to the lookup become the arguments to this method.  One
        additional keyword argument named ``variables`` is added to the method
        call.  It contains the variables available to ansible at the time the
        lookup is templated.  For instance::

            "{{ lookup('url', 'https://toshio.fedorapeople.org/one.txt', validate_certs=True) }}"

        would end up calling the lookup plugin named url's run method like this::
            run(['https://toshio.fedorapeople.org/one.txt'], variables=available_variables, validate_certs=True)

        Lookup plugins can be used within playbooks for looping.  When this
        happens, the first argument is a list containing the terms.  Lookup
        plugins can also be called from within playbooks to return their
        values into a variable or parameter.  If the user passes a string in
        this case, it is converted into a list.

        Errors encountered during execution should be returned by raising
        AnsibleError() with a message describing the error.

        Any strings returned by this method that could ever contain non-ascii
        must be converted into python's unicode type as the strings will be run
        through jinja2 which has this requirement.  You can use::

            from ansible.module_utils.unicode import to_unicode
            result_string = to_unicode(result_string)
        """
        pass

LOOKUP_ACTIONS = {
    'cartesian': 'lookups.lookup.cartesian',
    'consul_kv': 'lookups.lookup.consul_kv',
    'credstash': 'lookups.lookup.credstash',
    'csvfile': 'lookups.lookup.csvfile',
    'dict': 'lookups.lookup.dict',
    'dig': 'lookups.lookup.dig',
    'dnstxt': 'lookups.lookup.dnstxt',
    'env': 'lookups.lookup.env',
    'etcd': 'lookups.lookup.etcd',
    'file': 'lookups.lookup.file',
    'fileglob': 'lookups.lookup.fileglob',
    'first_found': 'lookups.lookup.first_found',
    'flattened': 'lookups.lookup.flattened',
    'hashi_vault': 'lookups.lookup.hashi_vault',
    'indexed_items': 'lookups.lookup.indexed_items',
    'ini': 'lookups.lookup.ini',
    'items': 'lookups.lookup.items',
    'lines': 'lookups.lookup.lines',
    'nested': 'lookups.lookup.nested',
    'password': 'lookups.lookup.password',
    'pipe': 'lookups.lookup.pipe',
    'random_choice': 'lookups.lookup.random_choice',
    'redis_kv': 'lookups.lookup.redis_kv',
    'sequence': 'lookups.lookup.sequence',
    'shelvefile': 'lookups.lookup.shelvefile',
    'subelements': 'lookups.lookup.subelements',
    'together': 'lookups.lookup.together',
    'url': 'lookups.lookup.url',
}