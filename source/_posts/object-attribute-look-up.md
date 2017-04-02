---
title: python中的对象属性查找
date: 2017-03-08 22:06:02
categories: python
tags: [python,object]
description: 分为实例调用和类调用，两者查找属性的流程是不一样的

---

[原文链接](http://www.betterprogramming.com/object-attribute-lookup-in-python.html)

这里面已经讲的很详细了。暂时还没有自己的深刻的思考和理解，就先搬运过来。

# Instance attribute look up 实例属性查找
> The implementation works through a precedence chain that gives data descriptors priority over instance variables, instance variables priority over non-data descriptors, and assigns lowest priority to getattr() if provided.

现在有一个类`C`和一个实例`c = C()`，现在调用`c.name`，相当于在实例`c`中查找`name`属性，流程如下：
```
Get the Class from Instance
Call the Class's special method __getattribute__.All objects have a default __getattribute__
	Get the Class's __mro__ as ClassParents
	For each ClassParent in ClassParents
		if the Attribute is in the ClassParent's __dict__
			if this attribute is data descriptor
				return the result from calling the data descriptor's special method __get__()
				Breaking the for each(do not continue searching the same Attribute any further)
	
	If the Attribute is in Instance's __dict__
		return the value as it is(even if the value is a data descriptor)
		#这个意思是即使是描述符也直接返回这个对象，不会去调用__get__(),返回值类似<__main__ descriptor object at Ox..>
	For each ClassParent in ClassParents
		if the Attribute is in the ClassParent's __dict__
			if is a non-data descriptor
				return the result from calling the non-data descriptor's special method __get__()
			if it is Not a descriptor
				return the value
	
	If Class has the special method __getattr__
		return the result from calling the Class's special method __getattr__
	
	Raise an AttributeError
```

有几个点要记住！
1. descriptors are invoked by the `getattribute()` method
2. overriding `getattribute()` prevents automatic descriptor calls
3. `getattribute()` is only available with new style classes and objects
4. `object.getattribute()` and `type.getattribute()` make different calls to `get()`
5. data descriptors always override instance dictionaries.
6. non-data descriptors may be overridden by instance dictionaries.

# Class attribute look up 类属性的查找
一个`metaclass` `M`，和一个`M`的实例，类`C`，这时候调用`C.name`的流程：
其实和实例访问一一对应，就是各自都升了一个level
```
Get the MetaClass from Class
Call the Metaclass's special method __getattribute__
	Get the Metaclass's __mro__ as MetaParents
	For each MetaParent in MetaParents
		if the Attribute is in the MetaParent's __dict__
			if is a data descriptor
				return the result from calling the data descriptor's special method __get__()
	
	Get the Class's __mro__ as ClassParents
	For each ClassParent in ClassParents
		if the Attribute is in the ClassParents's __dict__
			if is a(data or non-data) descriptor
				return the result from calling the descriptor's special method __get__()
				# 实例在这层上不会调用__get__()
			else
				return the value
	
	For each MetaParent in MetaParents
		if the Attribute is in the MetaParents's __dict__
			if is a non-data descriptor
				return the result from calling the non-data descriptor's special method __get__()
			if it is NOT a descriptor
				return the value
	
	If MetaClass has the special method __getattr__
		return the result from calling the MetaClass's special method __getattr__
	
	Raises an AttributeError
```

# [例子](https://gist.github.com/Crayon277/cd05d4c058a5e11c7bd202aa44fff876)

```python
#!/usr/bin/env python
# coding=utf-8

class Desc(object): # 定一个非数据描述符
    def __init__(self, msg):
        self.msg = msg
    
    def __get__(self, instance, owner=None):
        return "{0}: {1}".format(self.typ, self.msg) # self.typ是啥？？？？

    
class NonDesc(Desc):
    # non-data descriptor 
    typ = 'NonDesc'


class DataDesc(Desc):
    # data descriptor
    typ = 'DataDesc'

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass


class M(type):
    x = 'x from M'
    y = NonDesc('y from cls M')
    z = DataDesc('z from cls M')
    
    def __getattr__(self, name):
        return "getattr M {0}".format(name)


class A(object):
    #t = 't from A'
    #u = NonDesc('u from cls A')
    #v = DataDesc('v from cls A')
    x = 'x from A'
    y = NonDesc('y from cls A')
    z = DataDesc('z from cls A')


class B(A):
    """
    metaclass is M
    """
    __metaclass__ = M
    """
    这个metaclass什么用？？？？
    """
    
    
class C(B):
    """
    metaclass is inherited from C
    """
    def __getattr__(self, name):
        return "getattr C: {0}".format(name)
    

c = C()
print '******'
print 'c.__class__', c.__class__  #其实就是type(c), 还有注意c是新式类，格式应该是<class '__main__.C'>之类的
print 'c.__class__.__getattribute__', c.__class__.__getattribute__ # 因为c.__class__也是一个对象
# <slot wrapper '__getattribute__' of 'object' objects>
print 'c.__class__.__mro__', c.__class__.__mro__ # method resolution order C B A O

print '******'
print 'c.x', c.x 
"""
父类们寻找顺序是根据c.__class__.__mro__ 来的
c先去寻找父类们中有没有x的描述符，没有，然后在自己的__dict__中找x，也咩有，然后再去父类们的__dict__中找
有没有这个属性名的non-data 描述符，没有，不是描述符而是直接属性的呢？A中有，返回A中的x值
"""
print 'c.y', c.y
"""
同上，父类的顺序不废话了
最终在第三阶段找到A中的y，它是一个non-data descriptor，NonDesc: y from cls A
"""
print 'c.z', c.z
"""
在第一个阶段中的A中找到z 是一个data descriptor，饭后 DataDesc: z from cls A
"""
print 'c.nope', c.nope
"""
当前三个阶段都找不到的时候，如果类中有定义__getattr__，就到这里去，没有报错
这里所有三个阶段没有nope属性，然后到了__getattr__，返回 getattr C: nope
"""

c.t = 't from obj c'
c.u = NonDesc('u from obj c')
c.v = DataDesc('v from obj c')
c.x = 'x from obj c'
c.y = NonDesc('y from obj c')
c.z = DataDesc('z from obj c')

print '******'
print 'c.t', c.t
"""
如上，在第二个阶段找到t, 返回 t from obj c
"""
print 'c.u', c.u
"""
在第二个阶段在c字典里面找到，不管是值还是descriptor ，这里会调用__get__()  NonDesc: u from obj c
update:更正
因为在
"""
print 'c.v', c.v
"""
在第二阶段c字典里找到, 调用__get__() ，返回 DataDesc: v from obj c
"""
print 'c.x', c.x
"""
因为在第一阶段是在类父类中找描述符，虽然A中有属性x但不是描述符，因此进入第二个阶段，在实例字典中找，不管是不是描述符
只要名字对了就返回. 这里在这个阶段返回x from obj c
"""
print 'c.y', c.y
"""
同上，返回的是 NonDesc: y from obj c
"""
print 'c.z', c.z
"""
同上，返回的是 DataDesc: z from obj c
"""

print '******'  # 这里是用到 class attribute look up 。 以上是对实例进行点运算
print "C.x", C.x
"""
因为B的metaclass是M了，C继承B，C现在的metaclass也是M
现在要将上面的所有概念都升级，原来class变成metaclass，原来instance变成class
先根据metaclass里的mro决定先后顺序metaparents
因为这里是类属性访问，C类的metaclass是M，M.__mro__ 是 (<class '__main__.M'>, <type 'type'>, <type 'object'>)
按顺序找x的描述符，但M中没有x的描述符，然后type，object都没有。
进入第二个阶段，先计算C.__mro__,按照顺序依次访问类字典C,B,A,O ， 
如果有属性重名，先要描述符，不然只要是在__dict__中就返回
c中没有x,然后去B，B里面也咩有x，到A中，有x但是不是描述符，没关系直接返回,因为也没有名字为x的描述符了。
返回x from A
"""
print "C.y", C.y
"""
同上，虽然在M中有y但是是非数据描述符，在第2阶段中的A类中找到y非数据描述符,返回 NonDesc: y from cls A
"""
print "C.z", C.z
"""
这是在第一个阶段中的M里找到z数据描述符， 返回 DataDesc: z from cls M
"""
print "C.nope", C.nope
"""
上面三个阶段都没有，进入第四个阶段，这个阶段不是去C中的__getattr__，因为上面说了都升了一级，现在是在
M中的__getattr__，如果M里面没有__getattr__，那么就回报错，现在M有，返回 getattr M nope
"""

C.t = 't from obj C'
C.u = NonDesc('u from obj C')
C.v = DataDesc('v from obj C')
C.x = 'x from obj C'
C.y = NonDesc('y from obj C')
C.z = DataDesc('z from obj C')

"""
如果是类属性访问，好像没有A，B什么事 !!!!
写在流程搞错之前，之前在第二阶段没有计算类的__mro__
重新看一下流程
"""
print '******'
print "C.t", C.t
"""
因为metaclass以及mro中都没有t，进入下一个阶段
在第二阶段中现在C类中有t这个属性了，返回 t from obj C
"""
print "C.u", C.u
"""
同上，在第二阶段中C类的__dict__中找到，返回 NonDesc: u from obj C
"""
print "C.v", C.v
"""
同上，在第二阶段中返回 DataDesc: v from obj C
"""
print "C.x", C.x
"""
和M中有重名，但是因为M中的不是数据描述符，这个的优先级高，在第二阶段返回 x from obj C
虽然A中也有x，但是mro顺序C排在A前面
"""
print "C.y", C.y
"""
同上，有重名，但是M中是非数据描述符，第一阶段过，到第二阶段，返回 NonDesc: y from obj C
然后A中同理
"""
print "C.z", C.z
"""
重名，但是z在M中是数据描述符，在第一阶段就返回 DataDesc: z from cls M
"""
print "C.nope", C.nope
"""
这个没有变 getattr M nope
"""
```
