#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""http://www.vocabulary.com/dictionary/"""

from urllib import quote
import re

import requests
from bs4 import BeautifulSoup
from pyshanb.color import color


def clean_text(text):
    """清理文本.

    去掉首尾空格, 将多个空格合并为一个, 替换换行符为一个空格.

    """
    text = re.sub(r'(?<=\s)\s+', '', text.strip())
    return re.sub(r'\n', ' ', text)


def search(word):
    """解析搜索结果."""
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:26.0) Gecko/20100101'
                       'Firefox/26.0')
    }
    try:
        url = ('http://www.vocabulary.com/dictionary/definition.ajax?'
               'search=%s&lang=en')
        request = requests.Session()
        response = request.get(url % quote(word), headers=headers)
    except:
        return
    if not response.ok:
        return
    html = response.text
    soup = BeautifulSoup(html)

    # 找到解释所在块
    phrs_list = soup.select('.blurb p.short')
    if not phrs_list:
        return
    # 解释
    return phrs_list[0].text


def output(word, colour='green'):
    trans = search(word)
    if not trans:
        return
    word_color = color(word, colour, effect='underline')
    print '\n' + 'vocabulary.com- %s --begin'.center(40, '-') % word_color
    print trans
    print 'vocabulary.com------end'.center(45, '-')

if __name__ == '__main__':
    output('hello')
