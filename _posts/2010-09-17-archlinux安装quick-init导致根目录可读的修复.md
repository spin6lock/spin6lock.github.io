---
layout:     post
title:      archlinux安装quick-init导致根目录可读的修复
subtitle:   
date:       2010-09-17
author:     Mehaei
header-img: img/post-bg-iWatch.jpg
catalog: true
tags:
    - python
---
不得不说，Arch Linux真的非常快！搭积木式的构建方式可以给我一种掌控感。后来听说quick-init可以4秒启动，禁不住去试试，结果。。。失败了，只好卸载之，结果根文件系统变成只读，无法上网。。。

经过一轮google，锁定在/etc/inittab和/etc/rc.conf文件上，首先把这两个文件恢复原样。/etc中可以看到inittab.pacsave或inittab.original的备份文件，恢复即可。

若重启依然无法解决，通常是因为把initscripts这个包也卸载了。如果pacman无法上网，则需要minimalCD帮忙，按照新手安装指南配置好网络，然后将/etc/resolv.conf复制到硬盘相应目录上，再利用硬盘的pacman更新解决。

现在大约20s就可以看到Google首页了，很期待新一代chrome OS的成绩！话说基于suse构建的chrome OS真的很慢
