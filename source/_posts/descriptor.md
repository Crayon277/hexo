---
title: descriptor
date: 2017-03-08 08:50:01
categories: python
tags: [python,descriptor,object]

---

其实自己没有深入的研究源码，这篇也是基于阅读一些官方文档和他人的博客做的总结。
我这里的思路是从描述符的渊源到为什么有这个描述符，然后怎么用
这里先直接给出描述符的定义，先有个印象，如果一开始阅读感觉没什么联系，没关系，最终那些点将连成线的。
官方的定义：
> In general, a descriptor is an object attribute with “binding behavior”, one whose attribute access has been overridden by methods in the descriptor protocol. Those methods are __get__(), __set__(), and __delete__(). If any of those methods are defined for an object, it is said to be a descriptor.
> from -- [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html#definition-and-introduction)

也就是只要一个类定义了`__get__()`,`__set__()`,`__delete__()`当中的任意一个**特殊方法**,这个类就有了个别名“描述符”啦

# 描述符的由来
首先，因为python是一种动态编译的语言，他能在运行中动态添加类属性或类对象属性。那这些属性是被保存在比如`a.__dict__`这个里面，这里`a`是一个实例`a=A()`。其实类也有一个`__dict__`属性，通过`A.__dict__`就可以访问到.

```python
>>> class A(object):
...     def __init__(self):
...             self.attr = 1
...     def foo(self):
...             print self.attr
...
>>> a = A()
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'attr', 'foo']
>>> dir(A)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'foo']
>>> a.__dict__
{'attr': 1}
>>> A.__dict__
dict_proxy({'__module__': '__main__', '__dict__': <attribute '__dict__' of 'A' objects>, 'foo': <function foo at 0x101bba668>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None, '__init__': <function __init__ at 0x101bba5f0>})
```
注意到在`A`类中定义了一个`foo`函数，像这样的函数在C++语言中被称为成员函数，但是可以看到在`a.__dict__`中没有`foo`，在`A.__dict__`中有。其实通过访问，可以看出`a.__dict__`中保存的都是一些变量属性。这么理解，在C++中成员函数是被所有对象所共享的，不会为没个对象复制一份，这里也一样，可以看作是类的一个属性，不是实例的属性。那其实在python中，这么做是牵涉到了它的另外的两个概念，**绑定，未绑定函数**和**描述符**。先说一下，所有的类成员函数都是**`non-data despriptor`**。后面会继续解释

---

> In a nutshell, a descriptor is a way to customize what happens when you reference an attribute on a model.
> from -- [Python Descriptors, Part 1 of 2](http://martyalchin.com/2007/nov/23/python-descriptors-part-1-of-2/)

---

> Descriptor are the mechanism behind properties, methods,  static methods, class methods and `super()`
> from -- [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html#definition-and-introduction)

---

# 访问属性

[查找属性的访问顺序](http://www.mmmmmcclxxvii.cn/2017/03/08/object-attribute-look-up/)
建议先把下面的看了再来看这个

我之所以说先看下面，又不得不把这个主题先放上来，是因为其实描述符归根结底，目前看到就是对属性的取值赋值操作，**只不过是对这个操作封装了一下**而已。
```python
a.attr = 1
tmp = a.attr
```
一般的取值赋值就是这样子的，如果`attr`事先在类里面定义好了的`self.attr = arg` 上面的`a.attr = 1`其实就是重新将“标签”`a.attr`贴到`1`数值上去，如果没有那就是动态生成`attr`属性。
**但是这样的赋值太单一了，什么意思，也就是说，如果我要对赋入的值做下额外的检查，比如学生的成绩，不可能出现负数，身高也不可能出现负数。所以想到了在`__init__`当中增加一些逻辑代码进行检查**
```python
def __init__(self,score):
	assert score>=0,"value error"
	self.score = score
```
但是这样只是在初始化的时候，像`a = A(-1)`会报错，那之后如果`a.score = -100`像这样的误操作，也没人阻止。那我们又有了另一种思路
```python
def get_score(self):
	return self.score

def set_score(self,new_score):
	assert new_score>=0,"value error"
	self.score = new_score
```
通过`a.set_score(-100)`，调用一个函数，并在函数体内进行检查来进行赋值。

**总的来讲，python的属性获取，设置，这个属性只是一个存储的地方，只是一个容器，但往往你可能需要更多的功能，比如赋值的时候检验，然后，一般的，是用一些方法来做这些事情，_但是如果对于已经存在了的属性，你想用函数代替取值，赋值，你就要重写代码，找到所有用到这些属性的方法，然后改成函数_，比如上面的所有`a.score = 1`像这样的操作改成`a.set_score(1)`。这样就增加了工作量，这也是为什么在java程序中一个简单的取值都要封装成一个函数，就是为了避免何种情况，常见的模式也就是属性定义为私有变量，然后开放一个公有接口。python中的描述符只不过是另一种方法来实现这种对属性额外控制的需求而已**

# 描述符实例
描述符的用法应该不局限于下面给出的例子，要多看其他高人的代码！！！
```python
class Positive(object):
	def __init__(self,name):
		self.name = name
		
	def __get__(self,instance,owner):
		if instance is None:
			return self #这里相当于如果通过类调用,Student.score，就返回是类似<descriptor.Positive object at 0x123455..>之类的
		return instance.__dict__[self.name]

	def __set__(self,instance,value):
		if value < 0:
			raise ValueError("negative value error...")
		instance.__dict__[self.name] = value
```
上面就定义了一个描述符。其实就是一个类，描述符只是个名称而已。在我的世界里，我想叫它皮皮虾都可以。只是全世界就这么流通规定了
```python
class Student(object):
	score = Positive('score') #这句话就将score属性让描述符代理了
	def __init__(self,name,score):
		self.name = name
		self.score = score
```
现在如果有这么一个语句`s = Student('cy',100);a = s.score`，其实是相当于在做`a = type(s).__dict__['score'].__get__(s,type(s))`
可以查看`Student.__dict__`中的`score`属性是`'score': <__main__.Positive object at 0x101bb8ed0>`这样子的。
当作了`type(s).__dict__['score']`时其实就是获得了一个实例，之后还可以继续用点运算符往下接着做。

## Q&A
### Positive 描述符中的`__set__`为什么参数中没有类？
```python
>>> Student.__dict__
dict_proxy({'__module__': '__main__', 'score': <__main__.Positive object at 0x101bb8ed0>, '__dict__': <attribute '__dict__' of 'Student' objects>, '__weakref__': <attribute '__weakref__' of 'Student' objects>, '__doc__': None, '__init__': <function __init__ at 0x101bbaaa0>})
#注意上面的score属性的值
>>> Student.score = 12  # 通过类访问
>>> Student.__dict__
dict_proxy({'__module__': '__main__', 'score': 12, '__dict__': <attribute '__dict__' of 'Student' objects>, '__weakref__': <attribute '__weakref__' of 'Student' objects>, '__doc__': None, '__init__': <function __init__ at 0x101bbaaa0>})
#再对比一下score的值
```
**当类调用的时候，其实就是设置同名新值了，它将原来的描述符给替换覆盖了。**

### Student类里面的score和self.score,到底用的是哪个？？
可以先看一下
```python
>>> s = Student('cy','100')
>>> s.__dict__
{'score': '100', 'name': 'cy'}
>>> Student.__dict__
dict_proxy({'__module__': '__main__', 'score': <__main__.Positive object at 0x101bb8ed0>, '__dict__': <attribute '__dict__' of 'Student' objects>, '__weakref__': <attribute '__weakref__' of 'Student' objects>, '__doc__': None, '__init__': <function __init__ at 0x101bbaaa0>})
```
其实这里涉及到一个优先级的问题，也就是上面的访问属性的顺序链接。这里可以再跳回去看。因为描述符的优先级高！并且会改变默认的`get`,`set`方法。
> If an instance's dictionary has an entry with the same name as a data descriptor, the data descriptor takes precedence. If an instance's dictionary has entry with the same name as a non-data descriptor,the dictionary entry takes precedence.
>from [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html#descriptor-protocol)

什么是non-data descriptor后面会说明。

### `2`引申的一个问题就是如果`self.score = score`没有定义会是什么情况
```python
>>> class Student(object):
...     score = Positive('score')
...     def __init__(self,name):
...         self.name = name
...
>>> s = Student('cy')
>>> s.score = 10
>>> s.__dict__
{'score': 10, 'name': 'cy'}
>>> s.score = -10
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 10, in __set__
ValueError: negative error
```
还是照样行得通。因为`instance.__dict__[self.name] = value`.虽然初始化的时候没有`score`这个属性，但其实后面的字典操作，相当于动态增加了这个属性，而且访问的优先级照样根据那个顺序来

### 如果是`self.score = Positive('score')`会怎么样
```python
>>> class Student(object):
...     def __init__(self,name):
...         self.name = name
...         self.score = Positive('score')
...
>>> s = Student('cy')
>>> s.__dict__
{'score': <__main__.Positive object at 0x101bc70d0>, 'name': 'cy'}
>>> s.score = -10
>>> s.__dict__
{'score': -10, 'name': 'cy'}
```
没有起到作用，这是必然的。如果你知道访问顺序了之后，访问`s.score`时，因为类中没有同名的描述符，所以到实例中的`__dict__`看，如果有这个`key`，返回，但这里是赋值操作，参考另一篇[python name and values](http://www.mmmmmcclxxvii.cn/2017/03/29/python-name-and-values/)，`s.scorei = -10`只不过是将`score`这个**name**重新贴标签贴到数值`-10`上去。

### `__get__`中参数`owner`什么用，也没有用到它啊？
后面在`classmethod`中就会用到这个参数。其实函数参数写在哪里，也不一定都要用到，但更关心为什么要这么设计。后面看看源代码

看一个图：
![descriptor-example-Student](http://onexs3cnv.bkt.clouddn.com/descriptor-example-student.png)

# 应用场景
python中有个叫修饰器的东西，`property()`，它是描述符的简介版
```python
@property
def score(self):
	return self.__score

@score.setter
def score(self,score):
	if score < 0:
		raise ValueError('negative')
	self.__score = score

```
> calling propery() is a succinct way of building a data descriptor that triggers function calls upon access to an attribute
>from [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html#properties)

上面的写法`@property`使用到了[装饰器]()

1. 但是如果一个类里面有很多属性是相同的限制，比如学生的身高不能负数，成绩不能负数，体重不能负数，如果用`property`的话，那就多了很多重复的代码，每个属性都要像上面一样写一遍。这时候就可以考虑用写一个描述符类来“一统天下”了
2. 在之前说的对于已存在的属性，如果要对它们要进行限制，通过方法的话要找到每一处，这样很不方便，如果使用描述符只需要在类中加上`tall = Positive('tall')`像这样的语句就可以了，而且完全没有任何副作用！！

---

>If looked-up value is an object defining one of the descriptor methods, then python may override the default behavior and invoke the descriptor method instead.
>from [Descriptor HowTo Guide](https://docs.python.org/2/howto/descriptor.html#definition-and-introduction)

# 描述符的种类
> 学习也要遵循20/80定律，学到的20%就足够写程序了，先跑起来再来完善接下来的80%
> -- 尔东诚霍划夫斯基
描述符分`data descriptor`和`non-data descriptor`
两者之前的区别就是，后者只定义了`__get__`。也就是没有设置。





