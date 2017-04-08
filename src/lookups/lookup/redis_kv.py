from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

HAVE_REDIS=False
try:
    import redis        # https://github.com/andymccurdy/redis-py/
    HAVE_REDIS=True
except ImportError:
    pass

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

# ==============================================================
# REDISGET: Obtain value from a GET on a Redis key. Terms
# expected: 0 = URL, 1 = Key
# URL may be empty, in which case redis://localhost:6379 assumed
# --------------------------------------------------------------

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        if not HAVE_REDIS:
            raise LookupError("Can't LOOKUP(redis_kv): module redis is not installed")

        ret = []
        for term in terms:
            (url,key) = term.split(',')
            if url == "":
                url = 'redis://localhost:6379'

            # urlsplit on Python 2.6.1 is broken. Hmm. Probably also the reason
            # Redis' from_url() doesn't work here.

            p = '(?P<scheme>[^:]+)://?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

            try:
                m = re.search(p, url)
                host = m.group('host')
                port = int(m.group('port'))
            except AttributeError:
                raise LookupError("Bad URI in redis lookup")

            try:
                conn = redis.Redis(host=host, port=port)
                res = conn.get(key)
                if res is None:
                    res = ""
                ret.append(res)
            except:
                ret.append("")  # connection failed or key not found
        return ret
