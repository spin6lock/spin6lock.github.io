---
layout:     post
title:      python实现的简单的epub2txt
subtitle:   
date:       2011-09-13
author:     Mehaei
header-img: img/post-bg-desk.jpg
catalog: true
tags:
    - python
---
等了1年，还是没等到台电k6的固件更新，好失望。

由于k6不支持epub的目录跳转、内嵌字体，且每次阅读均需要重新解压epub，既浪费电又浪费时间，因此干脆转成txt算了。 

先用zipfile进行解压

然后用HTMLParser进行正文提取

最后输出同名txt 

代码在 [http://code.google.com/p/yaepub2txt ](http://code.google.com/p/yaepub2txt)上托管，google code上的另外一个epub2txt似乎也是国内的兄弟写的，是基于html2txt的库和xml解析做的，我懒，直接解压，读html文件了事了B-)
