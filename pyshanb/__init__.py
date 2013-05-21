#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyShanb - 命令行下的扇贝词典
"""


__title__ = 'pyshanb'
__version_info__ = (0, 5, 2, 'final', 0)
__author__ = 'mozillazg'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 mozillazg'


# modified from django(https://github.com/django/django/)
def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."
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

__version__ = get_version(__version_info__)