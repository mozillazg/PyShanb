#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import sys


class Settings(object):
    def __init__(self, configfile='pyshanb.conf', username='', password=''):
        self.config_file = configfile  # 配置文件名称
        self.configs = ConfigParser.RawConfigParser()
        # 读取配置文件。
        self.configs.read(self.config_file)
        self.has_username = username
        self.has_password = password

        # 如果没有配置文件或没有用户名及密码的配置项
        # 则创建默认配置文件
        if not (os.path.isfile(self.config_file)
                and self.configs.has_section('General')
                and self.configs.has_option('General', 'username')
                and self.configs.has_option('General', 'password')):
            self.default_config(username, password)

    @property
    def settings(self):
        self.get_settings(self.has_username, self.has_password)
        return self

    def default_config(self, username='', password=''):
        """设置默认配置
        """
        self.configs.add_section('General')
        self.configs.set('General', 'username', username)
        self.configs.set('General', 'password', password)
        self.configs.set('General', 'auto_play', '1')
        self.configs.set('General', 'auto_add', '0')
        self.configs.set('General', 'ask_add', '1')
        self.configs.set('General', 'enable_en_definition', '0')
        self.configs.set('General', 'enable_example', '0')

        self.configs.add_section('iciba')
        self.configs.set('iciba', 'enabled', '0')
        self.configs.set('iciba', 'enable_audio', '1')
        self.configs.set('iciba', 'lang', 'en-US')
        self.configs.set('iciba', 'enable_syllable', '1')
        self.configs.set('iciba', 'enable_definition', '1')
        self.configs.set('iciba', 'enable_extra', '1')

        with open(self.config_file, 'wb') as config_file:
            self.configs.write(config_file)

    def get_option_value(self, func, section, option, default):
        """执行相关获取配置项值的操作，
        并使用默认值代替异常信息
        """
        try:
            return func(section, option)
        except:
            return default

    def get_settings(self, has_username=False, has_password=False):
        """获取配置文件中相关选项的值
        """
        configs = self.configs
        CONFIGFILE = self.config_file
        get_option_value = self.get_option_value
        # 用户名及密码
        self.username = configs.get('General', 'username')
        self.password = configs.get('General', 'password')
        if not ((self.username or has_username)
                and (self.password or has_password)):
                a = u'Please configure your username and/or password'
                b = 'or command line option, like below:\n'
                b += 'pyshanb.py -u root -p abc'
                sys.exit(u'%s by editor config file:\n%s\n%s'
                         % (a, os.path.realpath(CONFIGFILE), b))

        # 其他非必需项。如果未配置相关选项则使用默认值
        self.auto_play = get_option_value(configs.getboolean, 'General',
                                          'auto_play', False)
        self.auto_add = get_option_value(configs.getboolean, 'General',
                                         'auto_add', False)
        self.ask_add = get_option_value(configs.getboolean, 'General',
                                        'ask_add', True)

        self.enable_en_definition = get_option_value(configs.getboolean,
                                                     'General',
                                                     'enable_en_definition',
                                                     False)
        self.enable_example = get_option_value(configs.getboolean, 'General',
                                               'enable_example', False)

        # iciba
        self.enable_iciba = get_option_value(configs.getboolean, 'iciba',
                                             'enabled', False)
        self.enable_icb_audio = get_option_value(configs.getboolean,
                                                 'iciba', 'enable_audio', True)
        self.enable_icb_lang = get_option_value(configs.get, 'iciba', 'lang',
                                                'en-US')
        self.enable_icb_syllable = get_option_value(configs.getboolean,
                                                    'iciba',
                                                    'enable_syllable', True)
        self.enable_icb_definition = get_option_value(configs.getboolean,
                                                      'iciba',
                                                      'enable_definition',
                                                      True)
        self.enable_icb_extra = get_option_value(configs.getboolean, 'iciba',
                                                 'enable_extra', True)

        #
        self.site = 'http://www.shanbay.com'
        self.url_login = '/accounts/login/'
        self.api_get_word = '/api/word/%s'
        self.api_add_word = '/api/learning/add/%s'
        self.api_get_example = '/api/learning/examples/%s'
        self.api_get_user_info = '/api/user/info/'


def main():
    settings = Settings().settings

    print 'username:', settings.username
    print 'password:', settings.password
    print 'auto_play:', settings.auto_play
    print 'auto_add:', settings.auto_add
    print 'enable_en_definition:', settings.enable_en_definition
    print 'enable_example:', settings.enable_example
    print 'site:', settings.site
    print 'url_login:', settings.url_login
    print 'api_get_word:', settings.api_get_word
    print 'api_add_word:', settings.api_add_word
    print 'api_get_example:', settings.api_get_example
    print 'enable_iciba:', settings.enable_iciba
    print 'enable_icb_audio:', settings.enable_icb_audio
    print 'enable_icb_lang:', settings.enable_icb_lang
    print 'enable_icb_syllable:', settings.enable_icb_syllable
    print 'enable_icb_definition:', settings.enable_icb_definition
    print 'enable_icb_extra:', settings.enable_icb_extra

if __name__ == '__main__':
    main()
