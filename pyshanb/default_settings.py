#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""默认配置信息
"""

# 扇贝网
# 自动播放发音
auto_play = False
# 自动添加到扇贝网
auto_add = False
# 询问是否添加到扇贝网
ask_add = True
# 启用英文释义
en_definition = False
# 获取例句
example = False
# 询问是否添加例句
ask_add_example = True

# 爱词霸
# 启用爱词霸信息
iciba = False
# 爱词霸发音
iciba_audio = True
# 声音标准(英音：'en-UK', 美音: 'en-US')
iciba_lang = 'en-US'
# 音标
iciba_syllable = True
# 解释
iciba_definition = True
# 同义词、反义词等
iciba_extra = True

# API
api_site = 'http://www.shanbay.com'
api_login = '/accounts/login/'
api_get_word = '/api/word/%s'
api_add_word = '/api/learning/add/%s'
api_get_example = '/api/learning/examples/%s'
api_get_user_info = '/api/user/info/'
api_add_example = '/api/example/add/%s?sentence=%s&translation=%s'
