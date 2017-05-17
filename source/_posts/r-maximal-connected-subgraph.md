---
title: 用R来找最大连通子图
date: 2017-03-25 08:35:37
categories: R
tags: [R,R-piece,BFS,DFS,algorithm]
photos:
- http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-11%20at%208.41.36%20AM.png

---

求上图的最大连通子图，其实就是图的遍历，图的遍历有深度优先和广度优先
图有很多种对应的存储结构，在R里面最简单的就是邻接矩阵了。

-update-
- 用深度优先搜索做
- 在深度优先里面涉及到的R中的全局，局部变量
<!-- more -->

# 构造邻接矩阵
```R
m <- matrix(0,5,5)
m[1,2] <- 1
m[1,3] <- 1
m[2,3] <- 1
m[4,5] <- 1

m <- m + t(m)
```
```R
> m
     [,1] [,2] [,3] [,4] [,5]
[1,]    0    1    1    0    0
[2,]    1    0    1    0    0
[3,]    1    1    0    0    0
[4,]    0    0    0    0    1
[5,]    0    0    0    1    0
```
主要也就是`m<-m+t(m)`这一步，因为是无向图，是对称矩阵，可以先构造一半然后与转置相加。**这是对称矩阵的性质的应用！！**
> 在线性代数中，实对称矩阵是一个方形矩阵，其元素都为实数，且转置矩阵和自身相等
> [实对称矩阵](https://zh.wikipedia.org/wiki/%E5%AE%9E%E5%AF%B9%E7%A7%B0%E7%9F%A9%E9%98%B5)

# 广度优先遍历

主要思想就是它分两个部分，一个部分保存已经访问过的，一个部分是未访问的，未访问部分是用一个队列来存储，每次从队头出一个元素i，然后将这个元素的能够够到的节点依次加到队尾去。这一步其实就是邻接表中的第i行中为1的元素加进来

先考虑简单的情况，从第1个节点出发，寻找包含1的最大联通子图，其实就是1能够直接或间接够到的所有节点，在图中我们可以直观的看到是1，2，3，三个节点。

## 错误的代码
```R
visited <- c(1)
unvisited <- m[1,]

while(length(unvisited)>0){
	now <- unvisited[1]
	unvisited <- unvisited[-1]
	candidate <- m[now,]
	candidate <- setdiff(candidate,visited)
	unvisited <- union(candidate,unvisited)
	visited <- c(visited,now)
}

print(visited)
```
这里我犯了一个错误，`unvisited <- m[1,]`,这是`unvisited`里面保存的是什么？？
```R
> unvisited
[1] 0 1 1 0 0
```
那我想要的是什么？应该是`visisted`中一开始是`1`,`unvisisted`中将`1`的邻接节点加进来是`2,3`,然后后面每次循环体内做的是队头元素出队列。但是加进来的元素应该是代表这个节点的符号,反应在矩阵中的应该是下标。矩阵里面存的其实是边信息，`1`代表有边,`0`代表无边，**其实要的是`0 1 1 0 0`对应的下标！！！需要的是节点信息**，这其实是两个概念

## 初始化
我欠缺的也就是我知道我想要的是什么，但是不熟悉R语法，或者说不知道怎么用R语言来实现，虽然我熟悉python语法，但我也不能保证我能写出很优雅的代码，因为跟别人差就差在，他们不仅精通语法，还知道他们的性能，能有很多组合。

这里我需要的是读进来第1行矩阵元素有`1`的下标，取下标怎么取

有关下标的函数,目前只注意到下面的三个
- `which`:Give the TRUE indices of a logical object, allowing for array indices.
- `which.min`:最小值的下标
- `which.max`:最大值的下标

按照条条大路通罗马的理论，只要这个函数跟目标有点沾边的肯定能实现，只是看你的想象力，是否能突破天际
因为`which`是需要一组逻辑向量，在R中逻辑值只有`TRUE`和`FALSE`,然后它会返回`TRUE`的下标
只要把`0 1 1 0 0`转换为逻辑值就行了。查了一下
```R
> as.logical(c(-1,0,1,2))
[1]  TRUE FALSE  TRUE  TRUE
```
可以看到`as.logical`认为只有`0`是`FALSE`，其它为`TRUE`,这样路就通了
```R
visited <- c(1)
unvisited <- which(as.logical(m[1,]))
```
因为只要得到逻辑向量就可以了，那逻辑操作还可以用`m[1,] == 1`来得到逻辑向量值。这也可以
还有没有其他方案？

因为我注意到这里要么是`0`,要么是`1`,可以用向量`1 2 3 4 5`去乘，就得到了`0 2 3 0 0`,然后只要大于0的就行了
```R
index <- c(1:5)
edge2node <- index*m[1,]
unvisited <- edge2node[edge2node > 0]
```
`edge2node[edge2node > 0]` 中的`edge2node>0`计算完之后是逻辑值，然后用`[]`下标操作取逻辑值只为`TRUE`的元素

上面两种得到的
```R
> unvisited
[1] 2 3
```
就是我想要的

## 遍历
上面一开始写的错误的代码中也就是和上面一样的问题。只要改了这一部分就行了。
```R
while(length(unvisited)>0){
	now <- unvisited[1]
	unvisited <- unvisited[-1] # 队头元素出队列
	#candidate <- m[now,]
	candidate <- which(as.logical(m[now,]))
	candidate <- setdiff(candidate,visited)
	unvisited <- union(candidate,unvisited) # 将队头元素的邻接节点加入队列
	visited <- c(visited,now)  # 将队头元素加入已访问的
}
print(visited)
```

这里`setdiff`和`union`是集合运算，因为可以在图上直观的看到，`1`这个节点可以找到`2`,`3`。到`2`这个节点，可以找到`1`,`3`,但此时，`1`这个节点是已经访问了的，如果不处理，还是加进队列里面的话，那就不断在循环了！！！

`setdiff`是取差值，注意参数的位置，**是将`visited`里面有的元素从`candidate`中消掉**
`union`是取并集，没什么好说的了
还有一个`intersect(x, y)`就是取交集

最后的结果
```R
> print(visited)
[1] 1 2 3
```

## 全图对每个节点进行同样的操作
图的最大连通子图，那就对每个节点都进行上面的操作，然后图包含节点最多的就是这个图的最大联通子图了

```R
max_node_num <- 0
maximal_connected_subgraph <- NULL
for(i in 1:5){
  visited <- c(i)
  unvisited <- which(as.logical(m[i,]))
  while(length(unvisited)>0){
    now <- unvisited[1]
    unvisited <- unvisited[-1]
    candidate <- which(as.logical(m[now,]))
    candidate <- setdiff(candidate,visited)
    unvisited <- union(candidate,unvisited)
    visited <- c(visited,now)
  }
  current_node_num <- length(visited)
  if(current_node_num > max_node_num){
    max_node_num <- current_node_num
    maximal_connected_subgraph <- visited
  }
}

sort(maximal_connected_subgraph)
print(m[maximal_connected_subgraph,maximal_connected_subgraph])
```
result:
```R
> print(m[maximal_connected_subgraph,maximal_connected_subgraph])
     [,1] [,2] [,3]
[1,]    0    1    1
[2,]    1    0    1
[3,]    1    1    0
```

# 深度优先遍历
深度优先就是一条道走到底，无路可走的时候，及时浪子回头，然后又不听教诲又去浪到底，直到玩累了，回家的过程。

## 思路
涉及到一个回朔。这样就需要一个`parent_node`来保存父节点的信息。这里我想到，是不是要回去的时候要重新计算父节点的邻接节点，因为这样才能知道其他节点啊。

同样还需要一个`visited`来保存已经访问过的节点。然后在访问完一个节点，要将这个节点加入`visited`中，在要遍历下一个节点的时候，需要取一个节点。那这个时候需要看这个节点是不是已经访问了。
这里我想到了两个方案：
1. 一个一个取。意思是下标操作，取一个对比一下是不是在`visited`中，可以用`any(visited == current_node)`如果是`FALSE`就是还未访问过。`visisted == current_node`返回的是一个逻辑向量，然后用`any`函数如果有一个是`TRUE`那返回值是`TRUE`，返回`FALSE`说明没有一个是相等的。
2. 一下子全取出来。然后用集合运算，做差，然后再取出一个。

然后我用笔在纸上模拟的时候，发现这应该是个递归的过程。那`visisted`需要全局来维护，那这样函数体内就用循环可以了，遍历一个节点的所有邻接节点，然后对每一个节点再进入这个函数。这样就不需要`parent_node`来维护了，但是需要一个边界条件来终止递归。那就是一个节点的所有邻接节点都被访问过了。

## 发现的问题，`visited`全局变量
```R
m <- matrix(0,5,5)
m[1,2] <- 1
m[1,3] <- 1
m[2,3] <- 1
m[4,5] <- 1

m <- m + t(m)

visited <- c(1)

dfs <- function(current_node){
  #browser()  # 调试用的
  
  candidate_node <- which(as.logical(m[current_node,]))
  candidate_node <- setdiff(candidate_node,visited)
  #print(candidate_node)
  if(length(candidate_node) == 0){
    return(0) #这个0返回的没有意义的，随便都可以，只是单纯的结束
  }
  for(i in candidate_node){
    visited <- c(visited,i) #访问i节点
    dfs(i) #递归
  }
}
dfs(1)
print(visited)
```

上面的结果出错了
```R
Error: evaluation nested too deeply: infinite recursion / options(expressions=)?
Error during wrapup: evaluation nested too deeply: infinite recursion / options(expressions=)?
```
那就是递归没返回
调试了一下，发现问题出现在`visited`上，`dfs(i)`进去的时候，理想中`visited`应该是全局变量，在循环中我将`i`节点加入已访问的节点中，但是发现递归进去的时候，`candidate_node <- setdiff(candidate_node,visited)`这时候的`visited`值是`1`,就是初始值。可是为什么呢？？？

> 内部函数在它的环境中查找visited的值（查找的顺序为：首先函数体的局部变量，参数；然后是外部函数中的局域变量，参数；最后是全局变量） 

所以当在函数内做赋值的时候，相当于就建立了一个局部变量，那在第一层的时候`visited <- c(visited,i)`这个语句还没执行到的时候，此时的`visited`在函数体内还没有定义！那找到的就是外部的变量，所以调试的时候看到的是`1`，那其实相当于因为在递归的时候可以看作都是进入自己的函数，所以每一层的`visited`都是独立的。

## 方案 1 : return(visited)
```R
dfs2 <- function(current_node,vis=NULL){
	candidate_node <- which(as.logical(m[current_node,]))
	candidate_node <- setdiff(candidate_node,visited)
	    
	if(length(candidate_node) == 0){
		return(NULL) 
	}
	for(i in candidate_node){
		if(!any(visited == i)){
			visited <- c(visited,dfs2(i))
		}
		return(visited)
	}
}
```
这么写有两个问题！！！
第一个是有闭环的时候，因为我在前面的代码计算`candidate_node`的时候是依赖`visited`的，在每一层的函数进去后，因为前面说了，每一层的`visited`是独立的，所以在没有赋值之前，也就是没有在下一层`return`之前，用的都是外部的`visited <- c(1)`这个值，所以这时候计算的`candidate_node`肯定是不正确的，不是我们想要的，因为不能正确判断是否邻接节点已经访问过。这是根源，所以导致了在下面`for`循环的时候，在闭环的情况下，因为没有正确的将已经访问的排除掉，而无限的递归。

第二个是分叉，就最简单的情况，`1`连接`2`,`3`,但后两个不连接，因为到`2`中，`visited`是外部的`1`，所以这里是恰好，凑巧，刚刚好`candidate_node`计算为空，返回，但是！！！返回的是空！这样`visited <- c(visited,dfs2(i))`这个语句就没有起作用，追其根源那就是`return`写的不正确。一方面是这里连`return(visited)`都没执行到，相当于在`2`层这里直接返回`NULL`，但是并没有把`2`这个节点加入`visited`中。
而且，即使不管上面的情况，在`2`饭后会，后面直接`return(visited)`了，函数直接退出了。`3`根本就没做。

试错：
```R
m <- matrix(0,3,3)
m[1,2] <- 1
m[1,3] <- 1
m + t(m) -> m

visited <- c(1)

print(dfs2(1))
```
结果
```R
> print(dfs2(1))
[1] 1
```

[todo] 使用return 写递归应该是可以的，那就是我整体的递归应该不是按照原来的思路了。但目前还没有想到怎么写


## 方案 2 : 这个`visited`当作一个参数传递就行了

但是发现，这个只是值传递参数，不是引用传递，也就是参数变了，最后`visited`自己没有改变没有用啊，`print(visited)`就没用，最后结果就只是`1`

## `<<-`解决

然后我[查到](https://zhangjg.github.io/blog/2015/12/25/The-Closure-in-R.html)里面提到了`<<-`，可能这个操作符才是将变量复制到全局变量中去，不然`<-`就在函数体内生成了一个同名的局部变量
然后我就将上面的`visited <- c(visited,i)`改为`visited <<- c(visited,i)`
得到的结果是
```R
> print(visited)
[1] 1 2 3 3
```
多了一个`3`，这个是因为在第一层的时候也就是`current_node`为`1`的时候，邻接节点是`2`,`3`,在`for`循环中，先进入`2`节点，此时可以遍历的只有`3`,然后进入`3`,访问完，回朔，此时应该是在这个图下`1`,`2`,`3`都是遍历完了的，但是回朔到`1`节点的时候，`for`循环还有一个`3`没执行，所以在`for`循环里面还要再加一个条件，看是否已经遍历过。
```R
for(i in candidate_node){
	if(!any(visited == i)){
		visited <<- c(visited,i) #访问i节点
	}
	dfs(i) #递归
}
```
结果：
```R
> print(visited)
[1] 1 2 3
```
## 寻找最大连通子图

那就是再用一个`for`循环封装一下，和上面`BFS`一样。

完整代码
```R
m <- matrix(0,5,5)
m[1,2] <- 1
m[1,3] <- 1
m[2,3] <- 1
m[4,5] <- 1

m <- m + t(m)

max_length <- 0
maximal_connected_subgraph <- NULL
node_num <- length(m[,1])

dfs <- function(current_node,vis=NULL){
  candidate_node <- which(as.logical(m[current_node,]))
  candidate_node <- setdiff(candidate_node,visited)
  if(length(candidate_node) == 0){
    return(NULL) #这个0返回的没有意义的，随便都可以，只是单纯的结束
  }
  for(i in candidate_node){
    if(!any(visited == i)){
      visited <<- c(visited,i) #访问i节点
    }
    dfs(i) #递归
  }
}
for(i in 1:node_num){
  visited <- c(i)
  dfs(i)
  print(visited)
  current_length <- length(visited)
  if(current_length > max_length){
    max_length <- current_length
    maximal_connected_subgraph <- visited
  }
}
sort(maximal_connected_subgraph)
print(m[maximal_connected_subgraph,maximal_connected_subgraph])
```
## 测试复杂的用例
构造一个新的图
![new-test](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-04-11%20at%208.00.24%20PM.png)
这么构造是因为多了一个闭环，以及让`1`,和`2`节点多了一个选择，测试回朔的过程
```R
> sort(maximal_connected_subgraph)
[1]  1  2  3  6  7  8  9 10
```
结果正确，就是打印的时候有点歧义，因为打印出来的矩阵如果没指定名字，又是1,2,3..顺序来的，会误以为是那几个节点，改一下名字就可以了
```R
mresult <- m[maximal_connected_subgraph,maximal_connected_subgraph]
colnames(mresult) <- maximal_connected_subgraph
rownames(mresult) <- maximal_connected_subgraph
print(mresult)
```
结果是：
```R
> print(mresult)
   1 2 3 6 9 7 8 10
1  0 1 1 0 0 1 0  1
2  1 0 1 1 0 0 0  0
3  1 1 0 0 0 0 0  0
6  0 1 0 0 1 0 0  0
9  0 0 0 1 0 1 0  0
7  1 0 0 0 1 0 1  0
8  0 0 0 0 0 1 0  0
10 1 0 0 0 0 0 0  0
```


