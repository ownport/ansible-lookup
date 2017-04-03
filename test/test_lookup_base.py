
from lookups import LookupBase


class Lookup(LookupBase):
    def run(self):
        return 'run()'


def test_lookup_create():

    lb = Lookup()
    assert isinstance(lb, Lookup)
    assert lb.run() == 'run()'


