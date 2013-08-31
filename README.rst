PyShanb：命令行下的扇贝词典
===========================

|Build| |Pypi version| |Pypi downloads|

基于 `扇贝网 API v0.8 <http://www.shanbay.com/support/dev/api.html>`__
开发的一个命令行下的查词工具。

文档
----

`<http://pyshanb.readthedocs.org/>`__

功能
----

-  自动登录扇贝网（需要配置用户名及密码）;
-  显示单词中文释义;
-  显示单词英文释义（可选，默认禁用）;
-  自动发音（Windows only）（可选，默认禁用）;
-  自动添加单词到扇贝网词库（当天待背单词列表）（可选，默认禁用）;
-  询问是否添加单词到扇贝网词库（可选，默认启用）;
-  显示例句（显示用户在扇贝网添加的例句）（可选，默认禁用）;
-  配置文件（配置用户名、密码及其他功能项）;
-  从爱词霸网获取单词信息（可选，默认禁用）;
-  通过命令行参数指定配置文件、用户名及密码等;
-  登录后显示用户昵称;
-  添加单词例句（可选，默认启用）;
-  高亮单词及错误信息。
-  插件功能


安装使用
--------

1. ``pip install pyshanb`` ；
2. 命令行下执行：\ ``shanbay -u username``\ （Tips：使用过程中输入 ``q``
   即可退出程序）。


命令行参数
~~~~~~~~~~

::

    >shanbay --hlep
    usage: shanbay-script.py [-h] [-V] [-s SETTINGS] [-u USERNAME] [-p PASSWORD]
                             [-e | -E] [-i | -I] [-a | -A]
                             [--color {black,white,red,green,yellow,blue,magenta,cyan,gray}]
                             [--plugin {youdao}]
                             [--enable-example | --disable-example]

    An command line tool for shanbay.com.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -s SETTINGS, --settings SETTINGS
                            the settings file of the application
      -u USERNAME, --username USERNAME
                            the account username of shanbay.com
      -p PASSWORD, --password PASSWORD
                            the account password of shanbay.com
      -e                    enable "Add example" feature
      -E                    disable "Add example" feature
      -i                    enable "Get data from iciba.com" feature
      -I                    disable "Get data from iciba.com" feature
      -a                    enable "Auto play audio" feature
      -A                    disable "Auto play audio" feature
      --color {black,white,red,green,yellow,blue,magenta,cyan,gray}
                            colorize keyword (default: green)
      --plugin {youdao}     enable plugin
      --enable-example      enable examples
      --disable-example     disable examples

.. |Build| image:: https://api.travis-ci.org/mozillazg/PyShanb.png?branch=master
   :target: http://travis-ci.org/mozillazg/PyShanb
.. |Pypi version| image:: https://pypip.in/v/pyshanb/badge.png
   :target: https://crate.io/packages/pyshanb
.. |Pypi downloads| image:: https://pypip.in/d/pyshanb/badge.png
   :target: https://crate.io/packages/pyshanb


License
-------

Licensed under the `MIT License <http://en.wikipedia.org/wiki/MIT_License>`__.
