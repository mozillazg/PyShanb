# 命令行下的扇贝网查词工具

基于[扇贝网 API v0.8](http://www.shanbay.com/support/dev/api.html "扇贝网 API v0.8")

## 依赖

* [python 2.6 or 2.7](http://www.python.org/ "www.python.org")
* [requests](https://github.com/kennethreitz/requests "requests-github")
* [mp3play(windows only)](https://code.google.com/p/mp3play/ "mp3play-url")

## 功能

* 自动登录扇贝网
* 显示单词中文释义
* 显示单词英文释义（可选，默认关闭）
* 自动发音（Windows only）（可选，Windows 平台默认启用，非 Windows 平台默认关闭）
* 自动添加单词到扇贝网词库（当天待背单词列表）（可选，默认启用）
* 显示例句（显示用户在扇贝网添加的例句，可选，默认关闭）

## 已知问题

* 无法正常显示音标（默认不输出音标）
* 非 Windows 平台无法自动发音（打算改用 pygame 解决跨平台问题）

## TODO

* 修复已知问题
* 增加配置文件
* 增加命令行参数
* 获取用户昵称
* 长文本换行
* 获取爱词霸的单词释义
* 改用爱词霸的单词读音文件，因为扇贝网提供的读音文件缺少必需的文件头，无法被 pygame 所识别
* 转换 mp3 格式的读音文件为 ogg 格式
