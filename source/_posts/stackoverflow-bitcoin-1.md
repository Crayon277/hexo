---
title: stackoverflow-bitcoin-1
date: 2017-05-29 18:31:21
categories: stackoverflow
tags: [stackoverflow,bitcoin,blockchain]
description: 学习stackexchange bitcoin板块的别人的惑。

---

# 工作量证明机制和权益证明机制有什么区别[What's the difference between PoW and PoS?'](https://bitcoin.stackexchange.com/questions/43467/whats-the-difference-between-pow-and-pos)

我正在寻找能够说明工作量证明机制算法和权益证明机制算法的解释，还有他们是如何和比特币还有区块链有联系的。

也希望有一个非常简单明了没有包含过多技术的回答。可以有一点技术方面的东东，但我不是开发者，我并不知道怎么去编程。

（）（）

---

下面几点简要的概括：

- 一个加密货币有它自己的区块链来储存所有出现的交易
- 工作量证明机制和权益证明机制是两种不同的算法来获取 哪个区块将会链接到区块链后面 的共识。
- [工作量证明（PoW）](https://en.bitcoin.it/wiki/Proof_of_work)需要某种类型的工作发生的证明。就比特币矿工来说，他们需要在区块被其他接受之前做这个工作。
- [权益证明(PoS)](https://en.bitcoin.it/wiki/Proof_of_Stake) 要求用户拥有相当量的货币（比如拥有许多coins）来决定下一个区块。这有某一方垄断货币的高风险。但是有几种方法可以阻止（通过随机分配利益相关者来共识新区块，其他）

最主要的区别可以归结于，工作量证明机制需要额外的资源（挖矿设备）但权益证明不需要。如果比特币家里减少，越来越少的人被激励去挖矿，因此会导致整个系统的安全性减少，工作量机制会被苛责（criticized) 。而权益证明机制，因为它是免费来增加新区块到区块链后面的，你可以用它来同事做几个相似的币的权益证明（详见PoS链接中的“nothing at stake”问题）

例子：
- 比特币，莱特币还有其他许多币种使用PoW方法。
- NXT，BitShares还有其他使用PoS方法。
- 以太坊使用PoW但是它计划要转到PoS.
- PeerCoin使用PoW和PoS的结合机制。
