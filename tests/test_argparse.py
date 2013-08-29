#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""测试命令行参数."""

from pyshanb.cmdoption import CmdOption
from pyshanb.helper import default_configfile

args = CmdOption()
parser = args.parser


def test_default():
    options = parser.parse_args([])
    assert options.settings == default_configfile
    assert options.username is None
    assert options.password is None
    assert options.ask_add_example is None
    assert options.enable_iciba is None
    assert options.auto_play is None
    assert options.colour == 'green'
    assert options.plugins == []


def test_args_true():
    options = parser.parse_args(['-s', 'foobar.conf', '-u', 'foo',
                                 '-p', 'bar', '-e', '-i', '-a', '--color',
                                 'red'])
    assert options.settings == 'foobar.conf'
    assert options.username == 'foo'
    assert options.password == 'bar'
    assert options.ask_add_example
    assert options.enable_iciba
    assert options.auto_play
    assert options.colour == 'red'


def test_args_false():
    options = parser.parse_args(['-E', '-I', '-A'])
    assert not options.ask_add_example
    assert not options.enable_iciba
    assert not options.auto_play


def test_args_plugin():
    options = parser.parse_args(['--plugin', 'youdao'])
    assert options.plugins == ['youdao']
