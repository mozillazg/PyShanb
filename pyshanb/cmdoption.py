#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

from optparse import OptionParser
from __init__ import __version__


class CmdOption(object):
    def __init__(self):
        usage = 'usage: %prog [-s SETTINGS] [-u USERNAME] [-p PASSWORD]\n'
        usage += ' '*18 + '[-e | -E] [-i | -I] [-a | -A] [--version]'
        version = 'PyShanb %s' % '.'.join(map(str, __version__))
        parser = OptionParser(usage=usage, version=version)
        parser.add_option('-s', '--settings', dest='settings',
                          help='The settings file of the application.',
                          metavar='SETTINGS', default='pyshanb.conf')
        parser.add_option('-u', '--username', dest='username',
                          help='The account username of shanbay.com.',
                          metavar='USERNAME', default='')
        parser.add_option('-p', '--password', dest='password',
                          help='The account password of shanbay.com.',
                          metavar='PASSWORD', default='')

        parser.add_option('-e', action='store_true', dest='ask_add_example',
                          help='Enable "Add example" feature.')
        parser.add_option('-E', action='store_false', dest='ask_add_example',
                          help='Disable "Add example" feature.')
        parser.add_option('-i', action='store_true', dest='enable_iciba',
                          help='Enable "Get data from iciba.com" feature.')
        parser.add_option('-I', action='store_false', dest='enable_iciba',
                          help='Disable "Get data from iciba.com" feature.')
        parser.add_option('-a', action='store_true', dest='auto_play',
                          help='Enable "Auto play audio" feature.')
        parser.add_option('-A', action='store_false', dest='auto_play',
                          help='Disable "Auto play audio" feature.')

        (self.options, self.args) = parser.parse_args()


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
