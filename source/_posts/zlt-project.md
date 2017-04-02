---
title: zlt-project
date: 2017-03-01 10:24:31
categories: python
tags: [python,project,Tkinter]
description: 章礼腾要我做的一个程序，他需求是，有AB两个文件夹，我想通过B文件夹中文件的文件名将A文件夹中相同文件名的文件复制到B文件夹

---

最近一直在用python写，这个也用python试试。需求图示
![demands](http://onexs3cnv.bkt.clouddn.com/demands.jpeg)

用到：
- 正则表达式：用来匹配test.py中的test名的
- shutil模块，shutil.copy复制
- os模块，切换目录用的。os.listdir,os.path.isfile等
- sys模块，sys.argv命令行参数
- Tkinter，图形化界面

---

# 主要的拷贝逻辑写出来

```python
import re
import os
import shutil
import sys

path_a = sys.argv[1]
path_b = sys.argv[2]

candidate_list = [x for x in os.listdir(path_b) if os.path.isfile(x) and x[0]!='.']
p = re.compile('\w+')
candidate = [p.match(file_name).group() for file_name in candidate_list]
#先把B文件中的文件名提取出来

for prefix in candidate:
	for every_file in os.listdir(path_a):
		if predix in every_file:
			file_path = path_a + '/' + every_file
			shutil.copy(file_path,path_b)
			print 'copy %s to %s'%(every_file,path_b)
```

接下来就是披上一件外衣了，Tkinter。![思维导图](http://onexs3cnv.bkt.clouddn.com/mind-map-project-zlt.png)
下面是代码

# `zlt_main_frame_listbox.py` 这个是显示文件夹功能的窗口
```python
#!/usr/bin/python
#-*- coding: utf-8 -*-
# File Name: zlt.py
# Created Time: Sun Mar  5 21:56:03 2017

__author__ = 'Crayon Chaney <mmmmmcclxxvii@gmail.com>'

import os
from Tkinter import *
from time import sleep
import pdb


class ShowList(Frame):
    # count = 0
    def __init__(self,parent,initdir=None):
        # super(ShowList,self).__init__(parent)
        """
        上面这个为什么不行？？？
        """
        Frame.__init__(self,parent)
        
        self.parent = parent

        self.cwd = StringVar(self)
        self.wholecwd = StringVar(self) 
        self.dir_display = Label(self,font = ('Helvetica',12,'bold'),fg = 'blue')
        self.dir_display.pack()

        self.dirfm = Frame(self)
        self.dirsb_y = Scrollbar(self.dirfm)
        self.dirsb_x = Scrollbar(self.dirfm,orient="horizontal")
        self.dirlb = Listbox(self.dirfm,yscrollcommand = self.dirsb_y.set,xscrollcommand = self.dirsb_x.set,height =20,width = 30 )
        self.dirsb_y.config(command = self.dirlb.yview)
        self.dirsb_x.config(command = self.dirlb.xview)

        self.dirlb.bind('<Double-1>',func=self.selectAndGo)

        self.dirsb_y.pack(side = RIGHT,fill=Y)
        self.dirsb_x.pack(side = BOTTOM,fill=X)
        self.dirlb.pack(side=LEFT,fill=BOTH)
        
        self.dirfm.pack()

        self.input = Entry(self,textvariable=self.cwd)
        self.input.bind('<Return>',func = self.doLs)
        self.input.pack()

        self.dirbuttonfm = Frame(self)
        
        self.clrbutton = Button(self.dirbuttonfm,text='clear',command=self.clrEntry)
        self.clrbutton.pack(side=LEFT)
        self.listbutton = Button(self.dirbuttonfm,text='List Directory',command=self.doLs)
        self.listbutton.pack(side=LEFT)

        self.dirbuttonfm.pack()

        if initdir:
            self.cwd.set(initdir)
            self.doLs()


    def clrEntry(self,ev = None):
        self.cwd.set('')

    def selectAndGo(self,ev=None):
        self.last = self.cwd.get()
        self.dirlb.config(selectbackground='red')
        self.cwd.set(self.dirlb.selection_get())
        self.doLs()

    def doLs(self,ev = None):
        cur = self.cwd.get()
        error = ''
        if not os.path.exists(cur):
            error = '%s is not exists'%cur
        elif not os.path.isdir(cur):
            error = "%s is not dir"%cur

        if error:
            self.cwd.set(error)
            self.parent.update()
            sleep(2)
            if not (hasattr(self,'last') and self.last):
                self.last = os.curdir
            self.cwd.set(self.last)
            self.dirlb.config(selectbackground='LightSkyBlue')
            return

        self.cwd.set('Fetching...')
        self.parent.update()

        dirfiles = os.listdir(cur)
        os.chdir(cur)

        self.dir_display.config(text=os.getcwd())
        self.wholecwd.set(os.getcwd())
        dirfiles.sort()
        self.dirlb.delete(0,END)
        self.dirlb.insert(END,os.curdir)
        self.dirlb.insert(END,os.pardir)

        for eachdirname in dirfiles:
            self.dirlb.insert(END,eachdirname)

        self.cwd.set(os.curdir)
        self.dirlb.config(selectbackground='LightSkyBlue')

if __name__ == '__main__':
    root = Tk()
    ShowList(root,os.curdir).pack()
    root.mainloop()
```

# `zlt_windows.py` 主窗口
```python
#!/usr/bin/python
#-*- coding: utf-8 -*-
# File Name: zlt_windows.py
# Created Time: Mon Mar  6 14:13:52 2017

__author__ = 'Crayon Chaney <mmmmmcclxxvii@gmail.com>'

from zlt_main_frame_listbox import *
import shutil
import re
import sys

class CopyDir(object):
    def __init__(self):
        self.top = Tk()
        self.top.title('你花大爷呕心沥血作')

        # ShowList(self.top).pack(side=LEFT)
        self.A = ShowList(self.top,os.curdir)
        self.A.pack(side=LEFT)
        self.topbuttonfm = Frame(self.top)
        self.copybutton = Button(self.topbuttonfm,text='<--A  copy  B-->',width = 15,command = self.confirmCopy)
        self.copybutton.pack()
        self.quitbutton = Button(self.topbuttonfm,text='退出',command = self.top.quit)
        self.quitbutton.pack()
        self.topbuttonfm.pack(side = LEFT,ipadx = 5)
        # ShowList(self.top).pack(side=LEFT)
        self.B = ShowList(self.top,os.curdir)
        self.B.pack(side=LEFT,ipadx = 5)


    def confirmCopy(self,ev = None):
        self.confirmtop = Toplevel(self.top)

        # pdb.set_trace()

        self.a_path =  self.A.wholecwd.get()
        self.b_path = self.B.wholecwd.get()
        
        listfiles_a = os.listdir(self.a_path)
        listfiles_b = os.listdir(self.b_path)
        
        title_msg = '复制这些到%s'%self.b_path
        self.confirmtop.title(title_msg)

        # self.fm = Frame(self.confirmtop) # to be pack
        self.copy_candidates_info = Text(self.confirmtop,height=30,width = 20) # to be pack
        
        pattern = re.compile('\w+')
        self.to_be_copied_list = []
        for to_be_copied in listfiles_b:
            try:
                prefix = pattern.match(to_be_copied).group()
            except AttributeError,e:
                continue
                # print e
                # if 'NoneType' in e:
                    # continue
                # else:
                    # sys.exit()
            for eachfile in listfiles_a:
                if prefix in eachfile :# and os.path.isfile(self.a_path+'/'+prefix): 可能在windows下不支持
                    self.to_be_copied_list.append(eachfile)

        # self.copy_candidates_info.delete(0,END)
        for item in self.to_be_copied_list:
            self.copy_candidates_info.insert(END,item+'\n') # window下换行符可能不一样 \r\n

        self.copy_candidates_info.pack(side = LEFT,padx = 10)

        information = 'copy to %s'%self.b_path
        self.other_information = Label(self.confirmtop,text = information)
        self.other_information.pack(side=LEFT,ipadx = 5,ipady = 13)

        self.fm = Frame(self.confirmtop)
        self.result_info = Label(self.fm,font = ('Helvetica',12,'bold'),fg='red')
        self.confirmbutton = Button(self.fm,text='确认',command = self.copyExecute)
        self.cancelbutton = Button(self.fm,text='取消',command = self.confirmtop.quit)
        """
        为什么点击取消会全体退出？？？ 想要的效果是只是这个确认窗口退出而已
        """
        self.result_info.pack(side=LEFT)
        self.confirmbutton.pack(side = LEFT)
        self.cancelbutton.pack(side=LEFT)
        self.fm.pack(side = BOTTOM)


    def copyExecute(self,ev=None):
        os.chdir(self.a_path)
        if not (hasattr(self,'to_be_copied_list') and len(self.to_be_copied_list)):
            self.result_info.config(text='Failed')
            return 
        for item in self.to_be_copied_list:
            try:
                shutil.copy(item,self.b_path)
            except Exception,e:
                self.result_info.config(text=e)
            else:
                self.result_info.config(text='Successful')
            
def main():
    c = CopyDir()
    mainloop()

if __name__ == '__main__':
    main()
```

# 发现的bug：
1. 因为我现在是在一个窗口生成了两个文件夹展示的frame，但是在一个进程中，一个文件夹切换了路径，另一个就跟着切换了导致出现bug，解决方法，要用多线程

