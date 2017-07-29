---
title: 微信小程序-snake案例解析
date: 2017-07-12 22:06:45
categories: wechat 
tags: [javascript,html,css]
description: 以微信贪吃蛇小程序为例，入门小程序

---

# snake.wxml


## wx:for

```html
<view class="ground">
    <view wx:for="{{ground}}"  class="rows" wx:for-item="cols">
        <view wx:for="{{cols}}" class="block block_{{item}}" >

        </view>
    </view>
</view>
```

最外层的`view`想成一个大容器，这个容器的大小是由相对应的`ground`的wxss规定的，然后内层第一个`view`是放在这个大容器的一个抽屉，然后最里层是放在这个抽屉里面的东西，

想象建立一个操场，先是规划好操场的大小，划好地块，然后在每一排的植被土壤弄好，然后再一块一块的假草放上去。

注意的就是，**默认数组的当前项的下标变量名默认为`index`，数组当前项的变量名默认为`item`**

```html
<view wx:for="{{array}}">
  {{index}}: {{item}}
</view>
```
这个`index`就是下标索引，从零开始，而`item`是数组里面具体的东西
比如这个`array`在js里赋值`['a','b','c','d']`
那么打印出来的是：
```
0:'a'
1:'b'
3:'c'
4:'d'
```
如果是`[[1,2],[2,3],[3,4]]`
那么打印出来是：
```
0:[1,2]
1:[2,3]
2:[3,4]
```
所以`item`表示的就是第`index`下标对应的值
`wx:for-index="idx"`,`wx:for-item="itm"`只是名字不叫`item`,`index`而已，自己命名罢了。




参考：
- [列表渲染](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/view/wxml/list.html)

## modal弹出框组件

