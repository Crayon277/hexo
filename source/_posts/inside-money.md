---
title: 愚见比特币（一）--货币的本质
date: 2017-05-18 10:42:39
categories: blockchain
tags: [bitcoin,monetary,currency]
description: 看了一些资料，表达能力不好，但还是尽量把我的看法尽可能的表达出来

---

对货币的研究不是很深入，但毕竟是每天都用的东西，然后结合了一些看的资料，下面给出我的理解，不对的地方非常欢迎指点。

---

要想了解比特币，还得从猴子变人开始说起...

古时候，人们交易，实际上就是交换，比如我有鸡蛋，你有牛奶，我刚好需要牛奶，然后你刚好需要鸡蛋，然后商量着，我用30个鸡蛋换你一桶牛奶。

![exchange](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-05-18%20at%2010.48.12%20AM.png)

但是社会体系越来越庞大后，需求也越来越多后，可能我要牛奶，但牛奶拥有者不要鸡蛋，所以我还得先换到他想要的那样东西，这让我想起了我小时候听的磁带里面的一则故事，故事名字还有里面具体的那个物品名字我给忘了，大概意思就是小兔他妈妈让小兔子拿着自家缝的一块布去换家里需要的白菜（我指的具体的物品是指这些，但这不是终点，忽略这些细节），然后小兔子找到白菜主人，他不要布，他要地瓜，然后找到地瓜主人，问要不要交换，然后也不要，他要香蕉，然后又去找香蕉的主人，反反复复，找到最终能交换到需要布的，然后再一步步回朔换到白菜。就是一个递归的过程。这样换，就很麻烦

![exchange_multi](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-05-23%20at%203.02.26%20PM.png)

（图片中的尖头表示拥有者手中持有物的更替）

然后慢慢大家达成某种共识，就是抽取出一种特殊商品，所有其他东西都可以由它等价交换（一般等价物）。现在我鸡蛋换牛奶是，先用30个鸡蛋换100个海贝，这里海贝就是这种“中介商品”，然后100个海贝再去换1桶牛奶

![exchange-agency](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-05-18%20at%2011.02.56%20AM.png)

这个海贝其实就是货币的雏形，然后慢慢的发展到金属货币，经历银本位，复本位，金本位，blabla的，这里我也不是很了解，但不影响。比如我国古代的铜币，银子，金子。但是金属有个弊端就是太重了，后来就有钱庄，发行银票，但银票本质还是以金子做货币基础的，银票只是起到了符号的作用。我国南宋的交子是最早政府发行的纸币（银票），而且这些交子（银票）都是由商人自由发行的。

到了二战结束后，全球形成了以美元为中心的布雷顿森林体系，取代了站前的金本位制度，后来美国取消兑换黄金后，全球真正进入了信贷程序发行货币的时代。

以前是用黄金作为中介，这些都是实物，看得见摸得着的。现在的纸币本位，其实是由国家信用作为“抵押”的

> 基础货币相当于政府向全国国民的借债，但至于借债是否能被偿还，乃至政府资产是否价值，只取决于人们对政府的信心和政府自身的信用

我是这么理解的。如果A欠B十块钱，B欠C十块钱，是不是通过商量协定后A欠C十块钱一样的。那现在其实就是把人民币看作一种权利义务的关系，我们是债权人，国家是债务人，我们有100元，先把这个单元去掉，相当于就是（我们有对国家的100债券），然后我们交易，我给你10元，就是我把对国家的10个债权转让给你。现在是把这个关系抽象出来放在原来黄金的位置上。

其实上面的这个债券债务关系比喻还是有点不太恰当，毕竟国家发行货币就是不断印钞，印多了通货膨胀。之前商业银行还可以发行自己的货币，但后来中央将这个权利回收，只有中央可以发行货币。

总结来说，很久以前的海贝变成了现在的纸币。货币用来买卖的，为什么我接受这个货币，其实就是大家都认可么，就像海贝，从商品中分离出来固定充当一般等价物，因为海贝是实物，摸得着看得见，后面是大自然“撑腰”。现在只是后面是国家的信用“撑腰”

那我们的财富是什么，是我们手上的100元吗？不是，财富是我们**资产负债表**的加加减减。可以说货币就是记账方式，钱只是账本上面的一串数字，那每个人其实有一本账本（在银行里）。

那比特币本质其实就是一个所有人的账本，所有人交易放在一个账本上，所有人都可以看，所有人都可以维护。
它是去中心化的，没有中央银行。记载在我们现在生活中的账本的那些数字，我们给它一个单位叫元，叫美元，日元等等。然后在比特币这个系统，我们给它一个单位叫比特币。这个系统中发行货币的方式就是“矿工挖矿“（我不太喜欢这个称号，久而久之就不知道本质是啥了，其实就是全网的记账人），给记账人记账的奖励就是产生新的比特币，以及交易产生的手续费。

那我们现实生活中的货币是基于国家信用的，而比特币是基于密码学，基于数学原理。**只要大家都认可**（共识机制），就可以交易了。

那国家货币还有一些防伪手段等来解决现实生活中出现的问题。下面会说明比特币是怎么利用数学来解决这个问题的。


---

我的理解不是很深，欢迎指正。也请阅读的过的人留下邮箱，万一有错，不想误人子弟，等错误更正会通过邮箱来提醒你。
