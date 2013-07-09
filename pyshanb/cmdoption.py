#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

from argparse import ArgumentParser
from __init__ import __version__


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
                            help='The settings file of the application.',
                            metavar='SETTINGS', default='pyshanb.conf')
        parser.add_argument('-u', '--username', dest='username',
                            help='The account username of shanbay.com.',
                            metavar='USERNAME')
        parser.add_argument('-p', '--password', dest='password',
                            help='The account password of shanbay.com.',
                            metavar='PASSWORD')

        group_example = parser.add_mutually_exclusive_group()
        group_example.add_argument('-e', action='store_true',
                                   dest='ask_add_example',
                                   help='Enable "Add example" feature.')
        group_example.add_argument('-E', action='store_false',
                                   dest='ask_add_example',
                                   help='Disable "Add example" feature.')

        group_iciba = parser.add_mutually_exclusive_group()
        group_iciba.add_argument('-i', action='store_true',
                                 dest='enable_iciba',
                                 help='Enable "Get data from iciba.com" feature.')
        group_iciba.add_argument('-I', action='store_false',
                                 dest='enable_iciba',
                                 help='Disable "Get data from iciba.com" feature.')

        group_audio = parser.add_mutually_exclusive_group()
        group_audio.add_argument('-a', action='store_true', dest='auto_play',
                                 help='Enable "Auto play audio" feature.')
        group_audio.add_argument('-A', action='store_false', dest='auto_play',
                                 help='Disable "Auto play audio" feature.')

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
