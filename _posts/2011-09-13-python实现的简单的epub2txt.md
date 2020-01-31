---
layout:     post
title:      python 实现的简单的 epub2txt
subtitle:   
date:       2011-09-13
author:     spin6lock
header-img: img/post-bg-desk.jpg
catalog: true
tags:
    - python
---
等了 1 年，还是没等到台电 k6 的固件更新，好失望。

由于 k6 不支持 epub 的目录跳转、内嵌字体，且每次阅读均需要重新解压 epub，既浪费电又浪费时间，因此干脆转成 txt 算了。 

先用 zipfile 进行解压

然后用 HTMLParser 进行正文提取

最后输出同名 txt 

代码在 [http://code.google.com/p/yaepub2txt ](http://code.google.com/p/yaepub2txt) 上托管，google code 上的另外一个 epub2txt 似乎也是国内的兄弟写的，是基于 html2txt 的库和 xml 解析做的，我懒，直接解压，读 html 文件了事了 B-)
