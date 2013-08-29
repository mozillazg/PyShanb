#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._werkzeug import import_string, find_modules


def find_all_plugins_name():
    modules = find_modules('pyshanb.plugins', silent=True)
    return [x.split('.')[-1] for x in modules]


def plugins_output(plugins, word):
    all_plugins = find_all_plugins_name()
    for plugin in plugins:
        if plugin in all_plugins:
            plugin = import_string('pyshanb.plugins.' + plugin, silent=True)
            plugin.output(word)


if __name__ == '__main__':
    print find_all_plugins_name()
    plugins_output(['youdao'], 'hello')
