#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""获取爱词霸单词信息
"""

import urlparse
import re
import requests


class Lciba(object):
    """从爱词霸获取单词信息
    """
    def __init__(self, headers):
        self.headers = headers
        self.word = word
        self.api_query = 'http://www.iciba.com/%s'
        self.content = None

    def query_word(self, word, api=None):
        """查询单词，返回网页内容
        """
        api_query = api or self.api_query
        url_query = api_query % word
        headers_q = copy.deepcopy(self.headers)
        headers_q.update({
            'Host': urlparse.urlsplit(url_query).netloc,
        })
        r_query = requests.get(url_query, headers=headers_q, prefetch=False)
        if r_query.status_code == requests.codes.ok:
            content_query = r_query.content
            self.content = r_query.content

    def get_word_date(self, word, headers):
        """获取单词简明释义
        """
        pass

    def get_audio_url(self, content):
        """
        """
        pass
