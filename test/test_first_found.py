
import pytest

from lookups.lookup import first_found
from lookups.lookup import LookupError

TERMS = [{
    'files': ['file1', 'file2', 'file3'],
    'paths': ['path1', 'path2', 'path3']
}]

def test_first_found_instance():

    ff = first_found.LookupModule()
    assert isinstance(ff, first_found.LookupModule)

def test_first_found_no_paths():

    ff = first_found.LookupModule()
    with pytest.raises(LookupError):
        assert ff.run(terms=TERMS) == ''

def test_first_found_paths(tmpdir):

    p = tmpdir.mkdir("path1").join("file3")

    ff = first_found.LookupModule()
    with pytest.raises(LookupError):
        assert ff.run(terms=TERMS) == 'path1/file3'
