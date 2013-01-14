#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""在命令行下使用扇贝网查询单词
"""

import sys
import requests
import urlparse
import copy


def login(url_login, headers, username, password):
    """登录扇贝网
    返回 cookies
    """
    # 首先访问一次网站，获取 cookies
    r_first_vist = requests.get(url_login, headers=headers,
                                stream=True)
    # 判断 HTTP 状态码是否是 200
    if r_first_vist.status_code != requests.codes.ok:
        return None
    # 获取 cookies 信息
    cookies_first_vist = r_first_vist.cookies.get_dict()

    # 准备用于登录的信息
    url_post = url_login
    # 获取用于用户标识的 cookies（身份令牌）
    token = cookies_first_vist.get('csrftoken')
    # 设置 headers
    headers_post = copy.deepcopy(headers)
    headers_post.update({
        'Refere': url_login,
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    cookies_post = cookies_first_vist
    # post 提交的内容
    data_post = {
        'csrfmiddlewaretoken': token,  # 唯一标识
        'username': username,  # 用户名
        'password': password,  # 密码
        'login': '登录',
        'continue': 'home',
        'u': 1,
        'next': '',
    }

    # 提交登录表单同时提交第一次访问网站时生成的 cookies
    r_login = requests.post(url_post, headers=headers_post,
                            cookies=cookies_post, data=data_post,
                            allow_redirects=False, stream=True)
    # print r_login.url
    if r_login.status_code == requests.codes.found:
        # 返回登录成功后生成的 cookies
        return r_login.cookies.get_dict()
    else:
        return None


def get_word(api, headers, cookies, word):
    """获取单词信息
    """
    ur_get = api % (word)
    r_get = requests.get(ur_get, headers=headers,
                         cookies=cookies, stream=True)
    if r_get.status_code != requests.codes.ok:
        return None

    new_cookies = r_get.cookies.get_dict()
    # 如果网站 cookies 信息发生了变化，更新 cookies
    if new_cookies:
        cookies.update(new_cookies)
    return r_get.json()


def add_word(api, headers, cookies, word):
    """收藏单词
    """
    url_add = api % (word)
    r_add = requests.get(url_add, headers=headers, cookies=cookies,
                         stream=True)
    if r_add.status_code != requests.codes.ok:
        return None

    new_cookies = r_add.cookies.get_dict()
    if new_cookies:
        cookies.update(new_cookies)
    return r_add.json()


def get_example(api, headers, cookies, learning_id):
    """获取用户在扇贝网添加的例句
    """
    url_example = api % (str(learning_id))
    r_example = requests.get(url_example, headers=headers,
                             cookies=cookies, stream=True)
    if r_example.status_code != requests.codes.ok:
        return None

    example_json = r_example.json()
    # 判断是否包含例句信息
    if example_json.get('examples_status') != 1:
        return None

    new_cookies = r_example.cookies.get_dict()
    if new_cookies:
        cookies.update(new_cookies)
    return example_json()


def download_audio(url_audio, headers, cookies=None, refere=None):
    """下载音频文件
    返回文件内容
    """
    headers_d = copy.deepcopy(headers)
    headers_d.update({
        'Host': urlparse.urlsplit(url_audio).netloc,
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
        except requests.exceptions.RequestException:
            sys.exit(u"Network trouble!")
    return check


@check_error
def main():
    import sys

    if sys.version_info[0] == 3:
        sys.exit(u"Sorry, this program doesn't support Python 3 yet")

    from urllib2 import quote
    import tempfile
    import os
    import time
    import conf

    site = conf.site
    username = conf.username
    password = conf.password
    auto_play = conf.auto_play  # 自动播放单词读音
    if auto_play and os.name == 'nt':
        import mp3play

    auto_add = conf.auto_add  # 自动保存单词到扇贝网
    ask_add = conf.ask_add  # 询问是否保存单词
    enable_en_definition = conf.enable_en_definition  # 单词英文释义
    enable_example = conf.enable_example  # 用户自己添加的单词例句

    # iciba
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

    cmd_width = 55

    headers = {
        'Host': urlparse.urlsplit(site).netloc,
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko'
                       + '/20100101 Firefox/15.0.1'),
    }

    # 登录
    print 'Login...'
    cookies = login(url_login, headers, username, password)
    if not cookies:
        sys.exit(u'Login failed!')

    while True:
        word = quote(raw_input(u'Please input a english word: ').strip())
        if not word:
            continue

        # 输入 q 退出程序
        if word == u'q':
            print u'Goodbye.'
            sys.exit(0)

        # 获取单词信息
        result_get = get_word(api_get_word, headers, cookies, word)
        if not result_get:
            continue

        # 输出单词信息
        # 学习记录
        word_leaning_id = result_get[u'learning_id']
        voc = result_get.get(u'voc')
        if not voc:
            print u"'%s' may not be a english word!" % word
            continue
        # 单词本身
        word_content = voc.get(u'content')
        # 音标
        # word_pron = voc.get(u'pron')
        # 音频文件
        word_audio = voc.get(u'audio')
        # 英文解释
        word_en_definition = [u'%s. %s' % (p, ','.join(d))
                              for p, d in voc.get(u'en_definitions'
                                                  ).iteritems()]
        # 中文解释
        word_definition = voc.get(u'definition')

        # print u'%s [%s]' % (word_content, word_pron)
        print u'%s' % (word_content)
        print u'-' * cmd_width
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

            print u'----iciba.com----'
            if iciba_syllable:
                print u'音节划分：%s' % iciba_syllable
            if iciba_def:
                # print iciba_def
                for x in iciba_def:
                    print '-'
                    print '%s' % x
            if iciba_extra:
                print '-'
                print iciba_extra
            if iciba_audio:
                word_audio = iciba_audio
            print u'----iciba.com----'

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
                audio = download_audio(word_audio,headers, cookies,
                                       refere=refere)
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
        if enable_example and word_leaning_id != 0:
            word_example = get_example(api_get_example, headers,
                                       cookies, word_leaning_id)
            if word_example:
                examples = word_example.get(u'examples')
                for example in examples:
                    word_examples.append('%(first)s*%(mid)s*%(last)s'
                                         % (example) +
                                         '\n%(translation)s' % (example))
        if enable_example and word_examples:
            print u'\nExamples:'
            for ex in word_examples:
                print u'%s' % (ex)

        if auto_add or ask_add:
            # 如果未收藏该单词
            if word_leaning_id == 0:
                if ask_add:
                    ask = raw_input('Do you want add ' +
                                    '"%s" to shanbay.com? (y/n): '
                                    % (word_content)).strip().lower()
                    if ask.startswith('y'):
                        # 收藏单词
                        word_leaning_id = add_word(api_add_word,
                                                   headers, cookies,
                                                   word)[u'id']
                else:
                    word_leaning_id = add_word(api_add_word,
                                               headers, cookies,
                                               word)[u'id']

        print u'-' * cmd_width

if __name__ == '__main__':
    main()
