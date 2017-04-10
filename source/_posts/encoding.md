---
title: 编码总结
date: 2016-10-04 09:47:42
categories: 砍树人
tags: [encode,python,unicode,utf-8]
photos:
- http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-09%20at%209.46.29%20AM.png

---
这篇很长！！！先看一下目录。

更新：
- python脚本文件的编码
- 添加vim编码的链接

<!-- more -->

# 问题的根源
因为计算机是二进制的，为了能在计算机上显示字符，又因为是电脑是美国人发明的，他们定义了字符表（ascii码表），也就是字符和数字的对应，比如在ascii码表中`65`表示`A`，这样就有一对一的映射关系，字符就能用数字表示了，那样计算机也就算懂得“文字”了。而ascii码表是用到了0~127这样一个范围，`0*** ****` 7位二进制，但是电脑普及之后，其他国家也想在电脑上显示自己的文字，因为一个字节是8位么，有些可以把8位中的最高位利用起来，定义一些其他字符，然后兼容ascii码，但是有些国家像中国，8位是远远不够的，所以就有了像gbk,gb2312这样的自己定义的一组字符编码表。后来国际上统一制定了一个叫unicode的字符编码表，能够包含**所有**国家的文字

那unicode到底是什么？
这里其实有好几个不同的概念

# 不要混淆概念

- 字符集(Abstract character repertoire)
- 编码字符集(Coded character set)
- 字符编码方式 (Character encoding form)
- 字符编码方案 (Character encoding scheme)

## 字符集
第一层，可以看作是抽象层，我就是我们人类的视角，看到的我们的语言的文字集合
> 不同文字系统在记录信息上的能力是等价的。进一步讲，文字只是信息的载体，而非信息本身。不用文字，用其他的载体（数字）也可以存储同样意义的信息。
> 吴军《数学之美》

## 编码字符集
就是给抽象的字符编上数字，可以看作逻辑层。
> 如gb2312中的定义的字符，每个字符都有个整数和它对应。一个整数只对应-着一个字符。反过来，则不一定是
这个说法有点模糊，反过来不一定是，是说在这个gb2312定义的字符中，一个字符能有多个整数对应，一个整数只对应一个字符的意思吗？一对多的关系？如果是这样，那没有意义啊，如果是因为在不同编码方式下，比如,这里只是假设打比方啊，在`a`编码表中，`"中"`对应`52`,在`b`编码中`"中"`对应`77`,这样说一个字符对应不同的整数还说的通，但是这样`77`在`a`中就能对应其他字符了，与一个整数只对应着一个字符在这个条件下也就矛盾了。所以我不知道这句话说的到底是什么意思

但只需要知道这里所说的映射关系，**是数学意义上的映射关系，编码字符集是与计算机无关的**,`unicode`就在这一层

## 字符编码方式
记得组原里面的逻辑结构和存储结构的概念，这里的字符编码方式就对应着存储结构的这个概念，它是与计算机有关的
> 通俗的说，意思就是怎么样才能将字符所对应的整数的放进计算机内存，或文件、或网络中。于是，不同人有不同的实现方式，所谓的万码奔腾，就是指这个。gb2312，utf-8,utf-16,utf-32等都在这一层。

这里就有问题了，既然像unicode已经定义了文字对数字的对应了，那直接就那样存就行了？
too young, too simple， 不是那么简单。要考虑到存储空间，提一下，因为会有很多零，考虑到这些，所以逻辑形式和存储形式会不一样。下面详解

## 字符编码方案
> 这个更加与计算机密切相关。具体是与操作系统密切相关。主要是解决大小字节序的问题。对于UTF-16和UTF-32编码，Unicode都支持big-endian 和 little-endian两种编码方案。一般来说，我们所说的编码，都在第三层完成（字符编码方式）。具体到一个软件系统中，则很复杂。浏览器－apache－tomcat（包括tomcat内部的jsp编码、编译，文件读取）－数据库之间，只要存在数据交互，就有可能发生编码不一致，如果在读取数据时，没有正确的decode和encode，出现乱码就是家常便饭了。

我理解就是这一层就是考虑大端还是小端存储，这是和**不同计算机**具体设计所不同的。

