---
title: understanding MRO
date: 2017-03-13 17:28:31
categories: python
tags: [python,mro,python-object]

---

其实我一直觉得遇到什么障碍再去学什么是效率比较高的，这时候是带着问题去解决问题，比起干看，没有与实际相结合，要有用多了。所以等你真正遇到这个问题了，再来看看。** 这个`MRO`是理解`super`方法的前序 **,以下考虑的都是多重继承，单重继承讨论这个就没什么价值了。

# Method Resolution Order

> In computing, the C3 superclass linearization is an algorithm used primarily to obtain the order in which methods should be inherited (the "linearization") in the presence of multiple inheritance, and is often termed Method Resolution Order (MRO)
> from wikipedia -- [C3 linearization](https://en.wikipedia.org/wiki/C3_linearization)

这里引进这个概念。因为在继承中，会有子类继承父类当中的一些元素或方法，但是在多重继承中，到底是哪一个呢？这里就涉及到了`MRO`，方法解释顺序。可以想像一个列表，里面是继承关系的顺序，当调用子类的方法，或访问子类的元素的时候，就按照这个顺序依次的查找。

```python
class A(object):
	pass
class B(object):
	pass
class C(B):
	pass
class D(A,B,C):
	pass
```
你可以试一下，这个`D`类是定义不了的，会报错
```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Error when calling the metaclass bases
  Cannot create a consistent method resolution
order (MRO) for bases object, B, C
```
这里是因为破坏了`MRO`的一个(`monotomic`)单调性规定：
> if C1 precedes C2 in the linearization of C, then C1 precedes C2 in the linearization of any subclass of C.

通过C3算法得出的`MRO`就可以满足上面的这个要求

# C3 linearization

先定义几个符号表示：
`C1C2....CN` 表示一个[C1,C2,C3....CN]的解决顺序列表，在这样的一个列表中，`head`是`C1`，**其余的**都叫做`tail`。
注意：是从C2到最后都算tail.
`C+(C1C2...CN) = CC1C2...CN` 表示`[C] + [C1,C2...CN]`
`L[C]`表示`linearization of class C`，规定`L[O] = O`,`O`表示`object`

算法可以描述为一个递归的过程：
> the linearization of C is the Sum of C plus the merge of the linearizations of the parents and the list of the parents.
> `L[C(B1B2...BN)] = C + merge(L[B1],...L[BN],B1...BN)`
顺序很重要，一一对应的。

merge 算法描述为(原文)：
> take the head of the first list, i.e L[B1][0]; if this head is not in the tail of any of the other lists, then add it to the linearization of C and remove it from the lists in the merge, otherwise look at the head of the next list and take it. if it is a good head, then report the operation until all the class are removed or it is impossible to find good heads. If fail, python will refuse to create the class C and will raise an exception.

## 没看懂直接看例子。

![example-class-inherit](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-30%20at%207.18.59%20PM.png)

写出各个的`linearization`（这个翻译成啥我也不知道）
```python
L[O] = O
L[E] = EO
L[D] = DO
L[F] = FO
L[B] = B + merge(L[D],L[E],DE)
     = B + merge(DO,EO,DE)
```
这里是要`merge`3个`list`，`DO`,`EO`,`DE`，从第一个`DO`开始，它的`head`是`D`，然后看`D`是否出现在其他`list`的`tail`中中，注意`tail`是指除了`head`其余的所有。比如有一个`list`是`ADCBEF`,那`D`出现在第2个位置也算是在`tail`中，而不是在最后一个位置才算是`tail`。也就是说只有`D`出现在其他`list`首位置的时候，或者就根本没有`D`，这个`D`算是一个`good head`，然后将`D`加入`B`的linearization中，如果`D`不满足上面的条件，那么顺推到下一个`list` `EO`中的`E`，如果再不满足，继续顺推，都不满足的话就`raise an exception`。

```python
L[B] = B + merge(L[D],L[E],DE)
     = B + merge(DO,EO,DE)
	 = B + D + merge(O,EO,E) #再从第一个list O 开始去第一个元素O，但O不满足，出现在了第二个EO的tail中，顺延
	 = B + D + E + merge(O,O)
	 = B + D + E + O
	 = BDEO
```

```python
L[C] = C + merge(DO,FO,DF)
	 = C + D + merge(O,FO,F)
	 = C + D + F + merge(O,O)
	 = CDFO
```
```python
L[A] = A + merge(L[B],L[C],BC)
	 = A + merge(BDEO,CDFO,BC)
	 = A + B + merge(DEO,CDFO,C)
	 = A + B + C + merge(DEO,DFO)
	 = A + B + C + D + merge(EO,FO)
	 = A + B + C + D + E + merge(O,FO)
	 = A + B + C + D + E + F + merge(O,O)
	 = A + B + C + D + E + F + O
	 = ABCDEFO
```
---
## 另一个例子-- 不能生成mro

![bad-example](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-30%20at%207.39.09%20PM.png)

```python
L[O] = O
L[X] = XO
L[Y] = YO
L[A] = AXYO 
L[B] = BYXO #这两个其实也应该通过上面那个merge算法算出来的，只不过这里一眼就能看出来
```
关键看类C
```python
L[C] = C + merge(AXYO,BYXO,AB)
	 = C + A + merge(XYO,BYXO,B)
	 = C + A + B + merge(XYO,YXO)
```
到了这里就做不下去了，这里`XYO`,`YXO`，不管第一个`X`还是第二个的`Y`，都不行！！
> X is in the tail of YXO whereas Y is in the tail of XYO
因此算法结束.`raise an error refuese to create class C`

# 快速判别能否生成MRO的方法
以下来自 [python Attributes and Methods](http://www.cafepy.com/article/python_attributes_and_methods/python_attributes_and_methods.html)
![simple hierarchy](http://www.cafepy.com/article/python_attributes_and_methods/images/simple_hierarchy.png)
现在要定义一个新的类`class N(A,B,C)` 
![game abacus style beads](http://www.cafepy.com/article/python_attributes_and_methods/images/beads_on_strings.png)
画的稍微歪了，第一排全是`O`，那ok，`result`中也生成`O`放在顶部，第二排，`BBC`，不一样，要全部一样才能放在最后的`result`中，所以这个是失败的。

如果将类`N`的定义改为`class N(A,C,B)`
![solved-beads on strings](http://www.cafepy.com/article/python_attributes_and_methods/images/beads_on_strings_solved.png)

----

出处：
1. [The Python 2.3 Method Resolution Order](https://www.python.org/download/releases/2.3/mro/)
2. [python Attributes and Methods](http://www.cafepy.com/article/python_attributes_and_methods/python_attributes_and_methods.html)
