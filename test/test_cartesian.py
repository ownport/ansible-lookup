
from lookups.lookup import cartesian


def test_cartesian_create():

    lm = cartesian.LookupModule()
    assert isinstance(lm, cartesian.LookupModule)


def test_cartesian_run_list():

    lm = cartesian.LookupModule()

    assert lm.run(terms=[('1'), ("a")]) == [ ['1', 'a'], ]

    assert lm.run(terms=[('1'), ("a", "b")]) == [ ['1', 'a'], ['1', 'b'], ]

    assert lm.run(terms=[('1','2','3'), ("a", "b")]) == [
                    ['1', 'a'], ['1', 'b'], ['2', 'a'], ['2', 'b'], ['3', 'a'], ['3', 'b']
    ]

