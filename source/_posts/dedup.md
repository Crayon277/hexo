---
title: hadoop mapreduce -- 数据去重(python)
date: 2017-06-09 08:05:32
categories: bigdata
tags: [hadoop,mapreduce]
description: 打个比方，桌上有10个苹果，之前的编程思想是从上往下看，mapreduce的编程思想是贴着桌面，平行透视的看。combiner阶段也是可以用于这个场景的。而且combiner是在每个运行map任务的节点上运行。是一个迷你的reduce过程

---

# 问题描述
就用mapreduce的思想来将重复的数据剔除

# 测试数据
自己随便弄
![testfile1](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.18.29%20AM.png)
![testfile2](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.18.37%20AM.png)

# map

```python
import sys

for line in sys.stdin:
    line = line.strip()

    print "{0}\t{1}".format(line,1)
```

这个比wordcount程序简单多了。其实在这个例子中，`<key,value>`的value没有什么用，最后不用输出。

# reduce

```python
import sys

last_key = None

for line in sys.stdin:
    this_key = line.split('\t')[0].strip()
    if this_key == last_key:
        pass
    else:
        if last_key:
            #print this_key #错误！！！
            print last_key #this_key每一轮都更新，当不一样了的时候，要将上一轮的key输出
        last_key = this_key
print this_key

```
在`this_key == last_key`条件满足的时候，跟wordcount不一样的是，这里什么都不用做，比较wordcount程序这里是要累加的。但其实reduce这一步只要将相同的输出一个就行了。

# 本地测试

命令: `python mapper.py < testfile* | sort | python reducer.py`
![localtest](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.51.38%20AM.png)

# hadoop测试

![ha](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.58.26%20AM.png)
![doop](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.58.40%20AM.png)
![result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%208.58.17%20AM.png)

看到结果也是一样的。

# combine

上面结果中
```bash
		Combine input records=0
		Combine output records=0
```
了解了一下combine的过程，我一开始疑惑combine到底在哪个阶段，他的输入是什么（输入的是sort前还是sort后），是在哪个节点运行的。

参考：

- [Which runs first, Combiner or Partitioner in a MapReduce Job](https://stackoverflow.com/questions/35195101/which-runs-first-combiner-or-partitioner-in-a-mapreduce-job)

-[] combine阶段在shuffle阶段之前，因为shuffle阶段做的是copy和sort，那么表示的就是combine阶段的时候是没有sort过的数据输入。这很重要。如果是sort过的话的，那么combine的程序就跟reducer的程序一样。只是在单个节点上，可以看作预处理的reduce。那在旧的mapreduce架构shuflle在jobtracker上运行，combine在tasktracker上执行。那在YARN架构下，combine应该在nodemanager，shuffle在resourcemanager。[Todo] 不确定

![combine](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%209.29.39%20AM.png)

**combine只是处理一个节点中的输出，而不能享受像reduce一样的输入（经过了shuffle阶段的数据）,这个非常关键**

## 实验combine带来的优化能力

先用wordcount测试，词频统计是一个可以展示combine用处的例子。词频统计程序为每一个它看到的词生成了一个（word，1）键值对。所以如果在同一个文档内“cat”出现了3次，（”cat”，1）键值对会被生成3次，这些键值对会被送到Reducer那里。通过使用Combiner，这些键值对可以被压缩为一个送往Reducer的键值对（”cat”，3）。现在每一个节点针对每一个词只会发送一个值到reducer，大大减少了shuffle过程所需要的带宽并加速了作业的执行。

### 测试数据
网上下载了两个英文小说
![entxt](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%209.54.51%20AM.png)

一个是165k，另一个是446k

---

**不使用 combine ：**

命令: `hadoop jar ../../hadoop-2.8.0/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar -input file:///Users/Crayon_277/Develop/Project/hadoop/mapreduce-program/wordcount/f*.txt -output file:///Users/Crayon_277/Develop/Project/hadoop/mapreduce-program/wordcount/output -mapper mapper.py -reducer reducer.py`

结果：
![result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%209.54.20%20AM.png)

可以看到
```bash
		GC time elapsed (ms)=4
		Total committed heap usage (bytes)=1160773632
```

---

**使用了combine: **

命令：`hadoop jar ../../hadoop-2.8.0/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar -input file:///Users/Crayon_277/Develop/Project/hadoop/mapreduce-program/wordcount/f*.txt -output file:///Users/Crayon_277/Develop/Project/hadoop/mapreduce-program/wordcount/output -mapper mapper.py -reducer reducer.py -combiner reducer.py`

combine的程序用回reducer.py的程序

![usecombine](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%2010.06.01%20AM.png)


```bash
		GC time elapsed (ms)=3
		Total committed heap usage (bytes)=1159200768
```

---

可以对比出
```bash
		GC time elapsed (ms)=4
		Total committed heap usage (bytes)=1160773632
	
		GC time elapsed (ms)=3
		Total committed heap usage (bytes)=1159200768
```
是有优化的。时间上效率也有提升。

## combine不是所有的情景都适合

combiner操作是有风险的，使用它的原则是combiner的输入不会影响到reduce计算的最终输入，例如：如果计算只是求总数，最大值，最小值可以使用combiner，但是做平均值计算使用combiner的话，最终的reduce计算结果就会出错。

# 数据去重的例子中使用combine

```python
import sys

s = set() #集合

for line in sys.stdin:
    s.add(line.strip().split('\t')[0]) #取<key,value>中的value

for item in s:
    print "{0}\t{1}".format(item,0) # 0其实没有什么意义

```

我预想的是这个在每个节点上将map输出的东西，先筛选一遍，就是用集合的方法，然后再输出，但是！！

![wrong](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%2010.55.19%20AM.png)

结果有点问题，用的时间也多了

[Todo]不知道为啥？combine的输出格式也和map阶段的一样，但错误。

从结果上看，还有重复的数据，反推，说明有数据没有被sort到一起，因为从打印结果看到，相同的中间隔着一些，但是在reduce的程序，可以看出，如果是收集在一起的数据是只会打印一个的，说明shuffle没有起作用？？
