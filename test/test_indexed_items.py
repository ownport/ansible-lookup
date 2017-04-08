
from lookups.lookup.indexed_items import LookupModule

def test_indexed_items_instance():

    ii = LookupModule()
    assert isinstance(ii, LookupModule)


def test_indexed_items_run():

    ii = LookupModule()
    assert ii.run([]) == []
    assert ii.run([1,2,3]) == [(0,1),(1,2),(2,3)]
    assert ii.run([[1,],[2,],3]) == [(0,1),(1,2),(2,3)]
    assert ii.run([(1,),[2,],3]) == [(0,1),(1,2),(2,3)]

