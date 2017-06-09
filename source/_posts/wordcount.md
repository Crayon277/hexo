---
title: hadoop wordcount in python
date: 2017-06-08 22:28:34
categories: bigdata
tags: [hadoop,mapreduce,python]
description: Hadoop Streaming是Hadoop提供的一个编程工具，它允许用户使用任何可执行文件或者脚本文件作为Mapper和Reducer

---

因为不会java，暂时用自己熟悉的python来写mapreduce程序放在hadoop上跑。mapreduce只是一个编程思想，不局限于语言。

---

# hadoop streaming

> both the mapper and the reducer are executables that read the input from stdin (line by line) and emit the output to stdout. The utility will create a Map/Reduce job, submit the job to an appropriate cluster, and monitor the progress of the job until it completes.

官网的解释，也就是说，这个可执行文件或脚本里面，只要从stdin标准输入读入数据，然后进行内部的分词处理，输出到stdout，就行了，streaming会创建mapreduce的作业，发送给各个tasktracker，同时监控整个作业的执行过程。

## 用法

```bash
hadoop jar hadoop-streaming-2.8.0.jar \
  -input myInputDirs \
  -output myOutputDir \
  -mapper /bin/cat \
  -reducer /usr/bin/wc
```


官网给出的，但在机子上首先需要找到hadoop-streaming的jar文件，路径跟官网的不一样。

![streaming](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2011.09.41%20PM.png)
我的路径是：`./share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar`

# 测试数据

![data](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2010.47.18%20PM.png)


# map阶段：

```python
import sys

for line in sys.stdin:
    line = line.strip()
    keys = line.split()
    for key in keys:
        value = 1
        print('{0}\t{1}'.format(key,value))
```

python从stdin标准输入中读取每行数据, 然后将词切分，然后输入格式为`<key,value>`的形式，因为在map阶段，value都是1

本地测试结果：

![test-map](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2010.52.19%20PM.png)



# reduce阶段：

```python
import sys

last_key = None
running_total = 0

for input_line in sys.stdin:
    input_line = input_line.strip()

    this_key, value = input_line.split("\t",1)
    value = int(value)

    if last_key == this_key:
        running_total += value
    else:
        if last_key: #进入新的一组会进入这条语句，last_key初始是None，一开始不会打印
            print("{0}\t{1}".format(last_key,running_total))

        running_total = value
        last_key = this_key

if last_key == this_key: #最后一组输出
    print("{0}\t{1}".format(last_key,running_total))
```

本地测试：
![test-reduce](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2010.56.42%20PM.png)

有问题！怎么没有把相同的归在一起，其实这个程序如果按照map的输出当作输入执行结果就是这样的。因为`last_key`和`this_key`不停在变，因为map的输出哪怕没有两行是相同的key。那其实这里就涉及mapreduce的机制了，map阶段完成由输入数据到单词切分的工作，还有**`shuffle`**阶段，这个阶段完成相同的单词的聚集和分发工作，__这个过程是mapreduce的默认过程，不用具体配置__,也就是map和reduce的中间环节会把相同的给收集起来再进行reduce，如果在本地测试应该是这样的：

![test_reduce2](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2011.03.25%20PM.png)

用`sort`命令将相同的放在了一起，就模拟了把相同单词的聚集工作。

- [] ？有个疑问就是：相同的单词聚集在一起是分发给一个节点么，也就是不同节点计算着不同的单词，可能有节点计算好几个不同的单词，但问题是，是不是一个相同的所有单词都是在一个节点上reduce，如果不是，因为相同的单词被分了几份reduce了，那岂不是还要再reduce，总归要合并的，那这步在哪个节点上，由谁控制？


# hadoop 上测试

用`file:///`放在本地看

`hadoop jar ../hadoop-2.8.0/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar -input file:///Users/Crayon_277/Develop/Project/hadoop/wordcount/testfile* -output file:///Users/Crayon_277/Develop/Project/hadoop/wordcount/output2 -mapper mapper.py -reducer reducer.py`


![1](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2011.19.07%20PM.png)
![2](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2011.21.23%20PM.png)
![3](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-08%20at%2011.21.37%20PM.png)

注：以上在伪分布集群下测试的。

## mapreduce framework

运行hadoop程序给出的INFO，可以看到
```bash
	Map-Reduce Framework
		Map input records=2
		Map output records=16
		Map output bytes=109
		Map output materialized bytes=153
		Input split bytes=234
		Combine input records=0
		Combine output records=0
		Reduce input groups=12
		Reduce shuffle bytes=153
		Reduce input records=16
		Reduce output records=12
		Spilled Records=32
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=0
		Total committed heap usage (bytes)=1160773632

```

`Map input records=2` 这是说明有两个文件输入
`Map output records=16`数了一下`mapper.py`程序的输出，就是16个
然后可以看到`Reduce input groups=12`应该就是说明了`shuffle`的工作收集相同的单词，但`Reduce input records=16`这个16应该指的的总的还是16个，不是按**单词组**来看。
`Shuffled Maps=2` 我本来觉得是代表了有2种单词是有相同的，收集在一起了。但不是，因为其实在这个案例上是有4种是单词是有重复的。[Todo]

贴个流程图：

![mapreduceprogram](https://i.stack.imgur.com/ToZS9.png)

# 总结
其实应该有5个阶段：
- map phase
> The map phase is done by mappers. Mappers run on unsorted input key/values pairs. Each mapper emits zero, one, or multiple output key/value pairs for each input key/value pairs.

- combine phase
>The combine phase is done by combiners. The combiner should combine key/value pairs with the same key. Each combiner may run zero, once, or multiple times.

- shuffle and sort phase
>The shuffle and sort phase is done by the framework. Data from all mappers are grouped by the key, split among reducers and sorted by the key. Each reducer obtains all values associated with the same key. The programmer may supply custom compare functions for sorting and a partitioner for data split.

- partitioner
>The partitioner decides which reducer will get a particular key value pair.

- reducer
>The reducer obtains sorted key/[values list] pairs, sorted by the key. The value list contains all values with the same key produced by mappers. Each reducer emits zero, one or multiple output key/value pairs for each input key/value pair.
参考：
[What is the purpose of shuffling and sorting phase in the reducer in Map Reduce Programming?](https://stackoverflow.com/questions/22141631/what-is-the-purpose-of-shuffling-and-sorting-phase-in-the-reducer-in-map-reduce)

因为combiner操作是有风险的，使用它的原则是combiner的输入不会影响到reduce计算的最终输入，例如：如果计算只是求总数，最大值，最小值可以使用combiner，但是做平均值计算使用combiner的话，最终的reduce计算结果就会出错。这个例子统计词频，同样也不能combine，因为会遗失数据了。
