---
title: project of stackoverflow - python object(一)
data: 2017/3/14 22:27:10
categories: stackoverflow
tags: [stackoverflow,python,object]
description: 搬运stackoverflow有关python的问题 之 object部分 （一）

---
# [what does 'super' do in python](http://stackoverflow.com/questions/222877/what-does-super-do-in-python)

下面两个的区别是？

```python
class Child(SomeBaseClass):
    def __init__(self):
		super(Child, self).__init__()
```
和
```python
class Child(SomeBaseClass):
    def __init__(self):
		SomeBaseClass.__init__(self)
```
<!-- more -->

我在单个继承中已经看到`super` 被用的很多了。我能知道为什么要在多重继承的时候用它，但是还是不清楚在这种情况用它的好处。

---

180票的回答：（John Millikin)

在单一继承用`super`的好处很小--只是你不再需要硬编码基类名字到方法里面去了

然后，在多重继承里，不用`super()`几乎是不可能的。这包括常见的习语，像是mixins，interface,abstract classes等，
这能让你的代码在之后延伸。如果以后有人想写一个拓展`Child` 和 mixin的类，他们的代码不会很好的工作。

---
75票的回答：

**区别是什么？**

`SomeBaseClass.__init__(self)`意思是调用`SomeBaseClass`的`__init__`方法
然后，`super(Child,self).__init__()`意思是从`Child`类的MRO的父类中调用一个绑定方法`__init__`
如果实例是Child的子类，有可能在方法解释顺序中的下一个父类是不一样的？？？

**向前兼容间接 ？？ （Indirection with Forward Compatibility) **

这能给你什么？对于单重继承，问题中给出的例子几乎等同于静态分析。然而使用`super` 提供了具有向前兼容性的间接层
向前兼容对于经验丰富的开发者来说是很重要的。你希望你的代码在做出一些细微的改动之后还能工作。当您查看修订历史记录时，您希望准确地查看何时更改了哪些内容。

你可能先从单重继承开始，但是当你增加另外的基类，你只需要改变基类的顺序（change the line with the bases）
（if the bases change in a class you inherit from）如果类继承关系变了（比如增加了一个mixin)，其实你就没做什么改变。
尤其在python2中，要想给super正确的方法参数是很难的。如果你知道你在单重继承下正确的使用`super`，这样是的调试就容易一点了

**依赖注入 Dependency Injection **

其他人可以使用你的代码然后插入一些父类到方法解释中(method resolution):

```python
class SomeBaseClass(object):
    def __init__(self):
		print('SomeBaseClass.__init__(self) called')
			
class UnsuperChild(SomeBaseClass):
	def __init__(self):
		print('UnsuperChild.__init__(self) called')
		SomeBaseClass.__init__(self)
							
class SuperChild(SomeBaseClass):
	def __init__(self):
		print('SuperChild.__init__(self) called')
		super(SuperChild, self).__init__()
```

现在你增加其他类，然后在Foo和Bar之间插入一个类

```python
class InjectMe(SomeBaseClass):
    def __init__(self):
		print('InjectMe.__init__(self) called')
		super(InjectMe, self).__init__()
				
class UnsuperInjector(UnsuperChild, InjectMe): pass
					
class SuperInjector(SuperChild, InjectMe): pass
```

使用un-super子类未能注入依赖，因为你是用的子类在自己执行打印后调用的是硬编码方法

```python
>>> o = UnsuperInjector()
UnsuperChild.__init__(self) called
SomeBaseClass.__init__(self) called
```

然而使用`super`的子类能正确的依赖注入

```python
>>> o2 = SuperInjector()
SuperChild.__init__(self) called
InjectMe.__init__(self) called
SomeBaseClass.__init__(self) called
```
(我：因为super按照MRO来寻找next类的，不是就是去找父类SomeBaseClass,
因为SuperInjector的MRO是自身> UnsuperChild > InjectMe > SomeBaseClass > object

还有就是 super 不是在SuperChild内么，为什么要按SuperInjector的MRO来？？
这里应该是因为SuperInjector的init没有定义，然后是用的supserchild的，但是还是按照自身的MRO来。
怎么做实验

)

__结论__
一直使用`super`来引用父类就好了

你想要引用的父类是MRO下一个类，而不是你看到的继承的关系

不使用`super` 回让你代码的使用者多了很多不必要的限制

---

# 我的：
一个例子就是
```python
from collections imoprt Counter, OrderedDict

class OrderedCounter(Counter, OrderedDict):
	pass

oc = OrderedCounter("abracadabra")
```
之前还一直奇怪这个为什么类里面pass，什么都不用写就能结合，现在知道是因为有super
相当于我先把参数传递到Counter初始化，然后因为有super找到的是下一个MRO，然后到OrderedDict初始化
相当于两个工序，先count再order。

