---
layout:     post
title:      StandardML 语言（一）
subtitle:   
date:       2010-02-06
author:     spin6lock
header-img: img/post-bg-kuaidi.jpg
catalog: true
tags:
    - python
---
在 Windows 平台下推荐使用 Moscow ML 解释器，主要是安装比较方便，其他有 Standard ML of New Jersey, 安装后需要设置环境变量（即 bin 目录所在位置）。

要引用系统模块，请使用 load "module", 例如：

-load "Math"; 

-Math 4.0;

函数名后需要空一格。

从 C/C++ 语言转来的同学，请多多练习 andalso 与 orelse，另外，条件表达式

　　　　　　　　　　if E then E1 else E2 

else 部分必须存在（即 else 需要严格匹配，一个 if 对应一个 else）。

附上 ML 程序设计教程 [ 课后习题答案 ](http://files.cnblogs.com/Lifehacker/exercises.7z)<a></a>