参考：
- [微信小程序之弹框modal](http://www.cnblogs.com/simba-lkj/p/6509927.html)
- [微信小程序把玩（二十三）modal组件](http://blog.csdn.net/u014360817/article/details/52671211)



# snake.wxss 中
## flex属性
首先看标签结构
```html
<view class="score">
    <view class="title">snake</view>
    <view class="scoredetail">
        <view class="scoredesc">得分</view>
        <view class="scorenumber">{{score}}</view>
    </view>
    <view class="scoredetail">
        <view class="scoredesc">历史最高</view>
        <view class="scorenumber">{{maxscore}}</view>
    </view>
</view>
```
上面的布局用图示就是
![layout](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.17.00%20PM.png)

```css
.score {
    display:flex;
}

.scoretitle{
    flex:1;
	...
}

.scoredetail{
    flex:1;
	...
}
```

如果用了flex就是这样的展现形式
![flex](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.21.04%20PM.png)

如果`.score`中设置的`display`设置为`block`,效果为
![block](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.22.58%20PM.png)
而且其他`inline`,`grid`等都是上面这个效果。

其实`flex`还隐藏了一个设置，就是`flex-flow`应该默认是`row`，所以在一列上展开。flex是flexiable的缩写，注意在`scoretitle`和`scoredetail`中都有设置`flex`值，这个值表示的意义就是比重，我是这么理解的。比如，如果将`scoretitle`中的`flex`值改为`4`

![4flex](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.28.25%20PM.png)
可以看到`title`的视图占的地盘越来越大，而因为另外两个视图都是由同样的`scoredetail`控制，`flex`都为1，所以占比相同。

**而且因为是`flex`，所以只要是关于距离的属性值，都会影响到它**，比如`scoretitle`中的`margin`值的左侧改为`200rpx`
```css
.title{
	...
    margin: 40rpx 20rpx 40rpx 200rpx;
	...
}
```
![margin200](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.35.06%20PM.png)

可以看到因为title这个视图被要求离左侧200rpx，**导致另外两个视图被等比例的压缩了。**

参考:
- [display:flex多栏多列布局](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-12%20at%2010.35.06%20PM.png)

## 操场宽度 rpx

参考：
-[微信小程序尺寸单位rpx以及样式相关介绍](http://www.51xuediannao.com/javascript/xiaochengxu_rpx.html)

```
.ground{
    width: 660rpx;
    height:840rpx;
    margin-left: 40rpx;
    background-color: #eee4da;
}
.block{
    width:30rpx;
    height:30rpx;
    float: left;
    background: #ccc;
}
```
> rpx单位是微信小程序中css的尺寸单位，rpx可以根据屏幕宽度进行自适应。规定屏幕宽为750rpx。如在 iPhone6 上，屏幕宽度为375px，共有750个物理像素，则750rpx = 375px = 750物理像素，1rpx = 0.5px = 1物理像素。

因为一个块设定30rpx,然后每一行有22个（22列），所以操场宽度是22*30=660rpx, 有28行，高度就是28*30=840rpx。


# snake.js
逻辑层！！

## setData

参考：
- [关于微信小程序里面this.setData到底怎样或运行的？](https://segmentfault.com/q/1010000007078232/a-1020000007103717)

> setData 函数用于将数据从逻辑层发送到视图层，同时改变对应的 this.data 的值。
> 注意
> 1.直接修改 this.data 而不调用 this.setData 是无法改变页面的状态的，还会造成数据不一致
> 2.单次设置的数据不能超过1024kB，请尽量避免一次设置过多的数据。

> 1.页面最终绑定的是data对象上的属性（键）
> 2.setData(obj)方法中要求对象作为参数，他做了两件事
>    1)他会将obj参数上的属性浅拷贝到data对象上，该功能建议你参考Object.assign()方法的功效
>    2)obj参数上的属性浅拷贝到data对象的同时，会对页面绑定该属性的地方重新渲染，起到了脏值检查的作用


### 为什么在`initGround`和`initSnake`方法中没有用`this.setData`，而是直接设置`data`中的值

先直接给结论，那是因为在`createFood`方法中`setData`了`ground`等值，不然在屏幕上显示不出操场。

```javascript
  onLoad: function (options) {
    var maxscore = wx.getStorageSync('maxscore');
    if(!maxscore) maxscore=0
    this.setData({
      maxscore:maxscore
    });
    this.initGround(this.data.rows,this.data.cols);
    //操场渲染
    //this.initSnake(3);
    //贪吃蛇渲染
    this.createFood();
    //this.move();
  },
```
```javascript
initGround:function(rows,cols){
    //初始化操场
    //console.log([rows,cols]);

    for(var i=0;i<rows;i++){
      var arr = [];
      this.data.ground.push(arr);
      for(var j=0;j<cols;j++){
        this.data.ground[i].push(0);
      }
    }
   // console.log(this.data.ground);
  },

  initSnake:function(len){
    for(var i= 0;i<len;i++){
      this.data.ground[0][i] = 1;
      this.data.snake.push([0,i]);
      //???Todo
      //这里没有用this.setData方法来设置snake可以吗？
      //还是用对象方法是可以的？
    }
  },
createFood:function(){
    var x=Math.floor(Math.random()*this.data.rows);
    var y=Math.floor(Math.random()*this.data.cols);
    var ground = this.data.ground;
    ground[x][y] = 2;
    this.setData({
      ground:ground,
      food:[x,y]
    })
  },
```
`initGround`和`initSnake`里面是对`data`数据中的`ground`和`snake`进行改变，如果把`onLoad`中的`createFood`注释掉，可以看到渲染的效果是
![comment createFood](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-15%20at%2010.53.43%20PM.png)

**注意**这里的棕色底是`ground`的css属性，是容纳操场的“大抽屉”
```css
.ground{
    width: 660rpx;
    height:840rpx;
    margin-left: 40rpx;
    background-color: #eee4da;
}
```
而贪吃蛇的活动场地是由`block`属性控制的，背景应该为灰色。可以在视图层打印出每个操场的数组值（操场由数组控制，值是0的为灰色，值是1的是蛇体部分，值是2的是食物）
```html
 <view class="ground">
    <view wx:for="{{ground}}" class="rows" wx:for-item="cols" >
      <view wx:for="{{cols}}" class="block block_{{item}}">
      {{cols}}
      </view>
    </view>
  </view>
</view>
```
因为有`{{cols}}`理应在操场这个视图中打印出数字，但是没有，还是和上面一样。

**然后再把`createFood`注释删掉**，看到效果

![uncomment createFood](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-15%20at%2011.00.41%20PM.png)

**由此得知，并不是`initGround`和`initSnake`不用`this.setData`来设置`ground`值，而是统一在`createFood`中做了，并可以验证，`this.setData`是逻辑层和视图层的实时交互的途径，要想在视图层中显示由逻辑层控制的一些参数，必须通过`this.setData`，不然没有效果。因为蛇体其实就是`ground`的某几个值为1，而`snake`不是用来渲染视图层的，是用来后面的判断生死以及移动的，可以想成是后台的数据，所以可以不用`this.setData`来设置，而`ground`是要显示在前端的，所以必须用`this.setData`来设置**

### 触壁后蛇头位移？

详细见下面的debug部分。

原因是因为在`checkGame`中的`this.setData`函数设置后，没有即使反应在视图层，**我想的是，这个函数是及时生效**

调用流程是：

`Move` --> `changeDirection` --> `changeRight` --> `checkGame` 

在`checkGame`中`this.setData`做完后不是马上视图层生效，而是回到`changeRight`继续做剩下的，而剩下的因为没经过逻辑判断，这里可能会后bug，因为触壁后，已经到头了，理应弹出结束框，但是因为视图层没有马上生效，所以导致`changeRight`中在`checkGame`后的`ground[x][y]=1`继续执行，这个则是超出了边界。

可以做一个实验

```html
<view>{{newfield.text}}</view>
<button bindtap="addnewfield"> add new field</button>
```

```javascript
addnewfield:function(){
    this.outersetData();
    this.setData({
      "newfield.text":"here is after outersetData"
    });
  },
  outersetData:function(){
    this.setData({
      "newfield.text":"can this message display???"
    })
  }
})
```

最后结果：
![result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-20%20at%209.17.42%20AM.png)

`outersetData`中设置的，在单步调试中也没有显示过，**说明，在函数调用过程中，应该是要所有调用结束后才会触发`setData`的作用，然后视图层重新渲染**

## 初始化操场

我写的是:
```javascript
...
initGround:function(rows,cols){
    //console.log([rows,cols]);
    var arr=[];
    for(var i=0;i<rows;i++){
      this.data.ground.push(arr);
      for(var j=0;j<cols;j++){
        this.data.ground[i].push(0);
      }
    }
    console.log(this.data.ground);
  },
...
```

注意`var arr = []`写在`for`循环外面，然后在调试中看到
![initground](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-13%20at%2012.12.32%20AM.png)

这是一个异常的情况，不可能有那么多数据。

然后测试了一下
![test](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-13%20at%2012.22.45%20AM.png)
从上面的测试可以看出，虽然`g.push(arr)`是导入了4个`[]`，但当`g[0].push(1)`，做这个的时候，实际上，这4个`[]`都是引用同一个arr,也就是`arr`是“全局的”，它变，全都变。

## 事件

参考：
-[event](https://mp.weixin.qq.com/debug/wxadoc/dev/framework/view/wxml/event.html)

视图层的代码
`<view class="control" bindtouchstart="tapStart" bindtouchmove="tapMove" bindtouchend="tapEnd">
` 
当在这个视图里面发生触屏事件，这个视图的大小可能是`control`控制的，然后在里面的每一次点击滑动，都会触发相应的`tapStart`,`tapMove`,`tapEnd`函数。

与视图层的逻辑层，以`tapStart`为例，
```javascript
  tapStart:function(event){
    this.setData({
      startx:event.touches[0].pageX,
      starty:event.touches[0].pageY
    })
  },
```

我一开始怀疑为什么要event,以为是关键字，看到文档中写
> 在相应的Page定义中写上相应的事件处理函数，参数是event。

它是参数，并不是关键字。然后试了一些，把上面的`event`改为其他的名字也可以，其实就是一个命名参数`function(event=**)`这种。
这个`event`是个对象。
> 如无特殊说明，当组件触发事件时，逻辑层绑定该事件的处理函数会收到一个事件对象。

然后是`event.touches[0]`，好奇[1]是什么，这个`touches`是什么东西。
> touches 是一个数组，每个元素为一个 Touch 对象（canvas 触摸事件中携带的 touches 是 CanvasTouch 数组）。 表示当前停留在屏幕上的触摸点。

然后打印出来，
![touches](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-13%20at%202.35.49%20PM.png)
`touches`数组就一个元素，长度就为1，没有`touches[1]`。

### tapEnd


## that和this

参考：
- [ js中this和that](http://blog.csdn.net/u010289760/article/details/49968387)
- [微信小程序开发日记：重要的var that=this](http://94rn.com/hudong/201701/14123.html)
- [深入理解JavaScript中的this关键字](http://www.cnblogs.com/rainman/archive/2009/05/03/1448392.html)


## onLoad

```javascript
   changeLeft:function(){
	    ...
        this.checkGame(snakeTAIL);
		...
		this.setData({
                ground:ground,
            snake:arr
        });
		...
    },
```

```javascript
    checkGame:function(snakeTAIL){
        var arr=this.data.snake;
        var len=this.data.snake.length;
        var snakeHEAD=arr[len-1];
        if(snakeHEAD[0]<0||snakeHEAD[0]>=this.data.rows||snakeHEAD[1]>=this.data.cols||snakeHEAD[1]<0){
                clearInterval(this.data.timer);
                    this.setData({
                    modalHidden: false,
                        })  
        }
        for(var i=0;i<len-1;i++){
            if(arr[i][0]==snakeHEAD[0]&&arr[i][1]==snakeHEAD[1]){
                clearInterval(this.data.timer);
                    this.setData({
                        modalHidden: false,
                    })
            }
        }
        if(snakeHEAD[0]==this.data.food[0]&&snakeHEAD[1]==this.data.food[1]){
            arr.unshift(snakeTAIL);
            this.setData({
                score:this.data.score+10
            });
            this.storeScore();
            this.creatFood();
        }  
    },
```

```javascript
modalChange:function(){
    this.setData({
            score: 0,
        ground:[],
        snake:[],
            food:[],
            modalHidden: true,
            direction:''
    })
    this.onLoad();
    },
```


我发现一个问题，就是在`changeLeft`中（或者其他change direction），会`checkGame`，如果贪吃蛇触壁或者碰到自己的身体，那就会设置`modalHidden`值为`false`然后，因为每个`this.setData`发送都会重新渲染视图层，然后将会触发弹出框，这个弹出框的确认也会触发一个事件，`modalchange`重置。这里就有一个问题了，这一些列都是从`changeleft`的`checkGame`步骤分叉出来的，那如果重置了之后，`changeleft`中的`this.setData`还执不执行了，因为重置这一步也会执行`this.setData`，那到底是设置了哪个数据？

从结果来看，如果贪吃蛇死了，触发重置，那么`changeleft`里面的`this.setData`就不会执行了，不然，`ground`和`snake`就不是初始值了。

然后我看到了`modalchange`中有`this.onLoad()`，猜测原因应该在这里，就是重新开始服务线程。这时候一切都被销毁，重新开始，自然`changeleft`中的`this.setData`也不会再执行了。





# 其他

1. 期间调试一个`changebottom`的bug，发现怎么也没有进去这个函数，结果发现在这个定义的下面还定义了同名的函数，那个里面什么还没写，估计是之前放在哪里搭的框架。**结论：如果有同名函数，则默认是选择最新的那个，也就是最下面的那个**。


# debug
##移动轨迹渲染
- `changeleft`中
发现贪吃蛇在往左移动的时候，把移动轨迹都当作身体渲染出来了。

![errorbodymove](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-16%20at%201.01.23%20AM.png)

原因：

```javascript
    for(var i=1;i<len-1;i++){
      arr[i] = arr[i+1];
    }
```
`for`循环里面把`i`从1开始了，应该从0开始。从1开始导致arr[0]没有被覆盖

## 死了的时候，蛇头“位移”
![errorplace](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-17%20at%201.16.27%20PM.png)

可以看到背后蛇头触到最右边的时候应该死了，但是蛇头却在下一行的最左边显示了一块，然后第1列整体往下挪了。最后一行由独立的一块。

[单步调试](http://blog.csdn.net/bright789/article/details/54709594)后发现，在`changeleft`等这些函数中

```javascript
...
 var x = snakeHead[0];
    var y = snakeHead[1]+1;
    arr[len-1] = [x,y];
    //var check = this.checkGame(arr);
	this.checkGame(arr);
    //if(check){
    ground[x][y] = 1;
    //}
    this.setData({
      snake:arr,
      ground:ground
    })
...
```

当`this.checkGame(arr)`做了之后，在`checkGame`函数中，当贪吃蛇死了之后，只是把`modalHidden`设为`false`了，但是这个`this.setData`没有让视图层重新渲染，不知道为什么？？？应该这里就弹出游戏结束的框了，但是没有，而是返回到`change*`函数内，继续做`ground[x][y]=1`，然后往下继续，因为已经触到最右边，此时`y=22`，是22，不是21，21是这一行的最后一块，还没出界，22出界。但是因为在`checkGame`中没有弹出结束框，所以`ground`中有第22列了，然后在`snake.wxml`中，是根据`{{ground}}`，然后两个嵌套循环来打印出这个操场，然后这个操场的每一个块又是由`snake.wxss`来控制，因为规定了每行就是22个，这是因为660/30 = 22，决定的，也是cols=22，定义的，然后上面的`y=22`，其实是第23块，从0开始。那这时候,一行放不下，就放到下一行去了，那本来第二行还换不换行？

做了一个实验，数据量小一点。

![test](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-07-17%20at%202.55.49%20PM.png)

可以看到没有换行


# 源代码：


