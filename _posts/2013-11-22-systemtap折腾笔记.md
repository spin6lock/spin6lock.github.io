---
layout:     post
title:      systemtap折腾笔记
subtitle:   
date:       2013-11-22
author:     spin6lock
header-img: img/post-bg-keybord.jpg
catalog: true
tags:
    - python
---
在这货上花费了不少时间，都是受了@agentzh 大神的蛊惑:) 他写的nginx-systemtap-toolkit监测的数据很有价值，对于系统优化实在是利器。

最早折腾systemtap，是在Ubuntu 12.04上搞的，内核版本是3.8.0-29-generic，流程参考[官方教程](https://sourceware.org/systemtap/wiki/SystemtapOnUbuntu)。因为12.04版本比较新，所以不需要重新编译内核了。然后添加带调试信息的内核，以及相关的Linux头文件。整个过程还算顺利，就是公司网速比较慢。下载完成后，用ubuntu官方仓库自带的systemtap 1.6，却出现各种奇怪的C编译错误，于是换到了git clone下来的最新版本。这次错误信息友好了很多，但tapset的脚本跟内核的dwarf信息似乎对应不上，报semantic error: not accessible at this address [man error::dwarf]。至此，ubuntu上的systemtap只能打出hello world，其他脚本都跑不了，遂放弃。教训是，systemtap要新版，内核要老版，若用老systemtap和新内核，一般是会挂的。

对systemtap的用户态监控还是很口水，虽然我司用的是自己写的定制语言，但是-g编译后应该可以监控私有语言的脚本栈，进而分析性能瓶颈。于是，死皮赖脸抢夺了一台CentOS的机器做测试。机器版本如下：

```
[root@localhost systemtap]# uname -rm
2.6.32-279.el6.x86_64 x86_64
　
[root@localhost systemtap]# cat /etc/redhat-release
CentOS release 6.3 (Final)
```

用的systemtap版本是最新的。跟Ubuntu相比，CentOS的包管理就比较差了，内核的调试信息包需要自己手动下载安装。参考[官方教程](https://sourceware.org/systemtap/wiki/SystemTapOnCentOS)，安装debuginfo-common和debuginfo后，就可以开搞了。还好，这次不需要编译内核。安装好systemtap后，跑起来却出现这个问题：

提示：

Checking "/lib/modules/2.6.32-279.el6.x86_64/build/.config" failed with error: 没有那个文件或目录

检查了一下相关的目录，/lib/modules/2.6.32-279.el6.x86_64/是一个软连接，链接到/usr/src/kernels/里去的。而2.6.32-358.23.2.el6.x86_64这个目录是真的没有，有的是2.6.32-358.23.2.el6.x86_64。谷歌了一下，这个目录是kernel-devel包的，通过yum安装的是最新的2.6.32-358.23.2.el6.x86_64，跟当前运行的内核不符。继续放狗，找到2.6.32-279.el6.x86_64的kernel-devel rpm包，安装完就有对应目录了。试了一下iotop终于成功了。

看了一下，systemtap似乎是根据写的probe编译成二进制模块，加载到内核里执行的。所以systemtap会在home目录下建立一个cache目录，避免重复编译相同的脚本。而nginx-systemtap-toolkit对Lua的栈探测，是通过监视LuaL开头的函数实现的，接下来准备按他的思路搞一下我们的私有语言。
