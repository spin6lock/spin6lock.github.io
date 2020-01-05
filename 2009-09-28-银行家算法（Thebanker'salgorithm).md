---
layout:     post
title:      银行家算法（Thebanker'salgorithm)
subtitle:   
date:       2009-09-28
author:     Mehaei
header-img: img/post-bg-alibaba.jpg
catalog: true
tags:
    - python
---1. 已被进程占用1. 进程资源需求最大值1. 系统可用资源1. 有A、B两进程，当前可用资源无法满足任一进程的需要，但A在运行时暂时释放了所占用的资源，使得B得以结束，从而释放更多资源，使得A顺利结束。1. 有A、B、C三个进程，当前资源可以满足A的运行需要，因此此时A并没有陷入死锁。