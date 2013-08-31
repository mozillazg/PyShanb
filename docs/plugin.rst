插件
====


pyshanby 支持简单的插件功能。可以通过插件系统输出各类词典的解释。


插件开发
--------

首先，插件都比方放到 ``pyshanb/plugins/`` 目录下；

其次，插件模块中必须包含函数 ``output(word, colour='green')``,
其中 ``word`` 就是用户输入的单词 。

插件示例
````````

::

    # pyshanb/plugins/foo.py

    """这个插件实现了输出单词的功能。

    不管插件简单或复杂，跟这个都是差不多的，
    都有一个共同的特点，那就是都包含一个 output 函数，
    而且该函数的第一个参数是 word.
    """

    def output(word, colour='green'):
        print word

更进一步的可以参考插件目录下的 youdao.py.
