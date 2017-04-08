
from lookups.lookup.flattened import LookupModule


def test_flattened_instance():

    f = LookupModule()
    assert isinstance(f, LookupModule)


def test_flattened_run():

    f = LookupModule()
    assert f.run(terms=[]) == []
    assert f.run(terms=[1,2,3]) == [1,2,3]
    assert f.run(terms=[[],1,2,3]) == [1,2,3]
    assert f.run(terms=[[1,2,3],1,2,3]) == [1,2,3,1,2,3]
    assert f.run(terms=[[1,2,3],[1,2],1,2,3]) == [1,2,3,1,2,1,2,3]

