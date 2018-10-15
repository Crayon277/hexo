---
title: 能不能一笔连成线
date: 2018-03-05 22:58:41
categories: C
tags: [c,algorithm]
description: 是图的遍历问题
photos:
- http://onexs3cnv.bkt.clouddn.com/WechatIMG127.jpeg

---

最终如果能一笔连成线，说明是都遍历到了。那从一个点开始，遍历就是找邻近的点，看看这个邻近的点合不合法

- 有没有越过边界
- 有没有被之前遍历过
- 是不是绿点

都合法在从这个邻近的点找它的邻近的点。
伪代码

```
next(点):
	if 找满了24个点:
		打印路径，退出
	for 该点的邻近点们:
		如果该点合法:
			保存轨迹
			next(邻近点)
			删除轨迹
```

代码：

```C
/*************************************************************************
	> File Name: solve.c
	> Author: Crayon Chaney
	> Mail:mmmmmcclxxvii@gmail.com
	> Created Time: Mon Mar  5 20:45:25 2018
 ************************************************************************/

#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

typedef struct route{
	int stack[24][2];
	int top;
}ROUTE;
int total = 24;
ROUTE path;

int flag = 0;

void print_path(){
	int top = path.top; //有可能还有其他解法，要保留这个path.top
	flag = 1;
	while(top >= 0){
		printf("(%d,%d) --> ", path.stack[top][0],path.stack[top][1]);
		top --;
	}
	printf("\n\n\n");
}

int Already_exist(x,y){
	for(int i = 0; i <= path.top;i++){
		if(x == path.stack[i][0] && y == path.stack[i][1]){
			return 1;
		}
	}
	return 0;
}

int valid(x,y){
	if(x<0 || y<0 || x>4 || y > 4 || (x == 0 && y == 1)){
		return 0;
	}
	if(Already_exist(x,y)){
		return 0;
	}
	return 1;
}

void save_route(x,y){
	path.top ++;
	path.stack[path.top][0] = x;
	path.stack[path.top][1] = y;
}

void clean_route(x,y){
	path.top --;  //退栈
}

void next(int x, int y,int count){  //先把框架搭好
	/* printf("pass,%d,(%d,%d),%d\n",count,x,y,path.top); */
	/* getchar(); */
   if( 24 == count && 23 == path.top){ //最后bug出现在这里 24 == path.top ，从0 开始
	   print_path();
	   return;
   }
   for(int i = -1;i<=1;i+=2){
		if(valid(x+i,y)){
			save_route(x+i,y);
			next(x+i,y,count+1);
			clean_route(x+i,y);
		}
   }
   for(int i = -1;i<=1;i+=2){
		if(valid(x,y+i)){
			save_route(x,y+i);
			next(x,y+i,count+1);
			clean_route(x,y+i);
		}
   }
   //这里的遍历邻近点还有没有更好的写法呢？？？
}

int main(){
	path.top = 0;
	int start_x=0,start_y = 0;
	path.stack[0][0] = start_x;
	path.stack[0][1] = start_y;
	next(start_x,start_y,1);
	if(!flag){
		printf("no solution!\n");
	}
	return 0;
}

```

有些语法忘了，全局变量结构体，一开始`path.top=0`放在主函数外面报错，可能python写多了，总觉得会执行到。但这个赋值一定要在函数体内，全局变量`int total = 24`这个是初始化！！！

