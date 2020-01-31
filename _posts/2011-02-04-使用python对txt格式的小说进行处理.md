---
layout:     post
title:      使用 python 对 txt 格式的小说进行处理
subtitle:   
date:       2011-02-04
author:     spin6lock
header-img: img/post-bg-digital-native.jpg
catalog: true
tags:
    - python
---
vim 的确是神器，可惜 sed 与 vim 不完全通用。这篇文章受<a href="http://hi.baidu.com/%C8%CB%BC%E4%CA%C0%E5%D0%D2%A3%D3%CE/blog/item/51f5ec1db41cffe51bd57630.html">《
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
用 vim 对 txt 格式的小说重新排版》</a>的启发，在此致谢！

经常下载 txt 的电子书，格式却不合心意，只好自己再处理。首要的就是处理段内换行。

原来的打算是定制一个 vim 模式，到时候处理小说时进入该模式，再使用各种快捷键。以此避免 txt 快捷键对日常编程的干扰。后来发现，vim 不像 emacs，可以定制自己的模式。（可能可以定制专用的 vimrc 解决，未经尝试）

于是转向脚本寻求解决办法。sed 与 awk 是此中翘楚，首先试试。可惜早些日子学的 sed 已经忘的差不多了，找不到比较简洁清晰的解决办法。sed 与 grep 类似，先读入一行，删除 \n，进行各种处理，最后写入文件，再添上 \n。 N 可以读入下一行到当前模式匹配空间再行处理。但是我需要对整个文件进行匹配，暂时未找到解决办法。

只好再次转投 python。Python 有自己的 re 模块，应该没问题。re.sub 可以进行替换。费了些时间的，是对中文的匹配。在 vim 中，可以用 [^\x00-\xff] 匹配双字节字符，然而 python 中却行不通。经过一番 google，发现可以用 [\x80-\xff] 匹配汉字（perl 同此，似乎两者对中文的正则支持还是有待改进）。

至此，问题初步解决：



<pre class="brush:python">#!/usr/bin/env python
#encoding=utf-8
import re
from sys import argv


if __name__ == '__main__':
	if len(argv) != 2:
		print 'usage: filename'
	else:
		fh = open(argv[1], 'r')
		content = fh.read()
		out = re.sub('\n([\x80-\xff])', r'\1', content)
		print out
</pre>



规范行首：



<pre class="brush:python">#!/usr/bin/env python
#encoding=utf-8
import re
from sys import argv


if __name__ == '__main__':
	if len(argv) != 2:
		print 'usage: filename'
	else:
		fh = open(argv[1], 'r')
		content = fh.read()
		out = re.sub(' +([\x80-\xff])', r'     \1', content)
		print out
</pre>



当然，下载来的文档通常是 GB2312，需要自己转换为 utf8 再行处理，可以参考我的 [《python 中文编码笔记》](http://www.cnblogs.com/Lifehacker/archive/2010/08/10/python_encode_decode.html)

在 win 下，有个优秀的文本处理工具可以利用，叫 cnbook。在百度的 fmddlmyy 贴吧可以下载到最新版本。
