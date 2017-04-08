
from lookups.lookup.items import LookupModule


def test_items_instance():

    i = LookupModule()
    assert isinstance(i, LookupModule)


def test_items_run():

    i = LookupModule()
    assert i.run(terms=[]) == []
    assert i.run(terms=[1,2,3]) == [1,2,3]
    assert i.run(terms=[[],1,2,3]) == [1,2,3]
    assert i.run(terms=[[1,2,3],1,2,3]) == [1,2,3,1,2,3]
    assert i.run(terms=[[1,2,3],[1,2],1,2,3]) == [1,2,3,1,2,1,2,3]

