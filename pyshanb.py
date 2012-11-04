#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""在命令行下使用扇贝网查询单词
"""

import requests
import urlparse
import copy


def login(url_login, headers, username, password):
    """登录扇贝网
    返回 cookies
    """
    # 首先访问一次网站，获取 cookies
    r_first_vist = requests.get(url_login, headers=headers,
                                prefetch=False,)
    if r_first_vist.status_code != requests.codes.ok:
        return None
    cookies_first_vist = r_first_vist.cookies.get_dict()
    url_post = url_login
    # 获取用于用户标识的 cookies
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
    # 提交登录表单并提交第一次访问网站时生成的 cookies
    r_login = requests.post(url_post, headers=headers_post,
                            cookies=cookies_post,
                            data=data_post, prefetch=False)
    # print r_login.url
    if r_login.status_code == requests.codes.ok:
        # 返回登录成功后生成的 cookies
        return r_login.cookies.get_dict()
    else:
        return None


def get_word(api, headers, cookies, word):
    """获取单词信息
    """
    ur_get = api + word
    r_get = requests.get(ur_get, headers=headers,
                         cookies=cookies, prefetch=False)
    if r_get.status_code != requests.codes.ok:
        return None
    new_cookies = r_get.cookies.get_dict()
    # 如果网站 cookies 信息发生了变化，更新 cookies
    if new_cookies:
        cookies.update(new_cookies)
    return r_get.json


def add_word(api, headers, cookies, word):
    """收藏单词
    """
    url_add = api + word
    r_add = requests.get(url_add, headers=headers, cookies=cookies,
                         prefetch=False)
    if r_add.status_code != requests.codes.ok:
        return None
    new_cookies = r_add.cookies.get_dict()
    if new_cookies:
        cookies.update(new_cookies)
    return r_add.json


def get_example(api, headers, cookies, learning_id):
    url_example = api + str(learning_id)
    r_example = requests.get(url_example, headers=headers,
                             cookies=cookies, prefetch=False)
    if r_example.status_code != requests.codes.ok:
        return None
    example_json = r_example.json
    if example_json.get('examples_status') != 1:
        return None
    new_cookies = r_example.cookies.get_dict()
    if new_cookies:
        cookies.update(new_cookies)
    return example_json


def download_audio(url_audio, headers, cookies):
    """下载音频文件
    返回文件内容
    """
    d_headers = copy.deepcopy(headers)
    d_headers.update({
        'Host': 'media.shanbay.com',
    })
    r_audio = requests.get(url_audio, headers=d_headers, cookies=cookies,
                           prefetch=False)
    if r_audio.status_code != requests.codes.ok:
        # raise r_audio.raise_for_status()
        return None
    else:
        return r_audio.content


def main():
    """docstring for main"""
    from urllib2 import quote
    import tempfile
    import os
    import time

    if os.name == 'nt':
        import mp3play
    # else:
        # raise Exception("Sorry, this program can't run on your\
                        # operating system.")
    site = 'http://www.shanbay.com'
    headers = {
        'Host': urlparse.urlsplit(site).netloc,
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko'
                       + '/20100101 Firefox/15.0.1'),
    }
    username = 'username'
    password = 'password'
    auto_play = True
    auto_add = True
    enable_en_definition = False
    enable_example = False
    url_login = site + '/accounts/login/'
    api_get_word = site + '/api/word/'
    api_get_example = site + '/api/learning/examples/'
    api_add_word = site + '/api/learning/add/'
    # 登录
    cookies = login(url_login, headers, username, password)
    if cookies:
        while True:
            word = quote(raw_input('please input the word: ').strip())
            if not word:
                continue
            # 获取单词信息
            result_get = get_word(api_get_word, headers, cookies, word)
            if result_get:
                # 输出单词信息
                # 学习记录
                word_leaning_id = result_get[u'learning_id']
                voc = result_get.get(u'voc')
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
                word_examples = list()
                if auto_add:
                    # 如果未收藏该单词
                    if word_leaning_id == 0:
                        # 收藏单词
                        word_leaning_id = add_word(api_add_word, headers,
                                                   cookies, word)[u'id']
                # 例句
                if enable_example and word_leaning_id != 0:
                    word_example = get_example(api_get_example, headers,
                                               cookies, word_leaning_id)
                    if word_example:
                        examples = word_example.get(u'examples')
                        for example in examples:
                            word_examples.append('%(first)s_%(mid)s_%(last)s\n\
                                                 %(translation)s' %
                                                 (example))
                print '-' * 50
                # print u'%s [%s]' % (word_content, word_pron)
                print u'%s' % (word_content)
                print u'%s' % (word_definition)
                if enable_en_definition and word_en_definition:
                    for en in word_en_definition:
                        print u'%s' % (en)
                if enable_example and word_examples:
                    for ex in word_examples:
                        print u'%s' % (ex)
                if auto_play and os.name == 'nt':
                    # 临时保存音频文件
                    file_name = (str(time.time()) +
                                 os.path.splitext(word_audio)[1] or '.mp3')
                    temp_file = os.path.realpath(tempfile.gettempdir() +
                                                 file_name)
                    # print temp_file
                    audio = download_audio(word_audio, headers, cookies)
                    with open(temp_file, 'wb') as f:
                        f.write(audio)
                    # 播放单词读音
                    mp3 = mp3play.load(temp_file)
                    mp3.play()
                   # 移除临时文件
                    os.remove(temp_file)
                    # print os.path.exists(temp_file)
                print '-' * 50
    else:
        print 'Login failed'

if __name__ == '__main__':
    main()
