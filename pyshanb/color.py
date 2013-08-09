#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""给文字加点颜色."""

import os

if os.name == 'nt':
    from colorama import init
    init()
    win = True
else:
    win = False

colors = ['black', 'white', 'red', 'green', 'yellow', 'blue',
          'magenta', 'cyan', 'gray']
styles = ['bold', 'blink', 'underline', 'reverse', 'hidden']


def wrapper(code):
    """将颜色码转换为 ANSI escape code."""
    code = str(code)
    return '\033[{code}m'.format(**locals())


default = wrapper('0')
bold = wrapper('1')
underline = wrapper('4')
blink = wrapper('5')
reverse = wrapper('7')
hidden = wrapper('8')


# 前景色
fore_black = wrapper('30')
fore_red = wrapper('1;31')
fore_green = wrapper('1;32')
fore_yellow = wrapper('1;33')
fore_blue = wrapper('1;34')
fore_magenta = wrapper('1;35')
fore_cyan = wrapper('1;36')
fore_gray = wrapper('37')
fore_white = wrapper('1;37')
fore_default = wrapper('39')

# 背景色
back_black = wrapper('40')
back_red = wrapper('1;41')
back_green = wrapper('1;42')
back_yellow = wrapper('1;43')
back_blue = wrapper('1;44')
back_magenta = wrapper('1;45')
back_cyan = wrapper('1;46')
back_white = wrapper('47')
back_default = wrapper('49')


def color(text, foreground=None, background=None, extra=None):
    """给文字加点颜色.

    :param text: 要着色的文字.
    :param foreground: 前景色即文字颜色.
    :param background: 背景色.
    :param extra: 额外的效果.

    """
    foreg_color = ''
    backg_color = ''
    extra_styles = []
    if foreground:
        foreground = foreground.lower()
        if foreground in colors:
            foreg_color = globals()['fore_' + foreground]
    if background:
        background = background.lower()
        if background in colors:
            backg_color = globals()['back_' + background]
    if win:
        extra = False
    if extra:
        extras = [x.strip() for x in extra.split(',')]
        for x in extras:
            if x in styles:
                extra_styles.append(globals()[x])
    codes = foreg_color + backg_color + ''.join(extra_styles)
    return codes + text + default

