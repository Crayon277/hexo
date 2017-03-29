---
title: python name and values
date: 2017-03-29 21:54:00
categories: python
tags: python

---

阅读 [Facts and myths about Python names and values](https://nedbatchelder.com/text/names.html) 做的摘记
内容不是很深，只是这里面提到了一些需要注意的点。最主要还是`name`和`value`的区别
<!-- more -->

# Fact: Names have no type, values have no scope.

>Just as names have no type, values have no scope. When we say that a function has a local variable, we mean that the name is scoped to the function: you can't use the name outside the function, and when the function returns, the name is destroyed. But as we've seen, if the name's value has other references, it will live on beyond the function call. It is a local name, not a local value.

翻译：

就跟名字没有类型一样，数值是没有作用范围的。当我们说一个函数有局部变量的时候，我们只是说的是名字只在函数作用域中起作用而已，你不能在函数外使用这个名字，当函数返回的时候，这个名字也就摧毁了。但是，如果这个名字指向的数值还有其他引用，它就会继续生存下去，不管这个函数了。局部变量，而不是局部数值。

# Fact: Values can't be deleted, only names can.

> Python's memory management is so central to its behavior, not only do you not have to delete values, but there is no way to delete values. You may have seen the del statement:

```python
nums = [1, 2, 3]
del nums
```

> This does not delete the value nums, it deletes the name nums. The name is removed from its scope, and then the usual reference counting kicks in: if nums' value had only that one reference, then the value will be reclaimed. But if it had other references, then it will not.

# Fact: Assignment never copies data.

> Mutable means that the value has methods that can change the value in-place. Immutable means that the value can never change, instead when you think you are changing the value, you are really making new values from old ones.
>

比如：
```python
x = 3
y = x
```
`x`和`y`只是一起指向了`3`而已，并没有给`y`再来一个`3`。这里`x`,`y`是`name`，`3`是`value`
上面说到的`Mutable`是什么意思，也就是因为这个赋值不拷贝数据的特性，当`y`变了的时候，比如`y+=1`，那`x`还变不变？这里就要考虑到可变类型和不可变类型了

Immutable values:
1. numbers
2. strings
3. tuples 

Mutable values:
1. lists
2. dicts
3. user-defined objects

那在上面`y+=1`之后，其实是给`y`重新`reference`到了4

关于mutable的直接截图：

![list_mutate](http://onexs3cnv.bkt.clouddn.com/list_mutate_value.png)

---

# Fact: Python passes function arguments by assigning to them.

```python
def my_func(x,y)
	return x+y
print(my_func(8,9))
```

> The names x and y are local to the function, so when the function returns, those names go away. But if the values they refer to are still referenced by other names, the values live on.
>

**注意**，这里就出现`name`和`value`的区别了，可以这样理解，`value`就是一个实物，`name`只是这个实物的标签，我可以贴很多标签，而看到这个标签，我就联想到这个实物，实物可以有多个标签，一个标签只能对应一个实物。

```python
def augment_twice(a_list,val):
	a_list.append(val)
	a_list.append(val)

nums = [1,2,3]
augment_twice(nums, 4)
print(nums) #[1,2,3,4,4]
```

![before](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-29%20at%2010.23.49%20PM.png)
---
![after](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-29%20at%2010.23.55%20PM.png)
---

虚线框表示本地`name`在一个新的`frame`里面，而参数传递只是一种赋值操作，`a_list` “指向” `nums`指向的`value`,而`list`类型是可变数据类型，所以任何`name`对它的改变都是就地的，可以通过`id()`操作来查看是否改变了地址

另外一个程序

```python
def augment_twice_bad(a_list,val):
	a_list = a_list + [val,val]
nums = [1,2,3]
augment_twice_bad(nums,4)
print(nums) #[1,2,3]
```
这个跟上面的程序就不同在函数里面一个是用`.append()`来增加元素，一个则用加法然后赋值，赋值，赋值，重要的事情说三遍，这是个赋值操作，一旦出现赋值，就相当于等式左边的`name`**rebind**出现在等式右边的`value`

![bad_before](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-29%20at%2010.35.39%20PM.png)
---
![bad_after](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-03-29%20at%2010.35.45%20PM.png)


> It's really important to keep in mind the difference between mutating a value in place, and rebinding a name. augment_twice worked because it mutated the value passed in, so that mutation was available after the function returned. augment_twice_bad used an assignment to rebind a local name, so the changes weren't visible outside the function.
> 


# 其他的 facts, myths都知道了，上面的需要注意一下就可以了。过

