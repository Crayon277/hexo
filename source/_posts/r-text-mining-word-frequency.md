---
title: 用r做一个简单的统计词频的程序
date: 2017-04-08 14:31:23
categories: R
tags: [R,text-mining,R-piece]

---
要求：
假设`文件1`中有内容`a b c c`,`文件2`中有`a b d`
现在要统计成如下的样子：

|       | a | b | c | d |
|-------|---|---|---|---|
| 文件1 | 1 | 1 | 2 | 0 |
| 文件2 | 1 | 1 | 0 | 1 |

用到R中的table函数

<!-- more -->
# 预备
## table
> table uses the cross-classifying factors to build a contingency table of the counts at each combination of factor levels.

```R
> f1
[1] "a" "b" "c" "c"
> table(f1)
f1
a b c 
1 1 2 
```
文档中说了`table`使用`facter`中的`level`来生成统计项，然后记录各项出现的次数。

## factor
```R
set.seed(102)                           # This yields a good illustration.
x <- sample(1:3, 15, replace=TRUE)
education <- factor(x, labels=c("None", "School", "College"))
```
```R
> x
[1] 2 2 3 2 1 2 3 1 3 2 3 3 3 2 2
>education
[1] School  School  College School  None    School  College None    College
[10] School  College College College School  School 
Levels: None School College
```
上面可以看出labels就是实现一种转化么。默认是`lables = levels(x)`



# 解题思路
因为`文件1`中没有d，但统计的时候还是要有它的项，当然值是0。所以我们要有一个`level`是包含所有的项的
```R
> table(factor(f1,levels=c('a','b','c','d')))

a b c d 
1 1 2 0 
```

这里有另一个话题就是读取文件还可以用`readLines`函数，不过
```R
> readLines(file.choose())
[1] "a b c c"
```
可以看到，这是一个向量，`scan`读进来直接是分开的。
所以如果用readLines的话，还要用`strsplit`函数进行分割，就和python中的`split`函数一样
还有我这里用`file.choose()`来手动选择文件，因为在mac上不知道为什么绝对路径传进去都有问题。[Todo]

## 简单情况
现在将情况简单化一点，现在假设只有一个文件，现在统计的`文件1`等就是第1行，依次类推。
### 先得到所有的词，每个词是一个元素，像`scan`那样
```R
dat <- readLines(file.choose())
rownum <- length(dat)
word <- NULL
for(i in 1:rownum){
	di <- dat[i]
	di <- strsplit(di,split=' ')[[1]]
	word <- c(word,di)
}
```
### 得到所有的项
其实也就是数学里面的集合么。估计`Levels`就是集合实现的
```R
> factor(word)
[1] a b c c a b d
Levels: a b c d
```
这样就得到了所需要的所有项`a`,`b`,`c`,`d`

那其实因子`a b c c a b d`它是按顺序来的，那其实对第一行的统计就可以`table(factor(word[1:len_row_1]))`
那`len_row_1`怎么得来，就可以在原来的`for`循环中直接用`length`计算出
```R
dat <- readLines(file.choose())
rownum <- length(dat)
len <- rep(0,rownum) #
word <- NULL
for(i in 1:rownum){
	di <- dat[i]
	di <- strsplit(di,split = ' ')[[1]]
	word <- c(word,di)
	len[i] <- length(di) #
}
```
多了有`#`号标记的这两行

### 统计
事先先生成`rownum`行然后`length(levels(factor(word)))`列的矩阵，之后往里面塞就行了
```R
f <- factor(word)
l <- levels(f)
m <- matrix(0,nrow = rownum,ncol = length(l))
```
```R
> m
     [,1] [,2] [,3] [,4]
[1,]    0    0    0    0
[2,]    0    0    0    0
```
因为我们现在有了`len`
```R
> len
[1] 4 3
```
`4`意思是文件第一行的元素个数，`3`就是第二行的
然后我们可以用数组的知识，也就是类似c语言中的两个指针来移动了
```R
start <- 1
for(i in 1:rownum){ # 这里我一开始忘了写1:，只是rownum，导致一直bug
	end <- start+len[i] - 1
	m[i,]<-table(factor(word[start:end],levels = l))
	start <- end+1
}
```
```R
> m
     [,1] [,2] [,3] [,4]
[1,]    1    1    2    0
[2,]    1    1    0    1
```
弄的好看一点
```R
> colnames(m)<-c('a','b','c','d')
> m
     a b c d
[1,] 1 1 2 0
[2,] 1 1 0 1
```

## 复杂情况
就是要前面的步骤，要读取多个文件。其实后面步骤都是一样的。只是一个是将多文件的内容放在一个文件的每一行，同样我们需要知道所有的项，也就是levels。多出来的工作也就是我们要读多个文件，然后进行拼接而已。
没什么难度，只是代码的优雅程度不一样而已。
### R下的文件目录操作
- `dir.create('newdir')`：创建文件夹
- `unlink('directory',recursive=TRUE)`:删除文件夹，若有文件一并删除
- `file.create('newfile')`: 创建一个新文件，若存在则会覆盖原文件
- `cat('hello world',file='newfile',append=TRUE)`: 文件加入一行内容
- `file.append('file1','file2')`: 将`file2`的内容添加到`file1`的后面
- `file.copy('source','des')`:拷贝文件`source`到文件`des`
- `file.show('filename')`： 显示文件内容
- `file.remove('filea','fileb')`: 删除文件
- `list.files()`：显示当前工作目录下的文件列表

这里可以借助`list.files()`来搭桥。知道了目录下的文件列表，我们就可以用循环了

### 合并数据
```R
f <- function(x){
	data <- readLines(x)
	return(strsplit(data,split=' '))
}
	
dir_path <- '/Users/Crayon_277/Develop/Project/R/homework/3'
files <- list.files(dir_path,pattern = '[0-9]+.txt$',full.names = T)
	
result <- lapply(files,f)
```
`list.files`中的`full.names`参数为`false`的时候
```R
> files
[1] "1.txt"      "2.txt"
```
当为`T`的时候
```R
> files
[1] "/Users/Crayon_277/Develop/Project/R/homework/3/1.txt"
[2] "/Users/Crayon_277/Develop/Project/R/homework/3/2.txt"
```
区别就一目了然了

```R
> result
[[1]]
[[1]][[1]]
[1] "a" "b" "c" "c"


[[2]]
[[2]][[1]]
[1] "a" "b" "d"
```
然后可以在用`for`语句拼接，或者一开始直接用`for`遍历

> lapply returns a list of the same length as X, each element of which is the result of applying FUN to the corresponding element of X.
> lapply就类似python中的map


