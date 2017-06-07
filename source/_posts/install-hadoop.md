---
title: install hadoop
date: 2017-04-14 14:47:18
categories: bigdata
tags: [hadoop]
description: 记录安装hadoop 2.8.0
---

因为hadoop版本的问题，有些命令可能不一样。网上搜到的一些资料都会过时或与我现在安装的版本不兼容。
所以直接看[官方文档](http://hadoop.apache.org/docs/)

那安装其实涉及的就是单机和集群。特地在知乎上逛了一圈，得到的答案是，看目的吧，如果主要想学习mapreduce编程的，不要搭集群，不要搭集群，不要搭集群！！！因为目的是修炼内功，就没必要磨练工具了吧。但至少我觉得安装个工具如果都搞不定的话，那就不用混了。还是把重心放在mapreduce编程上吧

这里记录一个安装`single-node` hadoop的历程。

我mac上用的是`homebrew`包管理工具，所以我就直接`brew install hadoop`。好了，安装完成。

接下来的[文档](http://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-common/SingleCluster.html)里面都有。

主要记录一下几个点：

1. java的路径

因为是从官网下载的dmg直接安装的。java home的路径是`/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home`
如果是其他途径，比如`brew cask install java`的话，那应该会在`/usr/local/Cellar/java`中吧（我猜的），还有其他的肯定会有提示的。

2. 官网文档中的etc/hadoop？？在哪？

因为是通过`brew`安装的`hadoop`，所以`hadoop`都在`/usr/local/Cellar/hadoop`里面。文档直接说是`etc/hadop`，对应我机子上完整的路径是`/usr/local/Cellar/hadoop/2.8.0/libexec/etc`

同理`bin/hadoop`


中间什么配置`core-site.xml`等文件看文档就好了。**因为不同版本可能配置会不一样！！！所以还是看官方文档**


![hadoop-localhost](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-03%20at%2012.29.03%20AM.png)

![yarn](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-05%20at%207.22.24%20PM.png)



出来这个页面就可以了

3. hadoop fs -ls

在官网文档里面的命令是`hdfs dfs`，但其实是一样的
![hadoop](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-03%20at%2012.54.22%20AM.png)

但执行结果：
```bash
WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
ls: `.': No such file or directory
```
上面那个是因为编译的问题。hadoop官方是32位编译的好像。然后我机子是64位的。这个暂时不管。
下面这个报错其实是正常的。

`hadoop fs -ls`命令的语法完整其实是`hadoop fs -ls [path]`
而默认情况下，不用详细指定`[path]`,hadoop会认为是在hdfs中的`/home/[username]`，这个`[username]`就是用bash shell当前的用户替换。

![shell](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-03%20at%205.17.35%20AM.png)

比如在我机子上，hadoop回去找`/home/MMMMMCCLXXVII`，但这个路径不存在hdfs中。那这样，其实就是指定一个路径就可以了。

`hadoop fs -ls /` 它会自动获取计算出hdfs的根目录，然后显示

其实根据`core-site.xml`的配置

```
<configuration>
    <property>
	    <name>fs.defaultFS</name>
		<value>hdfs://localhost:9000</value>
	</property>
</configuration>
```

预想`hadoop fs -ls hdfs://localhost:9000/` 应该可以的。但是好像有问题。[TOdo]

然后用hadoop命令显示本地的文件。`hadoop fs -ls file:///`






借鉴的文档：

---
[【hadoop】ssh localhost 免密码登陆（图解）](http://blog.csdn.net/joe_007/article/details/8298814)
主要就是先要有sudo权限，如果没有用root账户的时候。
[How To Create a Sudo User on CentOS ](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-centos-quickstart)
这个`usermod`命令后，要重启终端。
> Have you logged in again after the usermod? IIRC, groups are only looked up when you log in (e.g. opened a new terminal window).

然后就是那两个命令，创建isa-pub.
主要就是要有权限。

---

关闭SElinux

[CentOS7中关闭selinux](http://www.centoscn.com/CentOS/config/2015/0618/5681.html)
这个设置后重启没用，还是开着的

