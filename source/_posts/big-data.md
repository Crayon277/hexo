---
title: Intro to hadoop and MapReduce -- Big Data(一)
date: 2017-04-04 20:26:09
categories: bigdata
tags: [hadoop,mapreduce,udacity]

---

# Definition of Big Data
可能有些人认为几个`terebytes`的数据量是大数据，但这个量不是标准的，所以一个合理的定义是
> It's data that's too big to be processed on a single machine.

## Quiz: Chanllenges with Big Data
~~- most data is worthless~~
- data is created fast
- data from different sources in various formats

most data is not worthless, but actually does have a lot of value.

# The 3 V's of big data

## Volume
总结：量大。需要考虑那些能提供有用信息
> But in order to store it, you’ll need a way to scale your storage capacity up to massive volume. Hadoop, which stores data in a distributed way across multiple machines, does that

## Variety
就是说我们如果用像MySQL,Oracle这种数据库，数据必须要适合他们的格式，但是现在我们处理的数据很大部分都是`unstructured`或者是`semi-structured`.
比方说现在打客服热线不都有一个提示说是会录音，一种存储是语音识别成文字保存起来，另一种是直接存储成mp3格式然后让相应的软件解码如果后面要用的话。那hadoop不管你的数据是什么样的格式，
> you can just store the data in its raw format, and manipulate and reformat it later.

### example
> Sometimes the most unlikely data can be extremely useful and lead to savings due to better planning. 

![optimize choice](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%209.39.47%20PM.png)

比方说现在要通知附近的货车到中心取货，基于位置的系统就会通知最近的车辆过来。但往往，这个最近，不是最佳的选择。也许那里有交通堵塞，也许最近的车辆过来需要过羊肠小道，那里的路比较难走，也许是要绕一大圈才能到中心。更需要考虑的是，这辆车上也许没有足够的空间了，这辆车没有油了。所以以下都是需要考虑的

- Current GPS location fromi all trucks
- Current itineraries for all trucks
- Current traffic speed in related areas as reported by services such as waze
- Current load of trucks by volume and weight
- Fuel efficiency of the different vehicles

> The world we live in is extremely complex, and there are a lot of variables to consider that you can tweak to get large benefits.
>
## Velocity
实时更新？？
> If we can’t store it as it arrives, we’ll end up discarding some of it, and that’s what we absolutely want to avoid.


# history of hadoop
来自hadoop 之父 Doug Cutting
> So, let me tell you how Hadoop came to be. About ten years ago in around 2003, I was working on an Open Source web search engine called Nutch, and we knew it needed to be something very scalable, because the Web was you know, billions of pages. terabytes, petabytes, of data, that we needed to be able to process, and we set about doing the best job we could and it was tough. We got things up and running on four or five machines, not very well, and around that time Google published some papers about how they were doing things internally. Published a paper about their distributed file system, TFS. and about their processing, framework, MapReduce. So my partner and I, at the time, in this project, Mike Cafarella. said about trying to reimplement these in Open Source. So that more people could use them than just folks at Google. Took us a couple of years, and we had Nutch up and running on, instead of four or five machines, on, 20 to 40 machines. It wasn't perfect, it wasn't totally reliable, but it worked. And we realize that to get it to the point where it was scaled to thousands of machines, and be as bullet proof as it needed to be, would take more than just the two of us, working part time.
>
> Around that time, Yahoo approached me and said they were interested in investing in this. So I went to work for Yahoo in January of 2006. First thing I did there, was, we took the parts of Nutch that were a distributed computing platform, and put them into a separate project. A new project christened Hadoop. Over the next couple years, with, Yahoo's help, and the help of others, we took Hadoop, and really got it to the point where it did scale to petabytes, and running on thousands of processors. And doing so quite reliably. 
>
> It spread to lots of companies, and mostly in the Internet sector, and became quite a success. after that, we, we started to see a bunch of other projects grow up around it. And Hadoop's grown to be the kernel of a, which, pretty much an operating system for big data. We've got tools that, allow you to, more easily do, MapReduce programming, so, you can develop using SQL or a data flow language called Pig. And we've also got the beginnings of higher­level tools. We've got interactive SQL with Impala. We've got Search. and so we're really seeing this develop to being a general purpose platform for data processing. that scale's much better and that it is much more flexible than anything that's, that's, else is out there.

# hadoop cluster
![cluster](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%2010.04.35%20PM.png)
hadoop存储数据的方法是一个分布式的文件系统叫做`HDFS`。处理数据是通过`MapReduce`。
核心思想就是将数据分块，然后在集群中存储，也就是各个计算机搭建的一个网络吧。那这样的好处就是我们不用从中心取数据然后再操作，我们直接在集群中就地处理数据，后续还可以继续扩大集群的规模

# hadoop Ecosystem
![ecosystem](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-04%20at%2010.31.42%20PM.png)
> Core hadoop consists of HDFS and MapReduce
hadoop的生态系统。以hadoop为核心的，打造的周边产品，主要的目的就是降低使用hadoop的难度和门槛。
比如编写`MapReduce`的程序不是一件容易的事，有些没有编程经验的就可以用`Pig`，`Hive`，这种类似SQL语句来操作数据，但这两个都是将语句翻译为`MapReduce`然后再到集群上执行。
因为`Hive`和`Pig`它们本质上还是`MapReduce`的工作量，所以花费的时间可能更多。所以另一个开源项目`Impala`，它是允许直接用`SQL`语句来操作数据，不用经过`MapReduce`（具体现在我也不懂），所以这样就很快了
其他的也就类似了。

Cloudera hadoop版的其实就是把这些都给你打包好了，你不用在一个一个去弄了。

核心还是hadoop的`HDFS`和`MapReduce`

