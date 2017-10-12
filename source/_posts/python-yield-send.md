---
title: python里面yield和send
date: 2017-10-12 00:20:08
categories: python
tags: [python,python-piece]

---

前序资料链接：
- [python生成器详解](http://codingpy.com/article/python-generator-notes-by-kissg/)
- [python yield实现](http://www.cnblogs.com/coder2012/p/4990834.html)
- [python generator](http://www.bogotobogo.com/python/python_generators.php)

下面是自己的理解和补充
<! --more -->

一个函数里面有申明`yield`关键字的时候，这个函数就是生成器generator. 比如

```python
def g():
	value = (yield 1)
	print 'continue'
	value = (yield value)
```

测试：

```python
>>> f = g()
>>> f.next()
1
>>> f.send(2)
continue
2
```

`yield`其实类似做了一个中断跳到其他地方的操作。`send`方法就是返回中断处继续执行

`value = (yield 1)`要分开来看,`yield 1`和`value = yield`前面是`yield`出去，后面是`send`进来的值赋给了`value`

**`send`方法其实是有返回值的！！！** 返回值就是生成器从下一个`yield`值。但是`send`其实也是“中断”跳到原来`yield`的生成器，直到生成一个返回到它这里，它才继续操作。这里说的是两个函数分别包括`send`和`yield`，就是两个函数跳来跳去。

这个特性来解决生产者消费者问题，就是[协程](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328689835ecd883d910145dfa8227b539725e5ed000)的概念

```python
#!/usr/bin/python
#-*- coding: utf-8 -*-
# File Name: test_yield.py
# Created Time: Wed Oct 11 22:24:20 2017

__author__ = 'Crayon Chaney <mmmmmcclxxvii@gmail.com>'

# value = 0

def consumer():
    value = 0
    while 1:
        value = (yield value)
        if value:
            print "consuming ",value
            value = 'return here'
        else:
            break


def process(c):
    now = c.next()
    while now < 5:
        now = now + 1
        print "processing ",now
        msg = c.send(now)
        print msg
    c.close()

if __name__ == '__main__':
    c = consumer()
    process(c)
```

呈现的结果就是生产一个，消费一个
```
processing  1
consuming  1
return here
processing  2
consuming  2
return here
processing  3
consuming  3
return here
processing  4
consuming  4
return here
processing  5
consuming  5
return here
```

![状态机](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-10-12%20at%2011.03.30%20AM.png)

状态机图没有体现send返回值的，再完善一下。
