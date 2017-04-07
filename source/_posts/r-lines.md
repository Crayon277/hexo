---
title: 用R画出下面这样子的形式的图
date: 2017-04-07 13:35:06
categories: R
tags: [R-piece,R,plot]
description: 主要是plot, lines, text , points 四个函数的使用
photos:
- http://onexs3cnv.bkt.clouddn.com/Rplot-triangle.png
---

用到什么学什么

# plot的使用
官方的description
> Generic function for plotting of R objects. For more details about the graphical parameter arguments, see par.
>
> For simple scatter plots, plot.default will be used. However, there are plot methods for many R objects, including functions, data.frames, density objects, etc. Use methods(plot) and the documentation for these.
>
>plot(x, y, ...)

这里先用到plot的一个type参数
>what type of plot should be drawn. Possible types are
>
>"p" for points,
>
>"l" for lines,
>
>"b" for both,
>
>"c" for the lines part alone of "b",
>
>"o" for both ‘overplotted’,
>
>"h" for ‘histogram’ like (or ‘high-density’) vertical lines,
>
>"s" for stair steps,
>
>"S" for other steps, see ‘Details’ below,
>
>"n" for no plotting.

这里有个`"n"`的参数值可以选择，也就是什么都不会打印，先看个例子
```R
x <- seq(-pi,pi,length = 100)
plot(x,sin(x),type='p')
plot(x,sin(x),type='l')
plot(x,sin(x),type='n')
```
分别是这样色儿的
![points](http://onexs3cnv.bkt.clouddn.com/Rplot-sin.png)
![line](http://onexs3cnv.bkt.clouddn.com/Rplot-sin-line.png)
![none](http://onexs3cnv.bkt.clouddn.com/Rplot-sine-none.png)
看最后一个，也就是什么都没画。什么都没有有什么用！？
**存在即合理**，它可以用来弄一个画布，然后再在上面画其他图形

比如：
```R
> plot(c(0,10),c(0,10))
```
![with points](http://onexs3cnv.bkt.clouddn.com/Rplot-canvas-with-something.png)

这里`plot`的`x`,`y`参数是用向量指定的，`x`坐标的放一起，`y`坐标的放一起，其实坐标点是`(0,0)`,和`(10,10)`，在这两个坐标上，默认是画了两个小圆圈。但是如果我想要一个有坐标系的这样的一个画布，我就可以

```R
> plot(c(0,10),c(0,10),type='n')
```
![no points canvas](http://onexs3cnv.bkt.clouddn.com/Rplot-canvas-blank.png)

而这里`x`,`y`的作用就是撑开画布坐标系的大小，我如果`plot(c(0,50),c(0,50),type='n')`，那坐标系就变大了。

# lines
> A generic function taking coordinates given in various ways and joining the corresponding points with line segments.
> lines(x, ...)
>
> ## Default S3 method:
> lines(x, y = NULL, type = "l", ...)
>

就是根据像`plot`那样`x`,`y`解释的意思，将两点连起来，~~同时用`type`指定的样式画出这点线~~
这个说法有点不正确，好像是说`type`指定的是线的样式，比如实线，虚线，不是的。`lty`这个参数才是指定“线样式的”

我这里看到了`lines(x,...)`说明可以不用指定`y`，那画出来是什么？？
```R
> plot(c(0,10),c(0,10),type='n')
> lines(c(0,1))
> lines(c(5,9))
> lines(c(2,4))
> lines(c(10,1))
> lines(c(4,7))
```
![line(x)](http://onexs3cnv.bkt.clouddn.com/Rplot-line%28x%29.png)
可以看出来给出的`c(a,b)`，a,b都是表示纵坐标，默认好像横坐标是1到2，那这样就是画`(1,a)`到`(2,b)`的线？
至少实验出来是这样的
```R
> lines(c(4,7,6))
```
![line(x)456](http://onexs3cnv.bkt.clouddn.com/Rplot-line%28x%29-456.png)
三个向量元素，那上面的猜测是对的，现在是画`(1,a)`,`(2,b)`,`(3,c)`的线段，估计向量元素增多，就是横坐标到4，5，6了吧

## lines 的type
> lines(x, y, type = "l", ...)
> type 
> character indicating the type of plotting; actually any of the types as in plot.default.

说是根据`plot`的`type`来，一开始我觉得这不跟`lty`参数重复了么，其实两个是不一样的
```R
> plot(c(0,10),c(0,10),type='n')
> lines(c(2,4),c(3,8),type = "s")
> lines(c(6,7),c(3,8),type = "s",lty=2)
> lines(c(6,7),c(3,8),type = "l",lty=3)
```
![type-lty](http://onexs3cnv.bkt.clouddn.com/Rplot-type-lty.png)
当`type="s"`是，画的是折线！！！，`s`解释为step，相当于画的是曼哈顿路径。
`lty`才是线是什么样子的形式的。而`type`应该是画的什么什么形状吧，不知道怎么描述

### lty的实验

```R
plot(c(1,6),c(1,1),type='l',lty=1,ylim=c(0,8))
for(i in 2:6){
  lines(c(1,6),c(i,i),type = 'l',lty=i)
}
```
![lty](http://onexs3cnv.bkt.clouddn.com/Rplot-lty.png)

# text
在画布上写文本吧
直接看实验
```R
> plot(c(0,10),c(0,10),type='n')
> text(c(5,1),c(3,3),1)
> text(c(5,8),c(2,3),c("A","B"))
```
![text](http://onexs3cnv.bkt.clouddn.com/Rplot-text.png)

# points
画点。主要是`pch`,`cex`这两个参数有点意思
> pch
> plotting ‘character’, i.e., symbol to use. This can either be a single character or an integer code for one of a set of graphics symbols. The full set of S symbols is available with pch = 0:18, see the examples below. (NB: R uses circles instead of the octagons used in S.)
>
> Value pch = "." (equivalently pch = 46) is handled specially. It is a rectangle of side 0.01 inch (scaled by cex). In addition, if cex = 1 (the default), each side is at least one pixel (1/72 inch on the pdf, postscript and xfig devices).
>
> For other text symbols, cex = 1 corresponds to the default fontsize of the device, often specified by an argument pointsize. For pch in 0:25 the default size is about 75% of the character height (see par("cin")).
>
>cex
>character (or symbol) expansion: a numerical vector. This works as a multiple of par("cex").

目前我的理解就是pch就是点的样式，cex就是指定大小
## pch 实验
```R
plot(c(0,10),c(0,10),type='n')
line.draw = 9
for(i in 1:25){
	if((i-1) %% 5==0){
		line.draw = line.draw - 1
	}
	points((i-1)%%5,line.draw,pch=i)
}
```
![pch](http://onexs3cnv.bkt.clouddn.com/Rplot-points-pch.png)


# 回到题目
画这样的一个三角形。思路就是用`points`画大一点的圆圈，`text`来写`A`这中标签，然后`lines`来画线，没什么难度
```R
plot(c(0,10),c(0,10),type = 'n')
lines(c(3,5),c(4,9),type = 'l',lty=1)
lines(c(5,7),c(9,4),type = 'l',lty=1)
lines(c(3,7),c(4,4),type = 'l',lty=1,xlim=c(2.5,6.7))
points(5,9,pch=1,cex = 5)
text(5,9,'A')
points(3,4,pch=1,cex = 5)
text(3,4,'B')
points(7,4,pch=1,cex = 5)
text(7,4,'C')
```
不过我这样，太啰嗦了啊

R中的最常用的对象就是向量，很多运算都支持向量操作。可以用向量
```R
plot(c(0,10),c(0,10),type = 'n')
x <- c(3,5,7)
y <- c(4,9,4)
points(x,y,cex=5)
text(x,y,c("A","B","C"))
lines(x,y,type='l')
```
![triangle-vector](http://onexs3cnv.bkt.clouddn.com/Rplot-plot-triangle-vector.png)

`lines(x,y)` , 这个`x`，`y`的坐标，相当于这里，两个坐标的`x`都提取出来到`x`，两个坐标的`y`都提取出来到`y`，相当于起始点终点的`x`坐标放一起，起始点终点的`y`坐标放一起.感觉python中的`map(None,x,y)` 后就是`[(3,4),(5,9),(7,4)]` 其实就是各点的坐标

但是是不闭合的，为什么，其实两个组合确定一条线，可能`lines`中的向量，`x`先是`(3,5)`,在是`(5,7)`,`y`对应，但后面没有回去`(7，3)`。要手动添加
```R
lints(c(x,3),c(y,4),type='l')
```
这样就和开篇的fancybox的图片里面一样了。
