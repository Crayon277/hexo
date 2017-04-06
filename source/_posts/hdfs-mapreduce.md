---
title: Intro to hadoop and MapReduce -- hdfs & mapreduce (二)
date: 2017-04-06 16:34:28
categories: bigdata
tags: [hadoop,mapreduce,udacity]

---

## Quiz： Is there a problem
- [x] network failure
- [x] disk failure on datanode
- [] ~~not all datanode used~~ (Why do you think that all nodes have to be used. What if you have hundreds of Data Nodes?)
- [] ~~block sizes differ~~ (If block sizes would have to be the same, what would happen if the file could not be divided in same size blocks?)
- [x] disk failure on namenode


what if namenode had hardware problem
## Quiz: any problems now
- [x] data inaccessible  (when network failure)
- [x] data lost forever  (when disk failure)
- [] no problem

so, depends.


