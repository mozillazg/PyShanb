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
    def __init__(self, headers=None, audio=False, lang='en-US',
                 syllable=False, extra=False):
        self.headers = headers
        self.audio = audio
        self.lang = lang
        self.syllable = syllable
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

        返回值：
        (u'音节划分', u'audio url', ((u'词性', u'解释'),...), u'同义词之类的'))
        """
        datas = [None] * 4
        html = self.query(word)
        if not html:
            return None

        # 音节划分
        if self.syllable:
            datas[0] = self.get_syllable(html)

        if self.audio:
            datas[1] = self.get_audio(html)

        # 获取单词简明释义所在块
        re_pos = re.compile(ur"""(?ix)<strong\s+class="fl"[^>]*>([^<]+)
                            </strong>\s*(<span\s+class="label_list">\s*
                            (?:<label>(?:[^<]+)</label>\s*)+</span>)
                            """)
        pos = re_pos.findall(html)
        if not pos:
            return None

        # 单词简单释义
        lsts = []  # 存储全部单词释义
        # 每个词性所对应的解释
        re_labels = re.compile(ur'(?i)<label>([^<]+)</label>')
        for po in pos:
            lst = []
            lst.append(po[0])  # 词性（名词，形容词等）
            labels = po[1]
            for label in re_labels.findall(labels):
                lst.append(label)  # 解释
            lsts.append(''.join((lst)))
        datas[2] = tuple(lsts)

        # 同义词、反义词之类的
        if self.extra:
            datas[3] = self.get_extra(html)
        return tuple(datas)

    def get_syllable(self, html):
        """获取音节划分
        """
        re_sy = re.compile(ur'(?u)音节划分：([^<]*)')
        syllable = re_sy.findall(html)
        if syllable:
            return syllable[0].replace(u'▪', u'·')
        else:
            return None

    def get_audio(self, html):
        """获取单词发音文件
        """
        re_div = re.compile(ur'''(?ix)<div\s+class="prons"[^>]*>[\s\S]+?
                             <div\s+class="simple"[^>]*>''')
        div = re_div.findall(html)
        if not div:
            return None

        re_audio = re.compile(ur"asplay\('([^']+)'\)")
        audios = re_audio.findall(div[0])
        if not audios:
            return None
        if self.lang == 'en-UK':
            return audios[0]
        else:
            return audios[1]

    def get_extra(self, html):
        """获取同义词，复数等
        """
        re_div = re.compile(ur'''(?ix)<div\s+class="group_inf"[^>]*>\s*<ul>
                            [\s\S]+?</ul>\s*</div>''')
        div = re_div.findall(html)
        if not div:
            return None

        re_li = re.compile(ur'<li>(\S+)\s*<a\s*[^>]+>\W*(\w+)\W*</a>\s*</li>')
        lis = re_li.findall(div)
        if not lis:
            return None
        result = ''
        for a, b in lis:
            result += a + b
        return result

if __name__ == '__main__':
    iciba = Lciba()
    for i in iciba.get_data('word'):
        print i
