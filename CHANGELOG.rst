PyShanb Changelog
=================


0.6.1 (2013-xx-yy)
------------------

-- 修复 0.6 忘了添加 html5lib 依赖；
-- 添加 ``[--enable-example | --disable-example]`` 命令行选项控制是否输出单词例句。


0.6 (2013-08-29)
----------------

-  将配置文件保存到用户的家目录下；
-  添加文档;
-  改进命令行选项与配置文件共存的问题；
-  支持插件功能，目前有一个有道词典插件；
-  --plugin 选项控制启用哪些插件。

   ::

      --plugin {youdao}     enable plugin


0.5.5 (2013-08-14)
------------------

-  新生成的配置文件将不再包含命令行输入的密码信息；
-  高亮单词及错误信息；
-  添加 --color 选项控制高亮颜色。

   ::

       --color COLOR         colorize keyword (default: green). COLOR may be
                             "black", "white", "red", "green", "yellow", "blue",
                             "magenta", "cyan", or "gray"


0.5.4 (2013-07-28)
------------------

-  支持添加多个例句（输入 q 即可退出）。


0.5.3 (2013-07-09)
------------------

-  支持如下命令行参数形式；

   ::

       $ shanbay -uroot
       Please input password:
       Login...

-  使用 argparse 代替 optparse 处理命令行参数；
-  修复 --version 输出的版本信息有问题的 bug ，--help 添加描述信息。


0.5.2 (2013-05-21)
------------------

-  发布到 PyPI。


0.5.1 (2013-03-16)
------------------

-  新增加几个命令行参数（[-i \| -I][-a \| -A]）。

   ::

       -i                    enable "Get data from iciba.com" feature
       -I                    disable "Get data from iciba.com" feature
       -a                    enable "Auto play audio" feature
       -A                    disable "Auto play audio" feature


0.5 (2013-03-04)
----------------

-  现在可以为单词添加例句了（默认启用），可以通过配置文件或命令行参数
   ``-E`` 禁用该功能。

   ::

       -e                    enable "Add example" feature
       -E                    disable "Add example" feature


0.4 (2013-02-10)
----------------

-  增加命令行参数；

   ::

       -s SETTINGS, --settings SETTINGS
                             the settings file of the application
       -u USERNAME, --username USERNAME
                             the account username of shanbay.com
       -p PASSWORD, --password PASSWORD
                             the account password of shanbay.com


-  获取用户昵称。

0.3 (2013-01-14)
----------------

-  适应新版 requests(1.x) 和 shanbay.com. thanks @hongyuan19 。


0.2 (2012-12-04)
----------------

-  现在能够同时获取 `爱词霸 <http://www.iciba.com>`__ 的单词信息了（可选，默认禁用）。

   -  音节划分；
   -  读音；
   -  解释；
   -  过去分词、现在分词之类的其他信息；


0.1 (2012-11-15)
----------------

-  First version.

   -  自动登录扇贝网（需要配置用户名及密码）；
   -  显示单词中文释义；
   -  显示单词英文释义（可选，默认禁用）；
   -  自动发音（Windows only）（可选，默认禁用）；
   -  询问是否添加单词到扇贝网词库（可选，默认启用）；
   -  显示例句（显示用户在扇贝网添加的例句）（可选，默认禁用）；
   -  配置文件（配置用户名、密码及其他功能项）。

