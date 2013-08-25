#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

from argparse import ArgumentParser

from __init__ import __version__
from helper import default_configfile


class CmdOption(object):
    def __init__(self):
        self.version = 'PyShanb %s' % __version__
        description = 'An command line tool for shanbay.com.'
        self.parser = ArgumentParser(description=description)

        self.parser.add_argument('-V', '--version', action='version',
                                 version=self.version)
        self.parser.add_argument('-s', '--settings', dest='settings',
                                 help='the settings file of the application',
                                 default=default_configfile)
        self.parser.add_argument('-u', '--username', dest='username',
                                 help='the account username of shanbay.com')
        self.parser.add_argument('-p', '--password', dest='password',
                                 help='the account password of shanbay.com')

        group_example = self.parser.add_mutually_exclusive_group()
        group_example.add_argument('-e', action='store_true', default=None,
                                   dest='ask_add_example',
                                   help='enable "Add example" feature')
        group_example.add_argument('-E', action='store_false', default=None,
                                   dest='ask_add_example',
                                   help='disable "Add example" feature')

        group_iciba = self.parser.add_mutually_exclusive_group()
        group_iciba.add_argument('-i', action='store_true',
                                 dest='enable_iciba',
                                 help='enable "Get data from iciba.com" '
                                 'feature', default=None)
        group_iciba.add_argument('-I', action='store_false',
                                 dest='enable_iciba',
                                 help='disable "Get data from iciba.com" '
                                 'feature', default=None)

        group_audio = self.parser.add_mutually_exclusive_group()
        group_audio.add_argument('-a', action='store_true', dest='auto_play',
                                 help='enable "Auto play audio" feature',
                                 default=None)
        group_audio.add_argument('-A', action='store_false', dest='auto_play',
                                 help='disable "Auto play audio" feature',
                                 default=None)

        self.parser.add_argument('--color', dest='colour', default='green',
                                 choices=['black', 'white', 'red', 'green',
                                          'yellow', 'blue', 'magenta', 'cyan',
                                          'gray'],
                                 help='colorize keyword (default: green)')

        self.options = self.parser.parse_args()


def main():
    options = CmdOption().options
    print 'settings: ', options.settings
    print 'username: ', options.username
    print 'password: ', options.password
    print 'ask_add_example: ', options.ask_add_example
    print 'enable_iciba: ', options.enable_iciba
    print 'auto_play: ', options.auto_play
    print 'color: ', options.colour

if __name__ == '__main__':
    main()
