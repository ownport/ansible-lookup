
from lookups.lookup.env import LookupModule


def test_env_instance():

    e = LookupModule()
    assert isinstance(e, LookupModule)


def test_evn_run():

    e = LookupModule()
    assert e.run([]) == []
    assert len(e.run(['PATH',])) == 1
    assert e.run(['NONE',]) == ['',]