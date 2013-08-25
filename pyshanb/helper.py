#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


if os.name == 'nt':
    home = os.environ['USERPROFILE']
    windows = True
else:
    home = os.environ['HOME']
    windows = False
default_configfile = os.path.join(home, 'pyshanb.conf')
