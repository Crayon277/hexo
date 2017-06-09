---
title: hadoop 相关数据的规约mapreduce程序 in python
date: 2017-06-09 13:07:57
categories: bigdata
tags: [hadoop,mapreduce]
description: 一个电视台有多个节目，一个节目有收看的观众，那电视台的有多少观众？

---


# 生成数据

```python
import sys

chans   = ['ABC','DEF','CNO','NOX','YES','CAB','BAT','MAN','ZOO','XYZ','BOB']
sh1 =['Hot','Almost','Hourly','PostModern','Baked','Dumb','Cold','Surreal','Loud']
sh2 =['News','Show','Cooking','Sports','Games','Talking','Talking']
vwr =range(17,1053)

chvnm=sys.argv[1]  #get number argument, if its n, do numbers not channels,

lch=len(chans)
lsh1=len(sh1)
lsh2=len(sh2)
lvwr=len(vwr)
ci=1
s1=2
s2=3
vwi=4
ri=int(sys.argv[3])
for i in range(0,int(sys.argv[2])):  #arg 2 is the number of lines to output

    if chvnm=='n':  #no numuber
        print('{0}_{1},{2}'.format(sh1[s1],sh2[s2],chans[ci]))
    else:
        print('{0}_{1},{2}'.format(sh1[s1],sh2[s2],vwr[vwi]))
    ci=(5*ci+ri) % lch
    s1=(4*s1+ri) % lsh1
    s2=(3*s1+ri+i) % lsh2
    vwi=(2*vwi+ri+i) % lvwr

    if (vwi==4): vwi=5
```

然后执行：
```bash
python make_join2data.py y 1000 13 > num1.txt
python make_join2data.py y 2000 17 > num2.txt
python make_join2data.py y 3000 19 > num3.txt
python make_join2data.py n 100  23 > chan1.txt
python make_join2data.py n 200  19 > chan2.txt
python make_join2data.py n 300  37 > chan3.txt
```

可以查看数据：
![dat](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%201.14.03%20PM.png)

# 问题
然后在上面比如`Hourly_Talking,922`这些表明是有922个观众在观看`Hourly_Takling`这个节目。`Almost_Show,ABC`表明是`ABC`电视台下有`Almost_Show`这个节目，然后现在要计算`ABC`电视台的收视情况

# map

这里主要就是要筛选出`ABC`电视台

```python
import sys
import re

pat = re.compile(r'\d+')

for line in sys.stdin:
    if 'ABC' in line or len(pat.findall(line)):
        print '{}\t{}'.format(*(line.strip().split(',')))
```

![resu](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%201.35.54%20PM.png)

因为观众数的那些还不知道和那些电视台相关，所以这些数据要保留

# reduce

```python
import sys

line_count     = 0      
old_key        = None 
viewer_count   = 0       
abc_found      = False   

for line in sys.stdin:
    line       = line.strip()       
    key_value  = line.split('\t')   
    key        = key_value[0]       
    value      = key_value[1]       

    line_count = line_count + 1

    if key == old_key or line_count == 1:
        if value == "ABC":
            abc_found = True
        else:
            viewer_count = viewer_count + int(value)

    if key != old_key and line_count: #这是进入下一组了
        if abc_found == True: #只有在是ABC的才打印出来
            print( '%s %s' % (old_key, viewer_count) )
        old_key      = key  #下一个
        if value.isdigit():
            viewer_count = int(value)
        abc_found    = False

print '%s %s' % (key, viewer_count)

```

在reduce阶段的时候，shuffle已sort了，`<key,value>`的value要么是'ABC'，要么是数字，如果是数字的话累加，而且，因为是sort过的，然后一定是这样的形式：
```
d,12
d,23
d,abc
```
**所以相关的点就在`key`都是`d`的value累加完后，势必会读到`d`的value是哪个电视台的，如果是'ABC'的话，就可以输出了。**

# 本地测试

![local test](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%201.54.54%20PM.png)

# hadoop 集群测试
![1](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%202.00.15%20PM.png)
![2](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%202.00.30%20PM.png)
![3](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-09%20at%202.01.47%20PM.png)

与本地测试的结果一样






