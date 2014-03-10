#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""测试插件模块."""

from pyshanb.plugin import find_all_plugins_name


def test_plugin():
    assert find_all_plugins_name() == ['vocabulary', 'youdao']
