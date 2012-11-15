# PyShanb：命令行下的扇贝网查词工具

基于[扇贝网 API v0.8](http://www.shanbay.com/support/dev/api.html "扇贝网 API v0.8")开发的一个命令行下的查词工具。支持将生词添加到扇贝网的个人词库中。

![截图-默认功能](https://github.com/mozillazg/my-blog-file/raw/master/2012/11/pyshanb-01.png"截图-默认功能")

## 功能

* 自动登录扇贝网（需要配置用户名及密码）
* 显示单词中文释义
* 显示单词英文释义（可选，默认禁用）
* 自动发音（Windows only）（可选，默认禁用）
* 自动添加单词到扇贝网词库（当天待背单词列表）（可选，默认禁用）
* 询问是否添加单词到扇贝网词库（可选，默认启用）
* 显示例句（显示用户在扇贝网添加的例句）（可选，默认禁用）
* 配置文件（配置用户名、密码及其他功能项）

## 依赖

* [python 2.6 or 2.7](http://www.python.org/ "www.python.org")
* [requests](https://github.com/kennethreitz/requests "requests-github")
* [mp3play(windows only)](https://code.google.com/p/mp3play/ "mp3play-url")

## 安装使用

1. 安装依赖模块：`pip install -r requirements.txt`；
2. 配置用户名及密码（pyshanb.conf）；
3. 命令行下执行：`python pyshanb.py`（Tips：使用过程中输入 `q` 即可退出程序）。

## 截图

默认：       
![截图-默认功能](https://github.com/mozillazg/my-blog-file/raw/master/2012/11/pyshanb-01.png"截图-默认功能")

火力全开：      
![截图-功能全开](https://github.com/mozillazg/my-blog-file/raw/master/2012/11/pyshanb-02.png "截图-功能全开")
