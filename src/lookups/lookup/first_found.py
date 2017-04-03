from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

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

# first file found with os.path.exists() is returned
# no file matches raises ansibleerror
# EXAMPLES
#  - name: copy first existing file found to /some/file
#    action: copy src=$item dest=/some/file
#    with_first_found: 
#     - files: foo ${inventory_hostname} bar
#       paths: /tmp/production /tmp/staging

# that will look for files in this order:
# /tmp/production/foo
#                 ${inventory_hostname}
#                 bar
# /tmp/staging/foo
#              ${inventory_hostname}
#              bar
                  
#  - name: copy first existing file found to /some/file
#    action: copy src=$item dest=/some/file
#    with_first_found: 
#     - files: /some/place/foo ${inventory_hostname} /some/place/else

#  that will look for files in this order:
#  /some/place/foo
#  $relative_path/${inventory_hostname}
#  /some/place/else

# example - including tasks:
#  tasks:
#  - include: $item
#    with_first_found:
#     - files: generic
#       paths: tasks/staging tasks/production
# this will include the tasks in the file generic where it is found first (staging or production)

# example simple file lists
#tasks:
#- name: first found file
#  action: copy src=$item dest=/etc/file.cfg
#  with_first_found:
#  - files: foo.${inventory_hostname} foo


# example skipping if no matched files
# First_found also offers the ability to control whether or not failing
# to find a file returns an error or not
#
#- name: first found file - or skip
#  action: copy src=$item dest=/etc/file.cfg
#  with_first_found:
#  - files: foo.${inventory_hostname}
#    skip: true

# example a role with default configuration and configuration per host
# you can set multiple terms with their own files and paths to look through.
# consider a role that sets some configuration per host falling back on a default config.
#
#- name: some configuration template
#  template: src={{ item }} dest=/etc/file.cfg mode=0444 owner=root group=root
#  with_first_found:
#   - files:
#      - ${inventory_hostname}/etc/file.cfg
#     paths:
#      - ../../../templates.overwrites
#      - ../../../templates
#   - files:
#      - etc/file.cfg
#     paths:
#      - templates

# the above will return an empty list if the files cannot be found at all
# if skip is unspecificed or if it is set to false then it will return a list 
# error which can be caught bye ignore_errors: true for that action.

# finally - if you want you can use it, in place to replace first_available_file:
# you simply cannot use the - files, path or skip options. simply replace
# first_available_file with with_first_found and leave the file listing in place
#
#
#  - name: with_first_found like first_available_file
#    action: copy src=$item dest=/tmp/faftest
#    with_first_found:
#     - ../files/foo
#     - ../files/bar
#     - ../files/baz
#    ignore_errors: true


import os

from lookups.lookup import LookupError
from lookups.lookup import LookupBase
from lookups.utils.boolean import boolean


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        anydict = False
        skip = False

        for term in terms:
            if isinstance(term, dict):
                anydict = True

        total_search = []
        if anydict:
            for term in terms:
                if isinstance(term, dict):
                    files = term.get('files', [])
                    paths = term.get('paths', [])
                    skip  = boolean(term.get('skip', False))

                    filelist = files
                    if isinstance(files, basestring):
                        files = files.replace(',', ' ')
                        files = files.replace(';', ' ')
                        filelist = files.split(' ')

                    pathlist = paths
                    if paths:
                        if isinstance(paths, basestring):
                            paths = paths.replace(',', ' ')
                            paths = paths.replace(':', ' ')
                            paths = paths.replace(';', ' ')
                            pathlist = paths.split(' ')

                    if not pathlist:
                        total_search = filelist
                    else:
                        for path in pathlist:
                            for fn in filelist:
                                f = os.path.join(path, fn)
                                total_search.append(f)
                else:
                    total_search.append(term)
        else:
            total_search = self._flatten(terms)

        roledir = variables.get('roledir')
        for fn in total_search:
            try:
                fn = self._templar.template(fn)
            except (AnsibleUndefinedVariable, UndefinedError) as e:
                continue

            if os.path.isabs(fn) and os.path.exists(fn):
                return [fn]
            else:
                if roledir is not None:
                    # check the templates and vars directories too,if they exist
                    for subdir in ('templates', 'vars', 'files'):
                        path = self._loader.path_dwim_relative(roledir, subdir, fn)
                        if os.path.exists(path):
                            return [path]

                # if none of the above were found, just check the
                # current filename against the current dir
                path = self._loader.path_dwim(fn)
                if os.path.exists(path):
                    return [path]
        else:
            if skip:
                return []
            else:
                raise LookupError("No file was found when using with_first_found. Use the 'skip: true' option to allow this task to be skipped if no files are found")

