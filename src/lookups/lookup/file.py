from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import logging

from lookups.lookup import LookupError
from lookups.lookup import LookupBase

logger = logging.getLogger(__name__)

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []

        basedir = self.get_basedir(variables)

        for term in terms:
            logger.debug("File lookup term: %s" % term)

            # Special handling of the file lookup, used primarily when the
            # lookup is done from a role. If the file isn't found in the
            # basedir of the current file, use dwim_relative to look in the
            # role/files/ directory, and finally the playbook directory
            # itself (which will be relative to the current working dir)

            lookupfile = self._loader.path_dwim_relative(basedir, 'files', term)
            logger.debug("File lookup using %s as file" % lookupfile)

            if lookupfile:
                contents, show_data = self._loader._get_file_contents(lookupfile)
                ret.append(contents.rstrip())
            else:
                raise LookupError("could not locate file in lookup: %s" % term)

        return ret
