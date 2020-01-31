---
layout:     post
title:      archlinux 安装 quick-init 导致根目录可读的修复
subtitle:   
date:       2010-09-17
author:     spin6lock
header-img: img/post-bg-iWatch.jpg
catalog: true
tags:
    - python
---
不得不说，Arch Linux 真的非常快！搭积木式的构建方式可以给我一种掌控感。后来听说 quick-init 可以 4 秒启动，禁不住去试试，结果。。。失败了，只好卸载之，结果根文件系统变成只读，无法上网。。。

经过一轮 google，锁定在 /etc/inittab 和 /etc/rc.conf 文件上，首先把这两个文件恢复原样。/etc 中可以看到 inittab.pacsave 或 inittab.original 的备份文件，恢复即可。

若重启依然无法解决，通常是因为把 initscripts 这个包也卸载了。如果 pacman 无法上网，则需要 minimalCD 帮忙，按照新手安装指南配置好网络，然后将 /etc/resolv.conf 复制到硬盘相应目录上，再利用硬盘的 pacman 更新解决。

现在大约 20s 就可以看到 Google 首页了，很期待新一代 chrome OS 的成绩！话说基于 suse 构建的 chrome OS 真的很慢
