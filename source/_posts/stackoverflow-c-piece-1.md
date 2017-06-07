---
title: project of stackoverflow - C Piece (一)
date: 2017-05-27 18:55:09
categories: stackoverflow
tags: [c,c-piece,stackoverflow]
description: 搬运stackoverflow有关C的知识，即练英语，又可以从他人的困惑中学到新东西。

---

# C中的操作符优先级 [precedence of operator in c](https://stackoverflow.com/questions/25057097/precedence-of-operator-in-c)

我是一个变成新手，现在我正在学有关C操作符优先级的部分。我尝试着想要分析下面给出的代码

```C
     #include<stdio.h>
     int main()
     {
        int x, y, z;
        x = y = z= -1;
       z = ++x&&++y&&++z;
       printf("x = %d y = %d z = %d", x, y ,z);
     }
```
在学了操作符的优先级后，我知道一元操作符(unary operator)有更高的优先级，所以在上面的代码中：
` z = ++0&&++0&&++0;`
所以`x`,`y`,`z`的值是0，对吧？但是编译执行后，结果是`x = 0 y = -1 z = 0`
有人能帮我解决这个问题么？

---

得票2:

这个表达式：
`z = ++x&&++y&&++z;`

其实和下面这个表达式是等价的：

`z = ( ++x && ++y ) && ++z;`

根据标准C：
> 4. 和二进制位操作&不一样，&&操作是从左向右结合计算。如果第二个操作数北极算了，那就说明在第一个操作数和第二个操作数之间存在一个**sequence point**。如果第一个操作数比较等于0，那么第二个操作数不会被计算。

所以首先`++x`被计算。它等于0。所以`++y`不会被计算。表达式：
`(++x && ++y)`
结果是0。因为它等于0，所以表达式`(++x && ++y) && ++z`中的子表达式`++z`不会被计算。
所以`z`会被赋值整个表达式的值，那就是0。

这里至少没有任何未定义的行为(undefined behaviour) 因为表达式`++z`不会被计算。

所以你会得到 x == 0, y == -1, 和 z == 0 （这是因为赋值语句）

---

# [Undefined behavior and sequence points](https://stackoverflow.com/questions/4176328/undefined-behavior-and-sequence-points)

tag: c++ , undefined-behavior, c++.fag, sequence-points

什么是“序列点”(sequence points)? (不知道这么翻译对不对)
未定义行为和序列点的关系是什么？

我经常使用像`a[++i] = i`这种有趣却复杂的表达式，我也感觉不错，为什么要停止使用这些呢？

如果你已经阅读到这里了，确保访问下面的问题[Undefined behavior and sequence points reloaded.](https://stackoverflow.com/questions/4638364)

---

556票的回答：

C++98 和 C++03

这个回答是准备给C++旧标准的。C++11和C++14标准版本没有正式的包含"[sequence points]"这个说法；运算反而是(sequence before) 或 (unsequenced) 或 (indeterminately sequenced) 。网络效应（net effect)？基本上一致，但是术语不一样而已。

---
不承诺： 好吧，这个回答有点长，所以在阅读的时候需要一点耐心，如果你已经知道这些东西了，再次阅读不会让你疯狂的。

前提： 需要[C++ standard]()的一点基础知识

---

什么是sequence points?

标准中说到：

> At certain specified points in the execution sequence called sequence points, all side effects of previous evaluations shall be complete and no side effects of subsequent evaluations shall have taken place. (§1.9/7)

[TODO]
