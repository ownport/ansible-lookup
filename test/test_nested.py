
import pytest

from lookups.lookup.nested import LookupModule
from lookups.lookup import LookupError


def test_nested_instance():

    n = LookupModule()
    assert isinstance(n, LookupModule)


def test_nested_run():

    n = LookupModule()

    with pytest.raises(LookupError):
        assert n.run([]) == []

    assert  n.run([
                    [ 'alice', 'bob' ],
                    [ 'clientdb', 'employeedb', 'providerdb' ]
                ]) == [
                    ['alice', 'clientdb'], ['alice', 'employeedb'], ['alice', 'providerdb'],
                    ['bob', 'clientdb'], ['bob', 'employeedb'], ['bob', 'providerdb'],
                ]
