---
title: vim的字符编码
date: 2017-04-10 12:43:00
categories: 砍树人
tags: [encode,utf-8]
description: 对vim中`encoding`,`filenecoding`,`fileencodings`,`termencoding`的区别做个认识

---
# vim中的编码

vim 有四个跟字符编码方式有关的选项，encoding、fileencoding、fileencodings、termencoding (这些选项可能的取值请参考 Vim 在线帮助 :help encoding-names)

- encoding: Vim 内部使用的字符编码方式，包括 Vim 的 buffer (缓冲区)、菜单文本、消息文本等。默认是根据你的locale选择.用户手册上建议只在 .vimrc 中改变它的值，事实上似乎也只有在.vimrc 中改变它的值才有意义。你可以用另外一种编码来编辑和保存文件，如你的vim的encoding为utf-8,所编辑的文件采用cp936编码,vim会自动将读入的文件转成utf-8(vim的能读懂的方式），而当你写入文件时,又会自动转回成cp936（文件的保存编码). 
- fileencoding: Vim 中当前编辑的文件的字符编码方式，Vim 保存文件时也会将文件保存为这种字符编码方式 (不管是否新文件都如此)。 
- fileencodings: Vim自动探测fileencoding的顺序列表， 启动时会按照它所列出的字符编码方式逐一探测即将打开的文件的字符编码方式，并且将 fileencoding 设置为最终探测到的字符编码方式。因此最好将Unicode 编码方式放到这个列表的最前面，将拉丁语系编码方式 latin1 放到最后面。 
- termencoding: Vim 所工作的终端 (或者 Windows 的 Console 窗口) 的字符编码方式。如果vim所在的term与vim编码相同，则无需设置。如其不然，你可以用vim的termencoding选项将自动转换成term的编码.这个选项在 Windows 下对我们常用的 GUI 模式的 gVim 无效，而对 Console 模式的Vim 而言就是 Windows 控制台的代码页，并且通常我们不需要改变它。 

最主要的就是关注一下`encoding`和`fileencoding`，总结就是前者是vim内部处理字符的用的。vim中可能会处理不一样的编码的字符，然后都化为统一的格式进行处理是最明智的。后者是文件的编码格式。

上面也说的很清楚了，文件读入时，若是`fileencoding`和`encoding`不一致，会先转化成`encoding`，统一处理，最后保存的时候再转化回`fileencoding`。转化的过程就是通过`unicode`这个第二层过渡。看[编码总结](http://www.mmmmmcclxxvii.cn/2016/10/04/encoding/)

# vim的多字符编码方式支持工作流程

1. Vim 启动，根据 `.vimrc` 中设置的`encoding` 的值来设置 buffer、菜单文本、消息文的字符编码方式。 
2. 读取需要编辑的文件，根据`fileencodings` 中列出的字符编码方式逐一探测该文件编码方式。并设置`fileencoding`为探测到的，看起来是正确的 字符编码方式。 
3. 对比`fileencoding`和`encoding`的值，若不同则调用`iconv`将文件内容转换为`encoding`所描述的字符编码方式，并且把转换后的内容放到为此文件开辟的`buffer`里，此时我们就可以开始编辑这个文件了。注意，完成这一步动作需要调用外部的`iconv.dll`，你需要保证这个文件存在于`$VIMRUNTIME`或者其他列在`PATH`环境变量中的目录里。 
4. 编辑完成后保存文件时，再次对比`fileencoding`和`encoding`的值。若不同，再次调用`iconv`将即将保存的 buffer 中的文本转换为`fileencoding`所描述的字符编码方式，并保存到指定的文件中。同样，这需要调用`iconv.dll`由于`Unicode`能够包含几乎所有的语言的字符，而且`Unicode`的`UTF-8`编码方式又是非常具有性价比的编码方式 (空间消耗比`UCS-2`小)，因此建议`encoding`的值设置为`utf-8`。这么做的另一个理由是`encoding`设置为`utf-8`时，Vim 自动探测文件的编码方式会更准确 (或许这个理由才是主要的 ;)。我们在中文 Windows 里编辑的文件，为了兼顾与其他软件的兼容性，文件编码还是设置为`GB2312/GBK` 比较合适，因此`fileencoding`建议设置为 chinese (chinese 是个别名，在 Unix 里表示 gb2312，在 Windows 里表示cp936，也就是 GBK 的代码页)。 


