安装使用
========

1. ``pip install pyshanb`` ；
2. 命令行下执行：\ ``shanbay -u username``\ （Tips：使用过程中输入 ``q``
   即可退出程序）。


命令行参数
----------

::

    >shanbay --hlep
    usage: shanbay-script.py [-h] [-V] [-s SETTINGS] [-u USERNAME] [-p PASSWORD]
                             [-e | -E] [-i | -I] [-a | -A]
                             [--color {black,white,red,green,yellow,blue,magenta,cyan,gray}]
                             [--plugin {youdao}]

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
