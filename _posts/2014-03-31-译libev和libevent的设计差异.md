---
layout:     post
title:      译 libev 和 libevent 的设计差异
subtitle:   
date:       2014-03-31
author:     spin6lock
header-img: img/post-bg-debug.png
catalog: true
tags:
    - python
---
本文译自 [what's the difference between libev and libevent?](http://stackoverflow.com/questions/9433864/whats-the-difference-between-libev-and-libevent) 作者是 libev 作者

[ 问 ] 两个库都是为异步 io 调度而设计，在 Linux 上都是使用 epoll 机制，在 FreeBSD 上则都是 kqueue，还有诸如此类的很多相通之处。

除了这些表面上的差别外，其实这两者根本的区别在哪里呢？比如架构上，或者设计哲学上。

[ 答 ] 就设计哲学来说，libev 的诞生，是为了修复 libevent 设计上的一些错误决策。例如，全局变量的使用，让 libevent 很难在多线程环境中使用。watcher 结构体很大，因为它们包含了 I/O，定时器和信号处理器。额外的组件如 HTTP 和 DNS 服务器，因为拙劣的实现品质和安全问题而备受折磨。定时器不精确，而且无法很好地处理时间跳变。

libev 试图改进所有这些缺陷，例如避免使用全局变量，转而在所有函数中，使用上下文变量来代替。每个事件类型，使用单独的 watcher 类型（一个 I/O watcher 在 64 位机器上，只需要 56 字节。而 libevent 需要 136 字节）。允许额外的事件类型，例如基于挂钟的计时器，或者单调时间，线程内中断，准备并检查 watchers 来嵌入其他事件循环，或者被用于其他事件循环来嵌入。

额外组件的问题，是通过直接去掉额外组件来解决的，这样 libev 就可以小而美，快速高效了。但你也需要从其他地方寻找 http 库。因为 libev 没有带上。（例如，有一个库叫 libeio，可以完成异步 IO 的工作，也可以和 libev 配合使用 )。

总而言之，libev 试图做好一件事而已（目标是成为 POSIX 的事件库），这是最高效的方法。libevent 则尝试给你全套解决方案（事件库，非阻塞 IO 库，http 库，DNS 客户端）

一句话总结，libev 尝试追随 UNIX 工具箱哲学，一次只干一件事，每次都做到最好。

注意，这是 libev 的设计哲学，我想我作为 libev 的设计者，有着足够的发言权。至于这些设计目标有没有实际达到，或者这些设计哲学是否坚实可靠，则交由你来评判。

[ 译者注 ] 第一次注意到 libev，是在 gevent 的开发者 blog 上的这篇 [libev and libevent](http://blog.gevent.org/2011/04/28/libev-and-libevent/)，它简要说明了 gevent 从 libevent 切换到 libev 的决策过程。回顾 gevent，它实际需要的只是一个负责事件循环的 C 库，在上面的 HTTP 库和 DNS 库，都可以交由标准库强大得不得了的 python 完成。因此，作者的选择还是非常明智的。

从 Libevent 2.0 来看，libevent 团队已经意识到上述的问题，也提取出了 event loop 这个上下文 context，但是在具体的 DNS 解析，HTTPS 连接等等，还是有种力不从心的感觉。作为 libevent 的使用者，我们经历了 libevent 的试错阶段，发现 HTTPS 实现不行，再切换到 libcurl 去，与其这样，倒不如直接不提供该功能呢
