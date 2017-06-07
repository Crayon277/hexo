---
title: 重新编译hadoop过程终于到的问题
date: 2017-06-02 17:03:42
categories: bigdata
tags: [hadoop]


---


在macOS上直接执行命令`brew install hadoop`

然后执行hadoop命令的时候会出现
`WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable`
的警报。这是因为apcche hadoop 官网上下载的源文件是在32为的机器上编译的。所以当64位的机子在加载.so文件的时候会出错。基本上不影响使用hadoop(如果使用mahout做一些机器学习的任务时有可能会遇到麻烦，加载不成功，任务直接退出，所以还是有必要解决掉这个warn的)。

<!-- more -->


从网上下载的源文件中的`BUILDING.txt`看到如下的信息

```
Requirements:

* Unix System
* * JDK 1.7+
* * Maven 3.0 or later
* * Findbugs 1.3.9 (if running findbugs)
* * ProtocolBuffer 2.5.0
* * CMake 2.6 or newer (if compiling native code), must be 3.0 or newer on Mac
* * Zlib devel (if compiling native code)
* * openssl devel (if compiling native hadoop-pipes and to get the best HDFS encryption performance)
* * Linux FUSE (Filesystem in Userspace) version 2.6 or above (if compiling fuse_dfs)
* * Internet connection for first build (to fetch all Maven and Hadoop dependencies)
```
---

## java 路径问题

mac 下安装的路径见 [Mac下jdk的安装路径](http://blog.csdn.net/azhou_hui/article/details/46636769)


## protobuf的问题

因为用`brew insatll protobuf`命令来安装`protobuf`版本是最新的，而这里是要求`2.5.0`，所以要自己手动下载[protobuf2.5](https://github.com/google/protobuf/releases?after=v3.0.0-alpha-1)

### 解压

`tar xfvj tar xfvj protobuf-2.5.0.tar.bz2`

### 配置

进入目录后

`./configure CC=clang CXX=clang++ CXXFLAGS='-std=c++11 -stdlib=libc++ -O3 -g' LDFLAGS='-stdlib=libc++' LIBS="-lc++ -lc++abi"`

### make
`make -j 4`
`sudo make install`

完成！

## 关于zlib的

在Linux机子上的话就用各自的包管理工具安装。

```bash
yum -y install svn ncurses-devel gcc*
yum -y install lzo-devel zlib-devel autoconf automake libtool cmake openssl-devel
```
mac下执行
`xcode-select --install`就行了


## maven

修改安装目录下`conf/settings.xml`（因为maven使用的国外的reposity，国内有时无法访问，修改为国内镜像即可）
修改如下：
在<mirrors></mirrors>里添加
```
<mirror>
    <id>nexus-osc</id>
	<mirrorOf>*</mirrorOf>
	<name>Nexusosc</name>
	<url>http://maven.oschina.net/content/groups/public/</url>
</mirror>
```

上面最终是
```
<mirrors>
 <mirror>
  ...
 </mirror>
</mirrors>
```
同样在<profiles></profiles>内新添加

```
<profile>
       <id>jdk-1.8</id>
       <activation>
         <jdk>1.8</jdk>
       </activation>
       <repositories>
         <repository>
           <id>nexus</id>
           <name>local private nexus</name>
           <url>http://maven.oschina.net/content/groups/public/</url>
           <releases>
             <enabled>true</enabled>
           </releases>
           <snapshots>
             <enabled>false</enabled>
           </snapshots>
         </repository>
       </repositories>
       <pluginRepositories>
         <pluginRepository>
           <id>nexus</id>
          <name>local private nexus</name>
           <url>http://maven.oschina.net/content/groups/public/</url>
           <releases>
             <enabled>true</enabled>
           </releases>
           <snapshots>
             <enabled>false</enabled>
           </snapshots>
         </pluginRepository>
       </pluginRepositories>
     </profile>
```

But！！！在我的机子上有问题，还是保持原样就行了。因为后面出现了一个问题，所以以为这里是一个症状，排除法么。但如果有谁是因为镜像下载问题的话，估计是这个的问题。还有这里的国内镜像，`maven.oschian.net`，【todo】再去找找其他镜像的地址。
![maven](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-02%20at%207.16.06%20PM.png)



# 出现的问题

```bash
....
[INFO] Apache Hadoop Auth ................................. SUCCESS [  3.375 s]
[INFO] Apache Hadoop Auth Examples ........................ SUCCESS [  2.518 s]
[INFO] Apache Hadoop Common ............................... FAILURE [  4.272 s]
[INFO] Apache Hadoop NFS .................................. SKIPPED
[INFO] Apache Hadoop KMS .................................. SKIPPED
....
```

可以看到 hadoop common 编译失败

报错：

```bash
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 21.337 s
[INFO] Finished at: 2017-06-03T11:20:12+08:00
[INFO] Final Memory: 73M/725M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-antrun-plugin:1.7:run (make) on project hadoop-common: An Ant BuildException has occured: exec returned: 2
[ERROR] around Ant part ...<exec failonerror="true" dir="/Users/Crayon_277/Develop/Project/hadoop/hadoop-2.8.0-src/hadoop-common-project/hadoop-common/target/native" executable="make">... @ 7:160 in /Users/Crayon_277/Develop/Project/hadoop/hadoop-2.8.0-src/hadoop-common-project/hadoop-common/target/antrun/build-main.xml
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <goals> -rf :hadoop-common
```






链接文章：

- [Hadoop “Unable to load native-hadoop library for your platform” warning](https://stackoverflow.com/questions/19943766/hadoop-unable-to-load-native-hadoop-library-for-your-platform-warning)
- [Compile Apache Hadoop on Linux (fix warning: Unable to load native-hadoop library)](http://www.ercoppa.org/posts/how-to-compile-apache-hadoop-on-ubuntu-linux.html)
-
