---
layout:     post
title:      pysprotobug 修复
subtitle:   
date:       2016-03-25
author:     spin6lock
header-img: img/post-bg-e2e-ux.jpg
catalog: true
tags:
    - python
---
最近，找隔壁组的同学测试了一下我的 pysproto，他们提了很多有益的建议，非常感谢。

在测试中，出现了一次诡异的 coredump。当数据变大的时候，就有很大的机率遇上 double free。在 sproto 和 python sproto 插件里插了一堆打印点后，发现 sproto 在解包的时候报错了。但是 unpack 的代码相当简单，下意识忽略过去了。找云大侠看了一下数据，发现的确有个长度数据错了。至于是在哪一层出错了，还是要再找找。接着我们尝试了直接用 lua 版的 sproto 解包和打包，都没有问题。包的收发也是在单机进行的，不存在问题。于是又绕回到 unpack 上去了。仔细想想，数据越来越大的时候才会出问题。有可能跟默认缓冲区的大小有关，这个大小设置为 1024 了，难道 Realloc 的时候出错了？

放狗搜索了一下，发现 Realloc 的用法的确有问题。对于内存已满的情况，没有做出错处理，之前的指针也被覆盖掉了，造成内存泄漏。改好这一块后发现，为 sproto_unpack 传入新的缓冲区的时候，忘记更新缓冲区 dstsz 这个变量了，导致缓冲区足够大，而 sproto 会认为不够。。增加单元测试后已修复～
