---
title: project of stackoverflow - python piece (一)
date: 2016-02-12 08:11:45
updated: 2016-02-12 08:11:45
categories: stackoverflow 
tags: [python,stackoverflow,python-piece]
description: 搬运stackoverflow有关python的问题 之 小知识点 (一)、

---

[Why does Python print unicode characters when the default encoding is ASCII?](http://stackoverflow.com/questions/2596714/why-does-python-print-unicode-characters-when-the-default-encoding-is-ascii/21968640#21968640)

在python 2.6的交互式界面中：
```python
>>> import sys
>>> print sys.getdefaultencoding()
ascii
>>> print u'\xe9'
é
>>> 
```

我原本预想打印出来的结果是乱码或者直接报错，因为字符 "é" 并不是`ASCII`码所定义的范围，而且我没有指定编码。我想我是不是没有懂这个`ASCII`码作为默认编码的真正意思。

---

73票的回答：

谢谢不同回复的各方面的回答，我觉得我们可以连起来成一个解释
当尝试着去打印unicode字符串的时候，`u'\xe9'`，Python会隐式的先尝试去对这个字符串用`sys.stdout.encoding`返回的编码方案编码。实际上，python在一开始初始化的时候就记录了这个设置。如果不能在环境中找到合适的编码，才会使用默认的`ASCII`码编码。

比如，我使用一个默认编码是`UTF-8`的bash shell。当我在它上启动python，它会使用这个设置：
```bash
$ python

>>> import sys
>>> print sys.stdout.encoding
UTF-8
```
让我们先暂时退出python shell然后重新用一些伪造的编码设置bash的环境
```bash
$ export LC_CTYPE=klingon
# we should get some error message here, just ignore it.
```
然后重新启动python shell，证实一下他确实恢复到它默认的acsii编码
```bash
$ python

>>> import sys
>>> print sys.stdout.encoding
ANSI_X3.4-1968
```
那就对了！

如果现在你要打印一些在ascii码定义之外的unicode字符，你就会得到漂亮的错误提示
```bash
>>> print u'\xe9'
UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' 
in position 0: ordinal not in range(128)
```
---
让我们退出python，不要管bash shell

我们现在在python输出字符后观察会发生什么。为了能够观察，我们需要在图形界面的终端启动bash shell(我使用的是Gnome Terminal)然后我们设置终端的输出编码为`ISO-8859-1 aka latin-1`(图形界面的终端通常在下拉菜单里面都有可以设置字符编码的选项)注意，**这个不会改变shell 真正的环境编码。他只改变终端自己对于给出输出的解码方式，有点像浏览器的行为**。因此你可以改变终端的编码，那是和shell环境的编码是相互独立的。然后启动从shell中启动python，核实一下`sys.stdout.encodin`是被设置成shell的环境编码(我的是UTF-8)：
> (我：插一句，bash shell的环境编码是由LC_CTYPE决定的。然后终端改为latin-1的编码，应该先在编码正常utf-8的时候先启动，然后再改编码，否则，至少我尝试下来如果一开始用latin-1编码启动终端，注意是启动终端，sys.stdou.encoding是ascii)
```python
$ python

>>> import sys

>>> print sys.stdout.encoding
UTF-8

>>> print '\xe9' # (1)
é
>>> print u'\xe9' # (2)
Ã©
>>> print u'\xe9'.encode('latin-1') # (3)
é
>>>
```
(1) python 如实的输出二进制字节字符串，然后终端接受到这个，然后尝试着去用`latin-1`的字符映射来匹配它的值。在`latin-1`，`0xe9`或者`233`对应字符`"é"`,这也是终端的显示

(2) 不管当前设置在`sys.stdou.encoding`的编码方案是什么，python先__隐式__的用这个来编码unicode，在这个例子中是`UTF-8`。在`UTF-8`编码完了后,编成了一串二进制字符串`\xc3\xa9`（后面会解释）。终端接受到这个字节流后然后尝试着去用`latin-1`去解码`0xc3a9`，但是`latin-1`的范围是`0`到`255`，所以会一个字节一个字节的解码，`0xc3a9`是2个字节长，因此`latin-1`的解码器会解释成`0xc3(195)`和`0xa9(169)`,这两个对应的字符分别是Ã和©.

(3) python 会用`latin-1`的编码方案来编码unicode的code point `u'\x9'(233)`。事实是`latin-1`的code point的范围是0-255,然后刚好好unicode字符指向在那个范围内（Turns out latin-1 code points range is 0-255 and points to the exact same character as Unicode within that range. ）。因此，在那个范围内的unicode code point 用latin-1编码会产生相同的值。所以`u'\xe9'(233)`在用latin-1编码后，会产生二进制字符串`\xe9`。终端接受这个值后，尝试这种latin-1的字符映射来匹配这个值，就像第（1）中情况一样，它对应`"é"`，在屏幕上也是这么显示的。

> (我：在二进制的时候，是直接去找对应关系，不用用这个编码去解码到unicode再去找对应，我理解错了)

现在我们在下拉菜单下面将终端的编码设置为UTF-8（就像你改变浏览器编码一样）。不需要中断python或重启shell。现在终端的编码和python的一致了，我们来重新尝试打印：
```python
>>> print '\xe9' # (4)

>>> print u'\xe9' # (5)
é
>>> print u'\xe9'.encode('latin-1') # (6)

>>>
```









