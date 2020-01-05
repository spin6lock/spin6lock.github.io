---
layout:     post
title:      Mongodb在NUMA机器上的优化
subtitle:   
date:       2013-11-15
author:     Mehaei
header-img: img/post-sample-image.jpg
catalog: true
tags:
    - python
---
10gen在mongodb的部署指南上，提到了在NUMA机器上，mongodb可能会出现问题，参见：http://docs.mongodb.org/manual/administration/production-notes/#production-numa

里面引用了一篇博客，主要讲MySQL的swap insanity，而mongodb也会遇到类似的问题，博客地址：http://blog.jcole.us/2010/09/28/mysql-swap-insanity-and-the-numa-architecture/。

这篇博客有点长，我这里简单概括一下。

对于单CPU，多核心的情况，每个核心访问内存的速度是一样的，这种架构称为SMP（Symmetric multiprocessing， 对称多处理器），又叫UMA(Uniform Memory Architecture，与NUMA相对，一致性内存访问架构)。

对于多CPU，多核心的情况，如下图：

<img title="NUMA，图片来自 https://computing.llnl.gov/tutorials/linux_clusters/" src="https://computing.llnl.gov/tutorials/linux_clusters/images/motherboard1.jpg" alt="多CPU主板" width="304" height="358" />

可以看到，每个CPU都有一组配套的内存槽。每个CPU访问自身的内存插槽，速度都很快，但对于主板上的其他内存插槽，访问速度就会下降。这种架构被称为NUMA。

对于Linux来说，加载的时候就会检测内存，计算CPU到内存的访问开销，将CPU和内存分成一组组的。每个进程和线程，都会继承父进程的NUMA策略，这种策略包括这个进程/线程会在哪个CPU上运行，分配的内存应该用哪组插槽的。

面对内存分配，只要一经分配到指定的CPU内存槽，就不会再挪动了。对于数据库这类应用，理想情况下是一个单一的多线程进程，吃掉了几乎所有的系统内存，并尽可能多的消耗其余的系统资源例如IO。

对于两个CPU的NUMA架构来说，如果一个核心分配的内存超过系统内存的一半，就会出现问题。而Linux的分配策略是，首先使用CPU 0，然后再使用CPU 1。这时候就会出现一种情况，CPU 0的内存组已经率先使用完了，但系统还有很多空闲内存，都在CPU 1上。这时候，Linux会选择将CPU 0的内存刷到磁盘上，以换取可用内存。但是，swap过程远比跨CPU访问内存要慢啊。这就会造成内存还没用光，但数据库疯狂刷盘的现象了。

解决办法是用numactl指定分配策略，将数据库需要的内存分散在各个CPU/内存组上，保证不会出现一个核心已满而另一个核心空闲的情况。

```
#numactl --interleave all command
```
