---
title: PBFT算法理解
date: 2017-06-18 21:09:59
categories: blockchain
tags: [algorithm,blockchain,fabric]

---
参考资料：

- [超级账本PBFT（拜占庭容错）算法详解](http://bitkan.com/news/topic/21120)

![rough workflow](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-18%20at%209.11.30%20PM.png)

Q: 为什么是f+1
A：一方面，一个极端，因为拜占庭错误节点最多f个，当我有f+1个一致的结果，这f+1个没有一个是错误的节点，那么不管总数多少，即使我还有f个错误的，因为最多f个，但我已经有f+1个一致的结果了，f+1>f，所以作恶失败。另一个极端，f+1中有f个错误的节点。**因为结果都一样！！**，而最多是有f个replicas出现问题，所以至少有一个replicas是正确的，就是这个+1,而结果一致，说明这些结果都是正确的。f+1就是能保证了收到的结果是正确的。

---

> 紧接着prepare阶段，当一个replica节点发现有一个quorum同意编号分配时，它就会广播一条COMMIT信息给其它所有节点告诉他们它有一个prepared certificate了。与此同时它也会陆续收到来自其它节点的COMMIT信息，如果它收到了2f+1条COMMIT（包括自身的一条，这些来自不同节点的COMMIT携带相同的编号n和view v）


Q: 这里为什么是2f+1条commit
A: 最多容错n-1/3个(令等于f)，n=3f+1,然后减掉f个错误的，2f+1
