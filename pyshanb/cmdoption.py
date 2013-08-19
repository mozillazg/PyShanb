#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

import os
from argparse import ArgumentParser
from __init__ import __version__


if os.name == 'nt':
    home = os.environ['userprofile']
else:
    home = os.environ['home']
configfile = os.path.join(home, 'pyshanb.conf')


class CmdOption(object):
    def __init__(self):
        # usage = 'usage: %(prog)s [-s SETTINGS] [-u USERNAME] [-p PASSWORD]\n'
        # usage += ' '*18 + '[-e | -E] [-i | -I] [-a | -A] [--version]'
        version = 'PyShanb %s' % __version__
        description = 'An command line tool for shanbay.com.'
        parser = ArgumentParser(description=description)

        parser.add_argument('-V', '--version', action='version',
                            version=version)
        parser.add_argument('-s', '--settings', dest='settings',
                            help='the settings file of the application',
                            metavar='SETTINGS', default=configfile)
        parser.add_argument('-u', '--username', dest='username',
                            help='the account username of shanbay.com',
                            metavar='USERNAME')
        parser.add_argument('-p', '--password', dest='password',
                            help='the account password of shanbay.com',
                            metavar='PASSWORD')

        group_example = parser.add_mutually_exclusive_group()
        group_example.add_argument('-e', action='store_true',
                                   dest='ask_add_example',
                                   help='enable "Add example" feature')
        group_example.add_argument('-E', action='store_false',
                                   dest='ask_add_example',
                                   help='disable "Add example" feature')

        group_iciba = parser.add_mutually_exclusive_group()
        group_iciba.add_argument('-i', action='store_true',
                                 dest='enable_iciba',
                                 help='enable "Get data from iciba.com" feature')
        group_iciba.add_argument('-I', action='store_false',
                                 dest='enable_iciba',
                                 help='disable "Get data from iciba.com" feature')

        group_audio = parser.add_mutually_exclusive_group()
        group_audio.add_argument('-a', action='store_true', dest='auto_play',
                                 help='enable "Auto play audio" feature')
        group_audio.add_argument('-A', action='store_false', dest='auto_play',
                                 help='disable "Auto play audio" feature')

        parser.add_argument('--color', dest='colour',
                            help='colorize keyword (default: green). '
                            'COLOR may be "black", "white", "red", "green", '
                            '"yellow", "blue", "magenta", "cyan", or "gray"',
                            metavar='COLOR', default='green')

        self.options = parser.parse_args()


def main():
    options = CmdOption().options
    print 'settings: ', options.settings
    print 'username: ', options.username
    print 'password: ', options.password
    print 'ask_add_example: ', options.ask_add_example
    print 'enable_iciba: ', options.enable_iciba
    print 'auto_play: ', options.auto_play

if __name__ == '__main__':
    main()
