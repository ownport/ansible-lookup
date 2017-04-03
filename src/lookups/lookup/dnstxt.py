from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

HAVE_DNS=False
try:
    import dns.resolver
    from dns.exception import DNSException
    HAVE_DNS=True
except ImportError:
    pass

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

# ==============================================================
# DNSTXT: DNS TXT records
#
#       key=domainname
# TODO: configurable resolver IPs
# --------------------------------------------------------------

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        if HAVE_DNS == False:
            raise LookupError("Can't LOOKUP(dnstxt): module dns.resolver is not installed")

        ret = []
        for term in terms:
            domain = term.split()[0]
            string = []
            try:
                answers = dns.resolver.query(domain, 'TXT')
                for rdata in answers:
                    s = rdata.to_text()
                    string.append(s[1:-1])  # Strip outside quotes on TXT rdata

            except dns.resolver.NXDOMAIN:
                string = 'NXDOMAIN'
            except dns.resolver.Timeout:
                string = ''
            except DNSException as e:
                raise LookupError("dns.resolver unhandled exception", e)

            ret.append(''.join(string))

        return ret

