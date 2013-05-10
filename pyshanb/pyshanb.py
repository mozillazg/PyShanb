#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""命令行下的扇贝词典
"""

import sys
import requests
import urlparse
import copy
from urllib2 import quote
import tempfile
import os
import time

from cmdoption import CmdOption
from conf import Settings
from shanbay import Shanbay
from shanbay import LoginException


def download_audio(url_audio, headers, host=None, cookies=None, refere=None):
    """下载音频文件
    返回文件内容
    """
    headers_d = copy.deepcopy(headers)
    headers_d.update({
        'Host': host or urlparse.urlsplit(url_audio).netloc,
        'Refere': refere,
    })
    r_audio = requests.get(url_audio, headers=headers_d, cookies=cookies,
                           stream=True)
    if r_audio.status_code != requests.codes.ok:
        # raise r_audio.raise_for_status()
        return None
    else:
        return r_audio.content


# 使用装饰器（decorator）处理异常
def check_error(func):
    def check(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LoginException:
            sys.exit(u'Login failed!')
        except requests.exceptions.RequestException:
            sys.exit(u"Network trouble!")
    return check


@check_error
def main():
    if sys.version_info[0] == 3:
        sys.exit(u"Sorry, this program doesn't support Python 3 yet")

    # 获取各命令行参数的值
    options = CmdOption().options
    configfile = options.settings
    username = options.username
    password = options.password
    ask_add_example = options.ask_add_example
    enable_iciba = options.enable_iciba
    auto_play = options.auto_play
    
    if configfile:
        configfile = os.path.realpath(configfile)

    conf = Settings(configfile, username, password).settings
    site = conf.site
    username = username or conf.username
    password = password or conf.password

    if auto_play is None:
        auto_play = conf.auto_play  # 自动播放单词读音
    if auto_play and os.name == 'nt':
        try:
            import mp3play
        except ImportError:
            auto_play = False
    else:
        auto_play = False

    # shanbay.com
    auto_add = conf.auto_add  # 自动保存单词到扇贝网
    ask_add = conf.ask_add  # 询问是否保存单词
    enable_en_definition = conf.enable_en_definition  # 单词英文释义
    enable_example = conf.enable_example  # 用户自己添加的单词例句
    
    if ask_add_example is None:
        ask_add_example = conf.ask_add_example  # 询问是否添加例句

    # iciba.com
    if enable_iciba is None:
        enable_iciba = conf.enable_iciba
    enable_icb_audio = conf.enable_icb_audio
    enable_icb_lang = conf.enable_icb_lang
    enable_icb_syllable = conf.enable_icb_syllable
    enable_icb_extra = conf.enable_icb_syllable
    if enable_iciba:
        from iciba import Lciba as iciba

    url_login = site + conf.url_login
    api_get_word = site + conf.api_get_word  # 获取单词信息的 api
    api_get_example = site + conf.api_get_example  # 获取例句的 api
    api_add_word = site + conf.api_add_word  # 保存单词的 api
    api_get_user_info = site + conf.api_get_user_info  # 获取用户信息的 api
    api_add_example = site + conf.api_add_example  # 添加例句的 api

    cmd_width = 55

    headers = {
        'Host': urlparse.urlsplit(site).netloc,
        'User-Agent': (' Mozilla/5.0 (Windows NT 6.2; rv:18.0) Gecko'
                       + '/20100101 Firefox/18.0'),
    }

    # 登录
    print 'Login...'
    shanbay = Shanbay(url_login, headers, username, password)
    user_info = shanbay.get_user_info(api_get_user_info)
    print u'Welcome! %s.' % user_info.get('nickname')

    while True:
        word = quote(raw_input(u'Please input a english word: ').strip())
        if not word:
            continue

        # 输入 q 退出程序
        if word == u'q':
            print u'Goodbye.'
            sys.exit(0)

        # 获取单词信息
        word_info = shanbay.get_word(api_get_word, word)
        if not word_info:
            print u"'%s' may not be a english word!" % word
            continue

        # 输出单词信息
        # 学习记录
        word_learning_id = word_info.get(u'learning_id')
        voc = word_info.get(u'voc')
        if not voc:
            print u"'%s' may not be an english word!" % word
            continue
        # 单词本身
        word_content = voc.get(u'content')
        # 音标
        # word_pron = voc.get(u'pron')
        # 音频文件
        word_audio = voc.get(u'audio')
        # 英文解释
        word_en_definitions = voc.get(u'en_definitions')
        if word_en_definitions:
            word_en_definition = [u'%s. %s' % (p, ','.join(d))
                                  for p, d in word_en_definitions.iteritems()]
        else:
            word_en_definition = None
        # 中文解释
        word_definition = voc.get(u'definition')

        # print u'%s [%s]' % (word_content, word_pron)
        print ' %s '.center(cmd_width, '-') % word_content
        print u'%s' % (word_definition)

        if enable_en_definition and word_en_definition:
            print u'\nEnglish definition:'
            for en in word_en_definition:
                print u'%s' % (en)

        # iciba
        if enable_iciba:
            icb = iciba(headers=headers, audio=enable_icb_audio,
                        lang=enable_icb_lang, syllable=enable_icb_syllable,
                        extra=enable_icb_extra)
            info = icb.get_data(word)
            info = info if info else [None] * 4
            iciba_syllable, iciba_audio, iciba_def, iciba_extra = info

            if any(info):
                cmd_width_icb = 21
                print u'iciba.com-begin'.center(cmd_width_icb, '-')
                if iciba_syllable:
                    print u'音节划分：%s' % iciba_syllable
                if iciba_def:
                    # print iciba_def
                    print '-'
                    for x in iciba_def:
                        print '%s' % x
                if iciba_extra:
                    print '-'
                    print iciba_extra
                if iciba_audio:
                    word_audio = iciba_audio
                print u'iciba.com-end'.center(cmd_width_icb, '-')

        try:
            if auto_play and os.name == 'nt':
                if iciba_audio:
                    refere = icb.word_url
                else:
                    refere = None
                # 临时保存音频文件
                file_name = (str(time.time()) +
                             os.path.splitext(word_audio)[1] or '.mp3')
                temp_file = os.path.realpath(tempfile.gettempdir() +
                                             file_name)
                # print temp_file
                audio = download_audio(word_audio, headers, refere=refere)
                with open(temp_file, 'wb') as f:
                    f.write(audio)
                # 播放单词读音
                mp3 = mp3play.load(temp_file)
                mp3.play()
               # 移除临时文件
                os.remove(temp_file)
                # print os.path.exists(temp_file)
        except:
            pass

        # 例句
        word_examples = []
        if enable_example and word_learning_id != 0:
            word_example = shanbay.get_example(api_get_example,
                                               word_learning_id)
            if word_example:
                examples = word_example.get(u'examples')
                for example in examples:
                    word_examples.append('%(first)s*%(mid)s*%(last)s' % example
                                         + '\n%(translation)s' % example)

        if enable_example and word_examples:
            print u'\nExamples:'
            for ex in word_examples:
                print u'%s' % (ex)

        if auto_add or ask_add:
            # 如果未收藏该单词
            if not word_learning_id:
                if ask_add:
                    ask = raw_input('Do you want to add ' +
                                    '"%s" to shanbay.com? (y/n): '
                                    % word_content).strip().lower()
                    if ask.startswith('y'):
                        # 收藏单词
                        word_learning_id = shanbay.add_word(api_add_word, word)
                        word_learning_id = word_learning_id.get('id')
                        print '"%s" has been added to shanbay.com'\
                              % word_content
                else:
                    word_learning_id = shanbay.add_word(api_add_word, word)
                    word_learning_id = word_learning_id.get('id')
                    print '"%s" has been added to shanbay.com' % word_content

        # 添加例句
        if word_learning_id and ask_add_example:
            ask = raw_input('Do you want to add a example for '
                            'this word? (y/n): ')
            if ask.strip().lower().startswith('y'):
                sentence = None
                translation = None

                while not sentence:
                    sentence = raw_input('Please input sentence:\n')
                    if sentence.strip(' \n').lower() == 'q':
                        sentence = None
                        break
                if sentence:
                    while not translation:
                        translation = raw_input('Please input translation:\n')
                        if translation.strip(' \n').lower() == 'q':
                            translation = None
                            break
                if sentence and translation:
                    sentence = sentence.strip(' \n')
                    translation = translation.strip(' \n')
                    encoding = sys.stdin.encoding
                    translation = translation.decode(encoding).encode('utf8')

                    result = shanbay.add_example(api_add_example,
                                                 word_learning_id,
                                                 quote(sentence),
                                                 quote(translation))
                    if result.get('example_status') == 1:
                        print 'Add success'
        else:
            pass

        print '-' * cmd_width

if __name__ == '__main__':
    main()
