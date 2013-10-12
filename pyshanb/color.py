#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""给文字加点颜色."""

import sys
reload(sys)
sys.setdefaultencoding(sys.stdout.encoding)

from .helper import windows

if windows:
    from colorama import init
    init()

COLORS = ('black', 'white', 'red', 'green', 'yellow', 'blue',
          'magenta', 'cyan', 'gray')
EFFECTS = ('bold', 'blink', 'underline', 'reverse', 'hidden')


def wrapper(code):
    """将颜色码转换为 ANSI escape code."""
    code = str(code)
    return '\033[{code}m'.format(**locals())

default = wrapper('0')    # 默认效果
bold = wrapper('1')       # 粗体
underline = wrapper('4')  # 下划线
blink = wrapper('5')      # 闪烁
reverse = wrapper('7')    # 调换前景色和背景色
hidden = wrapper('8')     # 隐藏

# 前景色
fore_black = wrapper('30')      # 黑色
fore_red = wrapper('1;31')      # 红色
fore_green = wrapper('1;32')    # 绿色
fore_yellow = wrapper('1;33')   # 黄色
fore_blue = wrapper('1;34')     # 蓝色
fore_magenta = wrapper('1;35')  # 品红/紫红
fore_cyan = wrapper('1;36')     # 青色/蓝绿
fore_gray = wrapper('37')       # 灰色
fore_white = wrapper('1;37')    # 白色
fore_default = wrapper('39')    # 默认色

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


def color(text, foreground=None, background=None, effect=None):
    """给文字加点颜色.

    :param text: 要着色的文字.
    :param foreground: 前景色即文字颜色.
    :param background: 背景色.
    :param effect: 额外的特效.

    """
    foreg_color = ''
    backg_color = ''
    extra_effects = []

    if foreground and foreground.lower() in COLORS:
        foreg_color = globals()['fore_' + foreground.lower()]
    if background and background.lower() in COLORS:
        backg_color = globals()['back_' + background.lower()]
    if effect:
        effects = [x.strip() for x in effect.lower().split(',')]
        for x in effects:
            if x in EFFECTS:
                # windows 下只支持 bold
                if windows and x != 'bold':
                    continue
                extra_effects.append(globals()[x])
    codes = foreg_color + backg_color + ''.join(extra_effects)
    return codes + text + default


if __name__ == '__main__':
    print color('hello')
    print color('hello', 'red')
    print color('hello', 'red', 'white')
    print color('hello', 'red', 'white', 'blink')
    print color('hello', 'red', 'white', 'bold')
