from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import codecs
import csv

from lookups.lookup import LookupError
from lookups.lookup import LookupBase
from lookups.utils.unicode import to_bytes, to_str, to_unicode


class CSVRecoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding='utf-8'):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class CSVReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = CSVRecoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [to_unicode(s) for s in row]

    def __iter__(self):
        return self


class LookupModule(LookupBase):

    def read_csv(self, filename, key, delimiter, encoding='utf-8', dflt=None, col=1):

        try:
            f = open(filename, 'r')
            creader = CSVReader(f, delimiter=to_bytes(delimiter), encoding=encoding)

            for row in creader:
                if row[0] == key:
                    return row[int(col)]
        except Exception as e:
            raise LookupError("csvfile: %s" % to_str(e))

        return dflt

    def run(self, terms, variables=None, **kwargs):

        basedir = self.get_basedir(variables)

        ret = []

        for term in terms:
            params = term.split()
            key = params[0]

            paramvals = {
                'col' : "1",          # column to return
                'default' : None,
                'delimiter' : "TAB",
                'file' : 'ansible.csv',
                'encoding' : 'utf-8',
            }

            # parameters specified?
            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    assert(name in paramvals)
                    paramvals[name] = value
            except (ValueError, AssertionError) as e:
                raise LookupError(e)

            if paramvals['delimiter'] == 'TAB':
                paramvals['delimiter'] = "\t"

            lookupfile = self._loader.path_dwim_relative(basedir, 'files', paramvals['file'])
            var = self.read_csv(lookupfile, key, paramvals['delimiter'], paramvals['encoding'], paramvals['default'], paramvals['col'])
            if var is not None:
                if type(var) is list:
                    for v in var:
                        ret.append(v)
                else:
                    ret.append(var)
        return ret
