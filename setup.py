#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pyshanb

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = [
    'requests>=1.1.0'
]

packages = [
    'pyshanb',
]

def long_description():
    md =open('README.md').read() + '\n\n' + open('ChangeLog.md').read()
    return md

setup(
    name='pyshanb',
    version=pyshanb.__version__,
    description=pyshanb.__doc__.strip(),
    long_description=long_description(),
    url='https://github.com/mozillazg/PyShanb',
    download_url='https://github.com/mozillazg/PyShanb',
    author=pyshanb.__author__,
    author_email='mozillazg101@gmail.com',
    license=pyshanb.__license__,
    packages=packages,
    package_data={'': ['LICENSE.txt'], 'pyshanb': ['*.conf']},
    package_dir={'pyshanb': 'pyshanb'},
    include_package_data=True,
    install_requires=requirements,
    # setup_requires=['sphinx'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'shanbay = pyshanb.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
    ],
)