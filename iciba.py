#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""获取爱词霸单词信息
"""

import urlparse
import copy
import re
import requests


class Lciba(object):
    """从爱词霸获取单词信息
    """
    def __init__(self, headers=None, mp3=False, extra=False):
        self.headers = headers
        self.mp3 = mp3
        self.extra = extra
        self.query_api = 'http://www.iciba.com/%s'

    def query(self, word, api=None):
        """查询单词，返回网页内容
        """
        query_api = api or self.query_api
        query_url = query_api % word
        query_headers = copy.deepcopy(self.headers)
        if self.headers:
            query_headers.update({
                'Host': urlparse.urlsplit(query_url).netloc,
            })

        query_r = requests.get(query_url, headers=query_headers,
                               prefetch=False)
        if query_r.status_code == requests.codes.ok:
            query_content = query_r.content
            self.content = query_content
            return self.content
        else:
            return None

    def get_data(self, word):
        """获取单词简明释义，get_word_data(self, word) -> datas

        返回值示例：
        (((u'词性', u'解释'),...), u'同义词之类的', u'mp3 url'))
        """
        datas = [None] * 3
        html = self.query(word)
        if not html:
            return None

        # 获取单词简明释义所在块
        re_pos = re.compile(ur"""(?ix)<strong\s+class="fl"[^>]*>([^<]+)</strong>
                         \s*(<span\s+class="label_list">\s*(?:<label>(?:[^<]+)
                         </label>\s*)+</span>)""")
        # 每个词性所对应的解释
        re_labels = re.compile(ur'(?i)<label>([^<]+)</label>')
        pos = re_pos.findall(html)
        if not pos:
            return None

        lsts = list()  # 存储全部单词释义
        for po in pos:
            lst = list()
            lst.append(po[0])  # 词性（名词，形容词等）
            labels = po[1]
            for label in re_labels.findall(labels):
                lst.append(label)  # 解释
            lsts.append(tuple(lst))
        datas[0] = tuple(lsts)

        if self.mp3:
            pass

        if self.extra_enable:
            pass

        return tuple(datas)

    def get_audio_url(self, content):
        """获取单词发音文件
        """
        pass

if __name__ == '__main__':
    iciba = Lciba()
    print iciba.get_data('word')
