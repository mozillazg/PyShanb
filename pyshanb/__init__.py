#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyShanb - 命令行下的扇贝词典
"""

import datetime
import os
import subprocess

__title__ = 'pyshanb'
__version_info__ = (0, 5, 4, 'final', 0)
__author__ = 'mozillazg'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 mozillazg'


# modified from django(https://github.com/django/django/)
def get_version(version=None):
    """Return a PEP 386-compliant version number from VERSION."""
    if version is None:
        version = __version_info__
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    # | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev%s' % git_changeset

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return str(main + sub)


def get_git_changeset():
    """Return a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.

    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True, cwd=repo_dir,
                               universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')

__version__ = get_version(__version_info__)