# unicode
刚说了unicode是在第二层，只是理论上的，什么叫只是理论上的，它是理想的，他定义了字符与一个数字的关系，仅仅而此。他没有定义编码在电脑中的具体存储形式。
比如 `中` 对应是`4E2D 0100 1110 0010 1101`  它不就这样存着就好了么？ 不是这样的。
看`A` 是`41`,`0000 0000 0100 0001` 如果都按照这样直接存着，有一个问题就是太浪费资源了，8位还好，16位的话，有那么多个0，存储空间都浪费了，而且传输的时候也浪费不必要的带宽，所以这是理论上编码和具体实现的差别。在实际存储到计算机上要考虑其他因素，正是有这些因素，导致了`utf-8`，`utf-16`,`utf-32`等，基于`unicode`的编码方式。

**但有些编码不只是定义了影射关系，除了有字符集同时也包含了字符编码的含义，__也就是这样定义的也是这样存的__。如ASCII,GBK,GB2312等**， unicode 只是定义了编码。没有定义怎么具体实现。

unicode 作为字符集(usc)是唯一的，编码方案(utf)才是有很多种。

也就是怎么存储，比如`中`，用的最多的是utf-8

## utf-8
![utf-8](http://onexs3cnv.bkt.clouddn.com/utf8.png)

具体`utf-8`是怎么和`unicode`对应不是这里的讨论重点，终点是`unicode`和`utf-8`的关系，`unicode`是理想的，虚浮的，`utf-8`才是真实的显示的。`unicode`是一个`code point`，他还是需要被表示成一个一个binary,这就需要encode.

> In Unicode, a letter maps to something called a code point which is still just a theoretical concept. How that code point is represented in memory or on disk is a whole nuther story.


## 例子
![转化的例子](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-09%20at%209.46.29%20AM.png)
```python
>>> import sys
>>> sys.stdin.encoding
'UTF-8'
>>> c = '中文'
>>> c
'\xe4\xb8\xad\xe6\x96\x87'
>>> cu = c.decode('utf-8')
>>> cu
u'\u4e2d\u6587'
>>> cu.encode('gbk')
'\xd6\xd0\xce\xc4'
```
> It does not make sense to have a string without knowing what encoding it uses.

这句话很重要。这里就先知道`c`这个字符串是由`utf-8`编码的。也就是计算机里面存的就是`\xe4\xb8\xad\xe6\x96\x87`对应的二进制。其实编码可以看作一个给`unicode`加密的过程,解码就是从字符串到`unicode`解密的过程。其实最终在计算机里只是一些`010101010`这样的数字，关键就是看你怎么看待它，怎么去翻译它的问题，翻译不正确就没有意义。

`c` 是由`utf-8`来编码的，解码之后`unicode` code point 是`4e2d 6587`, 代表`'中文'`，再对它进行`gbk`编码，它则变成了`'\xd6\xd0\xce\xc4'`, 所以字符集在不同编码方式下可能对应的实际存储形式是不一样的。 但反过来。给你一串这个数字 ， 不知道它的编码方式是毫无意义的。
因为unicode定义了这个地球所有的字符和数字的映射关系，看作是一个“上层建筑”，一个蓝图，各个编码就是具体的施工，因为地形的原因，气候关系，各个国家根据这个蓝图都会有有些变动（这个例子不够好）。

**同一个`unicode`在不同编码下肯定是不一样的,但是不同的`unicode`在不同的编码下有可能是一样的**。这个很容易验证，只要随便找个字符字节，`decode`一下，只要能`decode`出来，这个字节符合编码的格式，然后还原出来的`unicode`就是在那个编码下对应的`unicode`但是两者是相同的字节。下面有一个例子，看下面。**所以，像`\xe9`这种给出不一定就是utf-8编码方式**，有些只是刚好符合编码格式，但是不一定有意义。

```python
>>> c.decode('ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
```
因为`c`不是`utf-8`来编码的所以用`ascii`来“解密”这个逆过程是行不通的
当得到了`unicode`又可以用不同的“加密方式”加密了。

# python中的编码深入（python2）
首先明确`0x41`和`\x41`的区别
```python
>>> 0x41
65
>>> \x41
  File "<stdin>", line 1
	\x41
	   ^
SyntaxError: unexpected character after line continuation character
>>> '\x41'
'A'
```
**`0x41`是`numeric` ，`\x41`是 `character`，它只有在字符串中才有意义。 两者虽然在电脑中都是存着`01000001`,但是看待它的角度不一样。 **

## str类和unicode类

**`str`和`unicode`是两个不同的类**
---

在python的REPL中，类似`w = '{whatever}'`，这样给出的，代表w是一个`str`，
> **str hold bytes ! str hold bytes ! str hold bytes !**
**str 存储的是已经编码后的字节序列，输出是看到每个字节用16进制表示，以`\x`开头，每个汉字会占用3个字节的长度。**

> str is string of bytes
> unicode is string of unicode character

```python
>>> c='中文'
>>> c
'\xe4\xb8\xad\xe6\x96\x87'
>>> cu=u'中文'
>>> cu
u'\u4e2d\u6587'
>>> print c
中文
>>> print cu
中文
>>> len(c)
6
>>> len(cu)
2
```
`cu=u'中文'`表示`cu`的编码指定为`unicode`了。这个是python的内部编码。
**我现在有一个疑问，那这个`cu`在内存中保存的是什么样的？？？** [Todo]

**一个以bytes 为单位，一个以unicode character 为单位**
> Unicode started out using 16-bit characters instead of 8-bit characters.!!!

我的理解是
`len(cu) == 2` 表示`cu`里面有2个code point 
`len（c) == 6` 表示`c`有6个bytes

## 那这里就有两个问题了
### -[x] str存储已经编码后的字节序列，是用什么编码？？
从键盘上按下到屏幕上显示的这一步我们先不管，我猜想是涉及到键盘的工作原理**[Todo](http://hsmaterial.moe.edu.tw/file/computer/7I44/class800/7I44/final/7i44_2_4/7i44_2_4.htm)**和输入法的原理**[Todo]**,改天再把这一块补上，现在先就关注再python内部的编码。
```python
import sys
>>> sys.stdin.encoding
'UTF-8'
```
是默认用`sys.stdin.encoding`来编码输入的字符。

说到这里，python中有好几个有关编码的函数或值
- sys.stdin.encoding
- sys.stdout.encoding
- sys.getdefaultencoding()
- sys.getfilesystemencoding()

各自的用处都不一样
![encoding in python](http://onexs3cnv.bkt.clouddn.com/python%E7%BC%96%E7%A0%81.png)

### -[] `w＝'中文'` 是需要编码一下的 用`utf-8`那这样 `w = '\xe9'`也要先`utf-8`编码？
这个我还不清楚，因为不可能一个不编码，一个编码，应该是统一的形式，但是对`\xe9`进行`utf-8`的编码是不行的因为对于但字节的，`utf-8`是高位是`0`开头的，所以这个不可能用`utf-8`编码成功，所以我猜测是因为`\x`,有这个，直接以字节码的形式传入进来了不用编码了。

## print 
当做`print c`的时候，会把`c`的byte string， 也就是字节流传到终端，终端接受到这一组字节流要用终端的编码来解码这个字节流（毕竟不是字符集，传送过来的只是编码方式，所以找字符对应关系还得还原），这样就又回到了`unicode`的形式，然后接下来就是[字符怎么显示到计算机屏幕上的问题了](http://www.mmmmmcclxxvii.cn/2015/11/12/how-character-display-on-screen/)
### 实验
```python
>>> c = '中文'
>>> c.decode('utf-8')
u'\u4e2d\u6587'
>>> c.decode('utf-8').encode('gb2312')
'\xd6\xd0\xce\xc4'
```
我在iTerm下先把Terminal的Character Encoding改为`GB 2312`
![change terminal encoding](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%208.03.38%20AM.png)
可以看到结果是被正确打印出来
![correct result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%208.05.13%20AM.png)
但当我把编码随便改成另外国家的
![other encoding](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%208.08.30%20AM.png)
然后再打印的时候就不对了
![wrong result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%208.09.04%20AM.png)
但是！ `cg`里面保存是一样的
![cg](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%208.10.14%20AM.png)
---

这也就是说当你终端的编码和在python中处理字符的编码不一致的时候，打印结果可能出现问题。之所以是可能，因为如果都是英文的话，因为都兼容ascii码,所以会打印出你想要看到的样子。

---
```python
>>> cg = '\xd6\xd0\xce\xc4'
>>> cg.decode('iso 8859-11')
u'\u0e36\u0e30\u0e2e\u0e24'
>>> cg.decode('gb2312')
u'\u4e2d\u6587'
```
这里就是不同`unicode`在不同的编码下有着相同的字节的例子
然后
```python
>>> cg.decode('iso 2022-jp')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  UnicodeDecodeError: 'iso2022_jp' codec can't decode byte 0xd6 in position 0: illegal multibyte sequence
```
上面那个能对`iso 8859-11`解码也只是凑巧，这个对`iso 2022-jp`就不行。

### 实验2
如果是`print`一个unicode对象的话
```python
>>> cgt = cg.decode('iso 8859-11')
>>> print cgt
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
```
看着样子好像是要转化成字节流传送到终端再解码。那这样不会出现什么问题么？
因为`unicode`的code point和字符之间是一一对应的，我编码成`utf-8`也好，`gbk`也好，其他什么的也好，只要能编成，我只是用它做个过度，我只需确保解码的时候用的是一致的编码的就行了，现在这里的问题就是`ascii`码不能编成，因为格式不支持。这个`ascii`应该是`sys.getdefaultencoding()`的。
以下终端编码是`utf-8`
```python
>>> cgt = cg.decode('iso 8859-11')
>>> cgt.encode('utf-8')
'\xe0\xb8\xb6\xe0\xb8\xb0\xe0\xb8\xae\xe0\xb8\xa4'
>>> print '\xe0\xb8\xb6\xe0\xb8\xb0\xe0\xb8\xae\xe0\xb8\xa4'
ะฮฤ
```
这个显示的不知道是不是一致的，看着又像又不像，少了一个点貌似，到底对不对？？

## 读取文件
### 读文件，文件的编码
现在我先建立一个`gbk.txt`的文件，在vim中`:set fileencoding=gbk`,有关vim中的编码[看这里](http://www.mmmmmcclxxvii.cn/2017/04/10/vim-encoding/)
输入内容`我叫陈烨`保存。
先看一下`utf-8`的编码长什么样，`gbk`编码长什么样
```python
>>> c = '我叫陈烨'
>>> c
'\xe6\x88\x91\xe5\x8f\xab\xe9\x99\x88\xe7\x83\xa8'
>>> c.decode('utf-8').encode('gbk')
'\xce\xd2\xbd\xd0\xb3\xc2\xec\xc7'
```
然后读取文件
```python
>>> f = open('gbk.txt')
>>> fr = f.read()
>>> fr
'\xce\xd2\xbd\xd0\xb3\xc2\xec\xc7\n'
```
可以看出，我保存的是`gbk`编码格式，现在读入的也是`gbk`编码的格式，因为计算机他操作的就在“第三层”（这里先忽略第四层）所以，**如果我不知道原来文件的编码是什么，直接操作文件内容也是没有意义的**，只是现在大部分都是`utf-8`，一切都恰好行的通，等出现乱码的时候就应该知道是编码出现问题了。

### 读文件，文件内容的操作
现在我建立一个文件叫做wr.TARIN  , 这是里面的内容是
`你好 中国 Hello China 1 2 3`
```python
>>> import sys
>>> sys.getfilesystemencoding()
'utf-8'
>>> f = open('wr.TRAIN')
>>> content=f.readline()
>>> content
'\xe4\xbd\xa0\xe5\xa5\xbd \xe4\xb8\xad\xe5\x9b\xbd Hello China 1 2 3\n'
```
这个`sys.getfilesystemencoding()`是不是用来文件解码的还不清楚！！！【Todo】
文件都是以字节流的方式读进来的？  但不管怎么样，读进来的是一段字符串，重点是你怎么看，都是这样的01010的数字，关键在于怎么翻译，所以要知道它文件原来的编码方式。
```python
>>> content_list = content.split()
>>> content_list
['\xe4\xbd\xa0\xe5\xa5\xbd', '\xe4\xb8\xad\xe5\x9b\xbd', 'Hello', 'China', '1', '2', '3']
>>> print content
你好 中国 Hello China 1 2 3
>>> print content_list
['\xe4\xbd\xa0\xe5\xa5\xbd', '\xe4\xb8\xad\xe5\x9b\xbd', 'Hello', 'China', '1', '2', '3']
>>> print content_list[0]
你好
```

那这里就有一个问题，为什么`print content_list`显示的是以这样的形式，而不是
`['你好','中国','Hello','China','1','2','3']`
这样子？
这其实是两个问题。`content_list`是`list`类型，它不是一个`str`！！！
```python
>>> l = ['中文','你好']
>>> l
['\xe4\xb8\xad\xe6\x96\x87', '\xe4\xbd\xa0\xe5\xa5\xbd']
>>> print l
['\xe4\xb8\xad\xe6\x96\x87', '\xe4\xbd\xa0\xe5\xa5\xbd']
>>> print str(l)
['\xe4\xb8\xad\xe6\x96\x87', '\xe4\xbd\xa0\xe5\xa5\xbd']
>>> str(l)
"['\\xe4\\xb8\\xad\\xe6\\x96\\x87', '\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd']"
```
在打印`list`类型的时候，会先把`list`转为`str`，这样就发现`\x`编程了`\\x`，相当于`\xe4`原本表示编码的，被当成字符串处理了，说了一切看你怎么看的问题。
但其实本来是`list`转为字符串格式的话，会调用`repr`来转化，但是效果是和`str`是一样的。
```python
>>> repr(l)
"['\\xe4\\xb8\\xad\\xe6\\x96\\x87', '\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd']"
```
```python
>>> lc = ','.join(l)
>>> print lc
中文,你好
>>> lc
'\xe4\xb8\xad\xe6\x96\x87,\xe4\xbd\xa0\xe5\xa5\xbd'
```
但是如果想要有`[...]`的效果怎么办
```python
>>> print str(l).decode('string_escape')
['中文', '世界']
```
`string_escape`是转义字符
```python
>>> repr(l)
"['\\xe4\\xb8\\xad\\xe6\\x96\\x87', '\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd']"
>>> repr(l).decode('string_escape')
"['\xe4\xb8\xad\xe6\x96\x87', '\xe4\xbd\xa0\xe5\xa5\xbd']"
>>> print "['\xe4\xb8\xad\xe6\x96\x87', '\xe4\xbd\xa0\xe5\xa5\xbd']"
['中文', '你好']
```
也就是相当于把`\\x`还原回`\x`了的一步操作。如果已经是`\x`再这样弄，没什么效果。

### 写入文件
```python
>>> ','.join(content_list)
'\xe4\xbd\xa0\xe5\xa5\xbd,\xe4\xb8\xad\xe5\x9b\xbd,Hello,China,1,2,3'
>>> fw = open('out.TEST','w')
>>> fw.write(','.join(content_list))
>>> fw.close()
```
![file_out](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202016-10-04%20at%209.11.11%20PM.png)

还可以用`unicode`统一来处理文本，不过在写入文件时，还是要转换为“第三层”的格式，毕竟`unicode`是虚浮的！！！
```python
>>> fw=open('out.TEST','w')
>>> content_u_list_conjunction = ','.join(content_u_list)
>>> content_u_list_conjunction
u'\u4f60\u597d,\u4e2d\u56fd,Hello,China,1,2,3'
>>> fw.write(content_u_list_conjunction)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec cant encode characters in position 0-1: ordinal not in range(128)
>>> fw.write(content_u_list_conjunction.encode('utf-8')) #要指定encode编码，不然用默认的
>>> fw.close()
  
```
这个默认的应该就是`sys.getdefaultencoding()`指定的吧。


## python 脚本文件的编码
经常可以看到一些`.py`文件的头两行是怎么写的
```python
#!/usr/bin/env/python
# coding=utf-8
# 或
# -*- coding: utf-8 -*-
```
> If a comment in the first or second line of the Python script matches the regular expression coding[=:]\s*([-\w.]+), this comment is processed as an encoding declaration; the first group of this expression names the encoding of the source code file. The encoding declaration must appear on a line of its own. If it is the second line, the first line must also be a comment-only line. The recommended forms of an encoding expression are

> `# -*- coding: <encoding-name> -*-`
> from [Encoding declarations](https://docs.python.org/2.7/reference/lexical_analysis.html#encoding-declarations)

> Python will default to ASCII as standard encoding if no other encoding hints are given.
> from [PEP 263 -- Defining Python Source Code Encodings](https://www.python.org/dev/peps/pep-0263/)

如果没有指定，脚本默认会用ascii码来解析文件内容，这时如果遇到有中文的，那就会报错
![without specific encoding](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-10%20at%2011.30.09%20AM.png)

还有一些[example](https://www.python.org/dev/peps/pep-0263/#id9)

# 参考资料
1. [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](http://www.joelonsoftware.com/articles/Unicode.html)
2. [python新手必碰到的问题---encode与decode，中文乱码](http://www.51testing.com/html/63/524463-817888.html)
3. [字符编码详解](http://noalgo.info/571.html)
4. [Unicode HOWTO](https://docs.python.org/2/howto/unicode.html)
5. [Meaning of 0x and \x in python hex strings?](http://stackoverflow.com/questions/16903192/meaning-of-0x-and-x-in-python-hex-strings)
6. [unicode-table](http://unicode-table.com/en/#00E9)
7. [Why does Python print unicode characters when the default encoding is ASCII?](http://stackoverflow.com/questions/2596714/why-does-python-print-unicode-characters-when-the-default-encoding-is-ascii/21968640#21968640)
8. [len() with unicode strings](http://stackoverflow.com/questions/24832335/len-with-unicode-strings)
9. [Python, len and slices on unicode strings](http://stackoverflow.com/questions/5695714/python-len-and-slices-on-unicode-strings)
10. [len(unicode string)](http://stackoverflow.com/questions/39835779/lenunicode-string#39835844)
11. [Python 2.7 解决写入文件的中文乱码问题](http://blog.csdn.net/huxian370/article/details/51145926)
12. [python write file dealing with encode](http://stackoverflow.com/questions/39807985/python-write-file-dealing-with-encode)
13. [Pragmatic Unicode](http://nedbatchelder.com/text/unipain.html)
14. [Python编程的中文问题](http://noalgo.info/578.html)

---

1,2,4,7,13,14 推荐要看一下

---

## 一些重要的摘出来
### 4
> The Unicode standard describes how characters are represented by code points. A code point is an integer value, usually denoted in base 16. In the standard, a code point is written using the notation `U+12ca` to mean the character with value `0x12ca` (4810 decimal). The Unicode standard contains a lot of tables listing characters and their corresponding code points:
> ```
> 0061    'a'; LATIN SMALL LETTER A
> 0062    'b'; LATIN SMALL LETTER B
> 0063    'c'; LATIN SMALL LETTER C
> ...
> 007B    '{'; LEFT CURLY BRACKET
> ```
> **Strictly, these definitions imply that it’s meaningless to say ‘this is character U+12ca’. U+12ca is a code point, which represents some particular character; in this case, it represents the character ‘ETHIOPIC SYLLABLE WI’. In informal contexts, this distinction between code points and characters will sometimes be forgotten.**
> 
> **A character is represented on a screen or on paper by a set of graphical elements that’s called a glyph. The glyph for an uppercase A, for example, is two diagonal strokes and a horizontal stroke, though the exact details will depend on the font being used. Most Python code doesn’t need to worry about glyphs; figuring out the correct glyph to display is generally the job of a GUI toolkit or a terminal’s font renderer.**
> 
> a Unicode string is a sequence of code points, which are numbers from 0 to 0x10ffff. This sequence needs to be represented as a set of bytes (meaning, values from 0-255) in memory. The rules for translating a Unicode string into a sequence of bytes are called an encoding.
 
### 12
There are many encodings and they define 128-255 differently.
> For example, character 185 (0xB9) is ą in windows-1250 encoding, but it is š in iso-8859-2 encoding.
> So, what happens if you print \xb9? It depends on the encoding used in the console. In my case (my console uses cp852 encoding) it is:
> ```python
> >>> print '\xb9'
> ╣
> ```
> **Because of that ambiguity, string '\xb9' will never be represented as '╣' (nor 'ą'...). That would hide the true value. ** (这里解释了为什么用`\xb9`这样字节来保存，而不打印出来实际的字符)It will be represented as the numeric value:
> ```python
> >>> '\xb9'
> '\xb9'
> #Also:
> >>> '╣'
> '\xb9'
> ```
> 
> **But what happens if variable is just entered in the console?When a variable is enteren in cosole without print, its representation is printed.** It is the same as the following:
> ```python
> >>> print repr(content)
> '\xe4\xbd\xa0\xe5\xa5\xbd \xe4\xb8\xad\xe5\x9b\xbd Hello China 1 2 3\n'
> ```

> Unlike str objects, which are strings of bytes, unicode objects are strings of unicode characters
> characters != bytes. a utf16 character is 2 bytes, but only one character

### 14

> 内置的open()方法打开文件时，read()读取的是str，读取后需要使用正确的编码格式进行decode()。write()写入时，如果参数是unicode，则需要使用你希望写入的编码进行encode()，如果是其他编码格式的str，则需要先用该str的编码进行decode()，转成unicode后再使用写入的编码进行encode()。如果直接将unicode作为参数传入write()方法，Python将先使用源代码文件声明的字符编码进行编码然后写入。

