
from lookups.lookup import first_found


def test_first_found_instance():

    ff = first_found.LookupModule()
    assert isinstance(ff, first_found.LookupModule)


# take a list of files and (optionally) a list of paths
# return the first existing file found in the paths
# [file1, file2, file3], [path1, path2, path3]
# search order is:
# path1/file1
# path1/file2
# path1/file3
# path2/file1
# path2/file2
# path2/file3
# path3/file1
# path3/file2
# path3/file3
def test_first_found_path():

    terms = {
        'files': ['file1', 'file2', 'file3'],
        'paths': ['path1', 'path2', 'path3']
    }
    ff = first_found.LookupModule()
    assert ff.run(terms=terms) == ''

