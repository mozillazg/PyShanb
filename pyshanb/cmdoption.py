#Parse!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理命令行参数
"""

from optparse import OptionParser
from __init__ import __version__


class CmdOption(object):
    def __init__(self):
        usage = 'usage: %prog [-s SETTINGS] [-u USERNAME] [-p PASSWORD]'
        usage += ' [--version]'
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
        # parser.add_option("--version", action="store_false",
                          # dest="verbose",
                          # help="Print the pyshanb version and exit.")

        (self.options, self.args) = parser.parse_args()

    def get_version(self):
        print '1.0'


def main():
    options = CmdOption().options
    print 'settings: ', options.settings
    print 'username: ', options.username
    print 'password: ', options.password

if __name__ == '__main__':
    main()
