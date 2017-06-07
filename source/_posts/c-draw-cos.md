---
title: c_draw_cos
date: 2015-06-02 08:33:38
update: 2015-06-02 08:33:38
categories: C
tags: [C-practice]
description: 在屏幕上用“*”显示0～360的余弦函数cos(x)的曲线。
photos:
- http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-02%20at%208.33.50%20AM.png

---

c的控制台程序打印是逐行打印。所以每一行都要一次性计算出所有*的位置。其实就是找规律
主要就是两个循环，一个是纵轴的，一个是横轴的，纵轴方向控制行，横轴方向控制打印*
`cos`这个函数是对称的.周期是0~2pi,pi是3.1415，所以横轴方向的长度是2pi，也就是6.28，
纵轴方向可以通过一个for循环从1到-1,通过acos反三角函数计算出横轴。为了显示方便可以放大倍数
因为是对称，每行两个*的横坐标是关于pi对称的。

```c
void draw_cos(){
    double y;
    int m,x;
    for(y=1;y>=-1;y-=0.1){
        x = acos(y)*10; //这里和下面的62-x的62是对应的。放大的倍数
        for(m = 1;m<x;m++) printf(" ");
        printf("*");
        for(;m<62-x;m++) printf(" "); //其实62表示的就是总的宽度
        printf("*\n");
    }
}
```

如果放大了20倍，而宽度还是62的话。
```c
x = acos(y) * 20
```
![wrong_result](http://onexs3cnv.bkt.clouddn.com/Screen%20Shot%202017-06-02%20at%2011.46.38%20AM.png)

可以看到，当x计算出来的超过了31（对称线）的时候，因为m这个循环变量也已经超过31，`m < 62 - x`这个控制语句已经不起作用了，所以就不正确了。
当要放大20倍的时候，宽度也要相应的放大2倍。
