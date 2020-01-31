---
layout:     post
title:      银行家算法（Thebanker'salgorithm)
subtitle:   
date:       2009-09-28
author:     spin6lock
header-img: img/post-bg-alibaba.jpg
catalog: true
tags:
    - python
---1. 已被进程占用 1. 进程资源需求最大值 1. 系统可用资源 1. 有 A、B 两进程，当前可用资源无法满足任一进程的需要，但 A 在运行时暂时释放了所占用的资源，使得 B 得以结束，从而释放更多资源，使得 A 顺利结束。1. 有 A、B、C 三个进程，当前资源可以满足 A 的运行需要，因此此时 A 并没有陷入死锁。