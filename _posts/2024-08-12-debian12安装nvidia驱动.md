---
layout:     post
title:      "debian12安装nvidia驱动"
subtitle:   ""
date:       2024-08-12
author:     "spin6lock"
catalog:    true
tags:
- debian
- nvidia
- operating system
---

事缘公司使用4年的台式机可以自购了，第一时间买回家准备搞本地大模型。奈何死活装不上NVIDIA驱动，搞的我都emo了。最近娃丢回老家了，正好有空研究一下

显卡驱动需要编译后加载到内核中，而Intel牵头搞的SecureBoot则通过主板固件检查内核是否被篡改，通过SecureBoot启动的内核，也会同步校验内核模块是否签名，未签名的模块就禁止加载。原理大概就是这样，但是debian官方教程没解释，基本就是让apt装个nvidia-driver的包就完事了……看了很多教程都是在纠结Nonveau的屏蔽上，这次发现其实官方已经都弄好了的。建议参考[这篇教程](https://tigress.cc/2023/09/18/Debian-Nvidia/)[时光机](http://web.archive.org/web/20240523004027/https://tigress.cc/2023/09/18/Debian-Nvidia/)，我自己是直接关掉内核签名检查来解决的，这个教程比较细致，是导入mok(Machine Owner Key)来做签名的，感觉会比较好。

但是，顺序很重要！装了nvidia的包以后，才生成了mok来给我们导入mokutil，而导入不是一次性的，需要重启后打密码确认的，那个界面依赖图形驱动，而nvidia驱动这时候还没有签名，不能启动，死循环了，所以我只好关SecureBoot了……供参考

当然用Nvidia官方的教程应该也可以，但是用nvidia的教程最好先固化内核版本，他那个不会随着内核升级而升级，内核接口改了就容易挂
