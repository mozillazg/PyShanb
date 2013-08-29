#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""有道词典."""

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
        'User-Agent': (' Mozilla/5.0 (Windows NT 6.2; rv:23.0) Gecko'
                       + '/20100101 Firefox/23.0'),
    }
    try:
        response = requests.get('http://dict.youdao.com/search?q=%s'
                                % quote(word), headers=headers)
    except:
        return
    if not response.ok:
        return
    html = response.text
    soup = BeautifulSoup(html)

    # 找到中文解释所在块
    phrs_list = soup.find(id='phrsListTab')
    if not phrs_list:
        return
    # 解释
    trans = phrs_list.find_all(class_='trans-container')
    tran_lists = []
    addition_lists = []
    for tran in trans:
        # 基本解释
        uls = tran.find_all('ul')
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                tran_lists.append(li.get_text())
        # 附加信息：复数，过去式。。。
        additionals = tran.find_all(class_='additional')
        for info in additionals:
            addition_lists.append(info.get_text())
    return map(clean_text, tran_lists), map(clean_text, addition_lists)


def output(word, colour='green'):
    trans = search(word)
    if not trans:
        return
    word_color = color(word, colour, effect='underline')
    print '\n' + 'youdao.com- %s --begin'.center(40, '-') % word_color
    for tran in trans:
        print '\n'.join(tran)
    print 'youdao.com------end'.center(45, '-')


if __name__ == '__main__':
    output('hello')