---

# [How does Python's super() actually work, in the general case?](http://stackoverflow.com/questions/33290894/how-does-pythons-super-actually-work-in-the-general-case/33291315?noredirect=1#comment72867412_33291315)

现在有很多有关`super()`的资源，包括[这个](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)博客写的，还有很多stackoverflow上的问题。但是我感觉它们都没有解释它在普遍情况下是怎么工作的，也就是底层的实现。

考虑下面的这个继承层次：

```python
class A(object):
    def foo(self):
		print 'A foo'
			
class B(A):
	def foo(self):
		print 'B foo before'
		super(B, self).foo()
		print 'B foo after'
										
class C(A):
	def foo(self):
		print 'C foo before'
		super(C, self).foo()
		print 'C foo after'
																	
class D(B, C):
	def foo(self):
		print 'D foo before'
		super(D, self).foo()
		print 'D foo after'
```
如果你读过python的方法解释顺序的规则，你就知道上面的MRO是（D,B,C,A,object)。 这是被D.__mro__决定的
`(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>))`

和
```python
d = D()
d.foo()
```

打印出的：

```python
D foo before
B foo before
C foo before
A foo
C foo after
B foo after
D foo after
```
结果符合MRO。 但是，考虑上面的B中的`super(B,self).foo()` 实际调用的是`C.foo`，这个是在`b=B()`中；`b.foo()` 会直接到`A.foo` 很显然使用`super(B,self).foo()`不是`A.foo(self)`的快捷键，虽然有时是

很显然`super()`是有意识的在意之前的调用，然后尝试着去跟随总的MRO链。我觉得有两个方法能完成这个。
第一个是做了一些类似在链中将`super`对象传递给下一个方法的`self`参数,像原来`self`对象那样，但是包含了这个信息，但是这样似乎会破坏很多东西(`super(D,d) is d`是False)，然后做了一些实验，我觉得这个方法不可行。

另外一个方法是类似全局变量来保存MRO和现在的链上的位置。我想象中的`super`算法是这样的：

1. 我们当前有工作的环境吗？如果没有，创建一个队列，获取MRO，将除了第一个之外的所有元素入队列
2. 将当前上下文的MRO队列中pop一个元素，在构建`super`实例的时候将它作为当前的class
3. 当访问`super`实例的一个方法的时候，在当前class上寻找，然后调用它

但是，这样却没有解释类似使用不一样的基类当作第一个参数来调用`super`，或者调用不同方法。（这段好别扭）
我想知道这个的更普遍的算法。而且，如果这样的context存在的话，我能看吗？我能破坏他么？这当然是一个糟糕的想法，但是python希望你成为一个成熟的人尽管你不是。

这同样也引入了好多设计的考量。如果我写的B只考虑了它和A的联系，然后又有其他人写了C，还有其他人写了D，我的`B.foo()`方法必须找到一个能兼容`C.foo()`的方法来调用`super`，尽管我在写它的时候C不存在。如果我想要我的类能很简单的扩展，那我必须要考虑这些。但是我不清楚这是不是比简单的将所有的`foo`的特征设置成一样来的更复杂。还有一个问题就是什么时候将代码放在`super`之前，什么时候之后，即使在仅考虑B的基类的时候它没有什么区别

---

7票的回答：

> super() is then obviously aware of the previous calls before it

它不是。当你做`super(B,self).foo`,`super`知道你的MRO因为它会从`type(self).__mro__`中得到。然后它知道应该在MRO的B后面那里开始寻找`foo`，一个粗略的纯 python写的应该是这样的：
```python
class super(object):
    def __init__(self, klass, obj):
		self.klass = klass
		self.obj = obj
	def __getattr__(self, attrname):
		classes = iter(type(self.obj).__mro__)

		# search the MRO to find self.klass
		for klass in classes:
			if klass is self.klass:
				break

		# start searching for attrname at the next class after self.klass
		for klass in classes:
			if attrname in klass.__dict__:
				attr = klass.__dict__[attrname]
				break
		else:
			raise AttributeError

		# handle methods and other descriptors
		try:
			return attr.__get__(self.obj, type(self.obj))
		except AttributeError:
			return attr

```
> If I wrote B thinking only of its relation to A, then later someone else writes C and a third person writes D, my B.foo() method has to call super in a way that is compatible with C.foo() even though it didn't exist at the time I wrote it!

并不要求你要从随机的类中多种继承。除非`foo`是被特意设计成在多重继承的时候将兄弟类的重写。D不应该存在。



