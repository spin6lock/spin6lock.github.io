---
layout:     post
title:      Mongodb 在 NUMA 机器上的优化
subtitle:   
date:       2013-11-15
author:     spin6lock
header-img: img/post-sample-image.jpg
catalog: true
tags:
    - python
---
10gen 在 mongodb 的部署指南上，提到了在 NUMA 机器上，mongodb 可能会出现问题，参见：http://docs.mongodb.org/manual/administration/production-notes/#production-numa

里面引用了一篇博客，主要讲 MySQL 的 swap insanity，而 mongodb 也会遇到类似的问题，博客地址：http://blog.jcole.us/2010/09/28/mysql-swap-insanity-and-the-numa-architecture/。

这篇博客有点长，我这里简单概括一下。

对于单 CPU，多核心的情况，每个核心访问内存的速度是一样的，这种架构称为 SMP（Symmetric multiprocessing， 对称多处理器），又叫 UMA(Uniform Memory Architecture，与 NUMA 相对，一致性内存访问架构 )。

对于多 CPU，多核心的情况，如下图：

<img title="NUMA，图片来自 https://computing.llnl.gov/tutorials/linux_clusters/" src="https://computing.llnl.gov/tutorials/linux_clusters/images/motherboard1.jpg" alt=" 多 CPU 主板 " width="304" height="358" />

可以看到，每个 CPU 都有一组配套的内存槽。每个 CPU 访问自身的内存插槽，速度都很快，但对于主板上的其他内存插槽，访问速度就会下降。这种架构被称为 NUMA。

对于 Linux 来说，加载的时候就会检测内存，计算 CPU 到内存的访问开销，将 CPU 和内存分成一组组的。每个进程和线程，都会继承父进程的 NUMA 策略，这种策略包括这个进程 / 线程会在哪个 CPU 上运行，分配的内存应该用哪组插槽的。

面对内存分配，只要一经分配到指定的 CPU 内存槽，就不会再挪动了。对于数据库这类应用，理想情况下是一个单一的多线程进程，吃掉了几乎所有的系统内存，并尽可能多的消耗其余的系统资源例如 IO。

对于两个 CPU 的 NUMA 架构来说，如果一个核心分配的内存超过系统内存的一半，就会出现问题。而 Linux 的分配策略是，首先使用 CPU 0，然后再使用 CPU 1。这时候就会出现一种情况，CPU 0 的内存组已经率先使用完了，但系统还有很多空闲内存，都在 CPU 1 上。这时候，Linux 会选择将 CPU 0 的内存刷到磁盘上，以换取可用内存。但是，swap 过程远比跨 CPU 访问内存要慢啊。这就会造成内存还没用光，但数据库疯狂刷盘的现象了。

解决办法是用 numactl 指定分配策略，将数据库需要的内存分散在各个 CPU/ 内存组上，保证不会出现一个核心已满而另一个核心空闲的情况。

```
#numactl --interleave all command
```
