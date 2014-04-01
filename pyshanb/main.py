#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""命令行下的扇贝词典
"""

import sys
import urlparse
import copy
from urllib2 import quote
import tempfile
import os
import time
import textwrap

import requests

from shanbay import Shanbay, AuthException, ServerException
from .utils import parse_settings
from .color import color
from .plugin import plugins_output


def download_audio(url_audio, headers, host=None, cookies=None, referer=None):
    u"""下载音频文件.

    返回文件内容

    """
    headers_d = copy.deepcopy(headers)
    headers_d.update({
        'Host': host or urlparse.urlsplit(url_audio).netloc,
        'Referer': referer,
    })
    r_audio = requests.get(url_audio, headers=headers_d, cookies=cookies,
                           stream=True)
    if not r_audio.ok:
        return
    else:
        return r_audio.content


def check_error(func):
    u"""使用装饰器（decorator）处理异常."""
    def check(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AuthException:
            sys.exit(color('Login failed!', 'red', effect='underline'))
        except (requests.exceptions.RequestException, ServerException):
            sys.exit(color('Network trouble!', 'red', effect='underline'))
    return check


def encode(unicode_str, encoding=sys.stdout.encoding):
    return unicode_str.encode(encoding, 'ignore')


def decode(string, encoding=sys.stdin.encoding):
    return string.decode(encoding, 'ignore')


def output(msg):
    print textwrap.fill(encode(msg), 79)


@check_error
def main():
    if sys.version_info[0] == 3:
        sys.exit(color("Sorry, this program doesn't support Python 3 yet",
                       'red', effect='underline'))
    settings = parse_settings()
    colour = settings.colour

    if settings.iciba:
        from iciba import Lciba as iciba_
    if settings.auto_play and os.name == 'nt':
        try:
            import mp3play
        except ImportError:
            settings.auto_play = False
    else:
        settings.auto_play = False

    cmd_width = 55
    headers = {
        'Host': urlparse.urlsplit(settings.site).netloc,
        'User-Agent': (' Mozilla/5.0 (Windows NT 6.2; rv:23.0) Gecko'
                       + '/20100101 Firefox/28.0'),
    }

    # 登录
    output('Login...')
    s = Shanbay(settings.username, settings.password)
    s.login()
    shanbay = s.api
    user_info = shanbay.user_info()
    output('Welcome! %s.' % color(user_info.get('nickname'), colour))

    while True:
        word = quote(raw_input('Please input an english word: ').strip())
        if not word:
            continue

        # 输入 q 退出程序
        if word == 'q':
            output('Goodbye.')
            sys.exit(0)

        # 获取单词信息
        info = shanbay.query_word(word)
        if not info:
            output("%s may not be an english word!" % color(word, colour))
            continue

        # 输出单词信息
        # 学习记录
        learning_id = info.get('learning_id')
        voc = info.get('voc')
        if not voc:
            output("%s may not be an english word!" % color(word, colour))
            continue
        # 单词本身
        word = voc.get('content')
        # 音标
        # pron = voc.get('pron')
        # 音频文件
        audio_url = voc.get('audio')
        # 英文解释
        en_definitions = voc.get('en_definitions')
        if en_definitions:
            en_definition = ['%s. %s' % (p, ','.join(d))
                             for p, d in en_definitions.iteritems()]
        else:
            en_definition = None
        # 中文解释
        cn_definition = voc.get('definition')

        output(' %s '.center(cmd_width, '-') % color(word, colour,
                                                     effect='underline'))
        output('%s' % cn_definition.strip())

        if settings.en_definition and en_definition:
            output('\nEnglish definition:')
            for en in en_definition:
                output('%s' % en.strip())

        # iciba
        if settings.iciba:
            iciba = iciba_(headers=headers, audio=settings.iciba_audio,
                           lang=settings.iciba_lang,
                           syllable=settings.iciba_syllable,
                           extra=settings.iciba_extra)
            iciba_info = iciba.get_data(word)
            iciba_info = iciba_info if iciba_info else [None] * 4
            iciba_syllable, iciba_audio, iciba_def, iciba_extra = iciba_info

            if any(iciba_info):
                cmd_width_icb = 30
                output('\n' + 'iciba.com- %s --begin'.center(
                    cmd_width_icb, '-') % color(word, colour,
                                                effect='underline'))
                if iciba_syllable:
                    output(u'音节划分：%s' % iciba_syllable)
                if iciba_def:
                    output('-')
                    for x in iciba_def:
                        output('%s' % x)
                if iciba_extra:
                    output('-')
                    output(iciba_extra)
                if iciba_audio:
                    audio_url = iciba_audio
                output('iciba.com------end'.center(cmd_width_icb, '-'))

        try:
            if settings.auto_play:
                if iciba_audio:
                    referer = iciba.word_url
                else:
                    referer = None
                # 临时保存音频文件
                file_name = str(time.time()) + \
                    os.path.splitext(audio_url)[1] or '.mp3'
                temp_file = os.path.realpath(tempfile.gettempdir() + file_name)
                audio = download_audio(audio_url, headers, referer=referer)
                with open(temp_file, 'wb') as f:
                    f.write(audio)
                # 播放单词读音
                mp3 = mp3play.load(temp_file)
                mp3.play()
               # 移除临时文件
                os.remove(temp_file)
        except:
            pass

        # 插件
        plugins_output(settings.plugins, word)

        # 例句
        examples = []
        if settings.example and learning_id:
            examples_info = shanbay.examples(learning_id)
            if examples_info:
                examples_dict = examples_info.get('examples')
                for example_dict in examples_dict:
                    #examples.append('%(first)s*%(mid)s*%(last)s'
                                    #'\n%(translation)s' % example_dict)
                    examples.append(
                        example_dict['first'] +
                        color(example_dict['mid'], colour) +
                        '%(last)s\n%(translation)s' % example_dict
                    )

        if examples:
            output('\nExamples:')
            for ex in examples:
                output('%s' % ex.strip())

        # 如果未收藏该单词
        if not learning_id:
            if settings.ask_add:
                ask = raw_input('Do you want to add %s to shanbay.com?'
                                ' (y/n): ' % color(word, colour))
                if ask.strip().lower().startswith('y'):
                    # 收藏单词
                    learning_id_info = shanbay.add_word(word)
                    learning_id = learning_id_info.get('id')
                    output('%s has been added to shanbay.com' % color(word,
                                                                      colour))
            elif settings.auto_add:
                learning_id_info = shanbay.add_word(word)
                learning_id = learning_id_info.get('id')
                output('%s has been added to shanbay.com' % color(word,
                                                                  colour))

        # 添加例句
        if learning_id and settings.ask_example:
            ask = raw_input('Do you want to add an example for '
                            'this word? (y/n): ')
            if ask.strip().lower().startswith('y'):
                while True:  # 支持多次添加例句
                    _break = False  # 是否跳槽循环
                    sentence = None
                    translation = None

                    # 例句
                    while not sentence:
                        sentence = raw_input('Please input sentence:\n')
                        if sentence.strip().lower() == 'q':
                            sentence = None
                            _break = True
                            break
                    if _break:
                        break

                    if sentence:
                        # 解释
                        while not translation:
                            translation = raw_input('Please input '
                                                    'translation:\n')
                            if translation.strip().lower() == 'q':
                                translation = None
                                _break = True
                                break
                    if _break:
                        break

                    # 添加例句到扇贝网
                    if sentence and translation:
                        sentence = sentence.strip().decode(encoding)
                        translation = translation.strip().decode(encoding)
                        result = shanbay.add_example(learning_id, sentence, translation)
                        if result.get('example_status') == 1:
                            output('Add success')
        else:
            pass

        output('-' * cmd_width)

if __name__ == '__main__':
    main()
