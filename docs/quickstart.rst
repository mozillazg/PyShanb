安装使用
========

Windows
-------

1. 下载 `shanbay.0.6.2.exe.zip <http://pan.baidu.com/s/1zMRKK>`__ ;
2. 命令行下执行：\ ``shanbay.0.6.2.exe -u username -p password``


其他平台/开发者
---------------

1. ``pip install pyshanb`` ；
2. 命令行下执行：\ ``shanbay -u username -p password``\ （Tips：使用过程中输入 ``q``
   即可退出程序）。


命令行参数
----------

::

    >shanbay --hlep
    usage: shanbay.py [-h] [-V] [-s SETTINGS] [-u USERNAME] [-p PASSWORD]
                      [-e | -E] [-i | -I] [-a | -A]
                      [--color {black,white,red,green,yellow,blue,magenta,cyan,gray}]
                      [--plugin {youdao}] [--example | --disable-example]
                      [--english | --disable-english]

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
      -e, --add-example     enable "Add example" feature
      -E, --disable-add-example
                            disable "Add example" feature
      -i, --iciba           enable "Get data from iciba.com" feature
      -I, --disable-iciba   disable "Get data from iciba.com" feature
      -a, --auto-play       enable "Auto play audio" feature
      -A, --disable-auto-play
                            disable "Auto play audio" feature
      --color {black,white,red,green,yellow,blue,magenta,cyan,gray}
                            colorize keyword (default: green)
      --plugin {youdao}     enable plugin
      --example, --enable-example
                            enable examples
      --disable-example     disable examples
      --english             enable english definition
      --disable-english     disable english definition
