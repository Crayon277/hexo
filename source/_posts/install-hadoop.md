---
title: install hadoop
date: 2017-04-14 14:47:18
categories: bigdata
tags: [hadoop]
description: 记录安装hadoop

---

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

