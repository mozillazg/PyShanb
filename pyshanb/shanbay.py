#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import copy


class LoginException(Exception):
    """登录异常
    """
    pass


class Shanbay(object):
    def __init__(self, url_login, headers, username, password):
        self.cookies = self.login(url_login, headers, username, password)
        self.headers = headers

    def login(self, url_login, headers, username, password):
        """登录扇贝网
        返回 cookies
        """
        # 首先访问一次网站，获取 cookies
        r_first_vist = requests.get(url_login, headers=headers,
                                    stream=True)
        # 判断 HTTP 状态码是否是 200
        if r_first_vist.status_code != requests.codes.ok:
            raise LoginException
        # 获取 cookies 信息
        cookies_first_vist = r_first_vist.cookies.get_dict()

        # 准备用于登录的信息
        url_post = url_login
        # 获取用于防 csrf 攻击的 cookies
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
            'csrfmiddlewaretoken': token,  # csrf
            'username': username,  # 用户名
            'password': password,  # 密码
            'login': '',
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
            raise LoginException

    def get_word(self, api, word):
        """获取单词信息
        """
        ur_get = api % word
        r_get = requests.get(ur_get, headers=self.headers,
                             cookies=self.cookies, stream=True)
        if r_get.status_code != requests.codes.ok:
            return None

        # 更新 cookies
        self.cookies.update(r_get.cookies.get_dict())
        return r_get.json()

    def add_word(self, api, word):
        """收藏单词
        """
        url_add = api % word
        r_add = requests.get(url_add, headers=self.headers,
                             cookies=self.cookies, stream=True)
        if r_add.status_code != requests.codes.ok:
            return None

        self.cookies.update(r_add.cookies.get_dict())
        return r_add.json()

    def get_example(self, api, learning_id):
        """获取用户在扇贝网添加的例句
        """
        url_example = api % str(learning_id)
        r_example = requests.get(url_example, headers=self.headers,
                                 cookies=self.cookies, stream=True)
        if r_example.status_code != requests.codes.ok:
            return None

        example_json = r_example.json()
        # 判断是否包含例句信息
        if not example_json.get('examples_status'):
            return None

        self.cookies.update(r_example.cookies.get_dict())
        return example_json

    def get_user_info(self, api):
        """获取用户信息
        """
        r_user = requests.get(api, headers=self.headers,
                              cookies=self.cookies, stream=True)
        if r_user.status_code != requests.codes.ok:
            return None

        user_json = r_user.json()
        # 判断是否包含例句信息
        if not user_json.get('result'):
            return None

        self.cookies.update(r_user.cookies.get_dict())
        return user_json
