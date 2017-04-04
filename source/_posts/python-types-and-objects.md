---
title: python types and objects
date: 2016-12-03 08:02:26
categories: python
tags: [python,type,object]

---

[Python Types and Objects](http://www.cafepy.com/article/python_types_and_objects/python_types_and_objects.html)
这篇文章解释了：
- 什么是`<type 'type'>`和<type 'object'>
- 用户自定义的类和实例是怎么联系在一起的以及和内建类型的联系
- 什么是`metaclass`元类

<!-- more -->

# `type`和`object`
从之前的学习面向对象编程来看，我们可以通过继承来定义一个类，也可以查看一个对象属于哪个类。其实这就可以抽象出两种关系
![relationship](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%202.56.02%20PM.png)
图中虚线就是`type`，表示一个**对象**(又称‘实例’)的类型是尖头指向的那个
图中的实线是`base`，表示一个**类**的基类是尖头指向的那个
> the type and base(if exist) are important, coz they define special relationships an object with other objects.

因为在python中一切皆为对象，所以`base`到头了就是`object`，这个是在python中一切类的祖宗。
而因为python中一切皆为对象, 它就有类型，`object`也是一个对象，它的类型就是`type`，`type`本身也是一个对象，为了满足python这样的设定，它的类型就是它自己。**`type`既是一个对象，也是一个类**。就说我们自己定义了一个类
```python
>>> class A(object):
...     pass
...
>>> A.__bases__
(<type 'object'>,)
>>> A.__class__
<type 'type'>
```
他也有类型，就是`type`类型
> keep in mind that the types and bases of objects just other objects

既然像类也是一种"对象",那它是谁的对象？？答案就是`metaclass`，`type`就是`metaclass`。
先有鸡还是先有蛋？
![explain](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%202.42.19%20PM.png)
## 类和类型的统一
这个问题在知乎上有一个解答不错
> 旧式类的实现不够好，类是类，实例是实例，类的类型是classobj，实例的类型是instance，两者的联系只在于__class__，这和内置对象是不同的，int对象的类型就是int，同时int()返回的也是int类型的对象，内置对象和自定义对象不同就对代码统一实现带来很大困难。比如说有段代码输入一个对象，返回一个默认构造的同类型对象，本来应该写作type(obj)()，现在就必须写成：obj.__class__() if hasattr(obj, '__class__') else type(obj)()。如果想用自定义的类去替代一些系统内置类型，比如说自定义一个dictionary，这样的不一致就会出问题新式类之后自定义类和内置类型就一致了：1. 所有类型的类型都是type2. 所有类型调用的结果都是构造，返回这个类型的实例3. 所有类型都是object的子类这样就不再需要区分自定义类和类型了。实现这件事其实并不容易，理性上来想，type的基类是object，而object的类型是type，这是一个先有鸡还是先有蛋的问题。Python通过对这几个类的特殊处理实现了这样的逻辑。
>
> 作者：灵剑
> 链接：https://www.zhihu.com/question/38803693/answer/103128686
> 来源：知乎
> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

# 自定义类和内建类型
图片来自那个文章顶部那个链接,这篇文章写的很详细了
![python objects map](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%203.35.31%20PM.png)
>1. Dashed lines cross spacial boundaries (i.e. go from object to meta-object). Only exception is <type 'type'> (which is good, otherwise we would need another space to the left of it, and another, and another...).
>2. Solid lines do not cross space boundaries. Again, <type 'type'> -> <type 'object'> is an exception.
>3. Solid lines are not allowed in the rightmost space. These objects are too concrete to be subclassed.
>4. Dashed line arrow heads are not allowed rightmost space. These objects are too concrete to be instantiated.
>5. Left two spaces contain types. Rightmost space contains non-types.
>6. If we created a new object by subclassing <type 'type'> it would be in the leftmost space, and would also be both a subclass and instance of <type 'type'>.

## 两个对象
python中分`Type`对象和`Non-Type`对象，这个`Non-Type`不是一个正式的概念，只是这么称呼，这类对象，比如2，就是2，2怎么再派生？怎么再实例化，不行，所以是**too concrete**。怎么判断，只要`type(obj)`出来的是`<type 'type'>`就是`Type`对象，不然就是`Non-Type`对象
>- Type objects - can create instances, can be subclassed.
>- Non-type objects - cannot create instances, cannot be subclassed.
>- `objectname.__class__` exists for every object and points the type of the object.
>- `objectname.__bases__` exists for every type object and points the superclasses of the object. It is empty only for `<type 'object'>`.
>- Some non-type objects can be created using special Python syntax. For example, `[1, 2, 3]` creates an instance of `<type 'list'>`.

## 两个动作
两种关系对应两种动作可以生成两种对象。有可能是`Type`对象,也有可能是`Non-Type`对象。
两个动作就是`subclassing`和`instantiating`.
### subclassing
这个动作具体就是`class`语句,定义一个类，或者说定一个`type`，
> This means you can create a new object that is somewhat similar to existing type objects.

> To create a new object using subclassing, we use the class statement and specify the bases (and, optionally, the type) of the new object. This always creates a type object.

~~这段代码抽象代表的就是一个类~~

###  instantiating
这个动作就是实例化，由一个`type`实例化出对象，`type`相当于一个工厂的模型，具体就是通过`()`操作。
> To create a new object using instantiation, we use the call operator (()) on the type object we want to use. This may create a type or a non-type object, **depending on which type object was used**.

> This means you can create a new object that is an instance of the existing type object.

python中的内建类型是在启动python后生成的。比如
```python
>>> type(list)
<type 'type'>
>>> list.__bases__
(<type 'object'>,) # list是从object派生而来了
>>> ml = [1,2,3]
>>> type(ml)
<type 'list'>
```
如果问`[1,2,3]`是什么类型啊？列表类型啊。列表类型是什么类型啊？`type`类型啊。`type`类型是什么类型啊？`type`类型。。。当我们创建{'a':1,'b':2},(1,2)这种，是从`<type 'list'>`,`<type 'dict'>`实例化出来的，也就是相应的`type`，包括自定义。

# metaclass
很重要的一点就是，当我`class`语句定义了一个类，我就自动的有了一个`type`，其实也就是说`__class__`（新式类）
```python
class C(object):
	pass
```
`type(C)`就已经定了。它是根据所继承的父类的`type`延续下来的，因为`object`的类型是`type`所以
```python
>>>type(C)
<type 'type'>
```
那其实这样追溯下去，因为`object`类型是`type`类，所以所有的类都是`type`类。除了`Non-Type`对象的类型是相对应的类。所以那幅图的前面两列的虚线都指到`type`。
这里有一个问题就是它是由继承关系决定的，那如果是多重继承呢？是继承哪个？
```python
>>> class M1(type):
...     pass
...
>>> class M2(type):
...     pass
...
>>> class A(object):
...     __metaclass__ = M1
...
>>> class B(object):
...     __metaclass__ = M2
...
>>> type(A)
<class '__main__.M1'>
>>> type(B)
<class '__main__.M2'>
>>> class C(A,B):
...     pass
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  TypeError: Error when calling the metaclass bases
      metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
```
如果大家的`metaclass`都一样，那就没得说了，如果不一样，那么就会混乱，这时候要指定。什么时候会不一样呢？一般情况下都是`type`，除非自己定义`specialType`然后派生。但**建议是不要用这个特性**。

另一个问题就是，到底怎么自定义`specialType`？上面例子已经给出答案了。
```python
class C(object):
	__metaclass__ = specialType
```

# 隐式关系
图片来自文章顶部链接文章中的：
[![transitivity of relationships](http://www.cafepy.com/article/python_types_and_objects/images/relationships_transitivity.png)](http://www.cafepy.com/article/python_types_and_objects/python_types_and_objects.html)

`issubclass`问的是一个`class`是不是`subclass` of 另一个`class`。`class`和`class`之间的关系
`isinstance`问的是一个`object`是不是`instance` of 另一个`class`。`object`和`class`之间的关系

```python
>>> isinstance(type,type) #虚线，type指向自己 
True
>>> isinstance(type,object) #因为type是自身的实例，type又是object的子类，所以type是object的实例
True
>>> isinstance(object,object) #因为object是type的实例，type又是object的子类，所以object是object的实例
True
>>> isinstance(object,type) # 虚线
True
>>> issubclass(type,type) # A class is considered a subclass of itself
True
>>> issubclass(type,object) # 实线
True
>>> issubclass(object,object) # 任何类都是object的子类
True
>>> issubclass(object,type) # object在类的金字塔顶端，它上面就没人啦
False
```
> [A class is considered a subclass of itself](https://docs.python.org/2/library/functions.html#issubclass)


---
# Q&A
1. `class`,`object`,`instance`的关系
>An object is an instance of a class, and may be called a class instance or class object; instantiation is then also known as construction. Not all classes can be instantiated – abstract classes cannot be instantiated, while classes that can be instantiated are called concrete classes.

2. How does python really create a new object?
> Internally, when python creates a new object, it always uses a type and creates an instance of that object. Specifically it uses the __new__() and __init__() methods of the type. In a sense, the type serves as a factory that can churn out new objects, the type of these manufactured objects will be the type object used to create them. This is why every object has a type.

