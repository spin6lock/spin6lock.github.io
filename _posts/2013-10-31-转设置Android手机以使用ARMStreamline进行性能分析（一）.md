---
layout:     post
title:      转设置Android手机以使用ARMStreamline进行性能分析（一）
subtitle:   
date:       2013-10-31
author:     spin6lock
header-img: img/post-bg-mma-6.jpg
catalog: true
tags:
    - python
---
##  

- Streamline 5.7版。Streamline是[ARM Development Studio 5](http://www.arm.com/zh/products/tools/software-tools/ds-5/index.php)的一个组成模块。因此，可通过下载[ARM DS-5](http://www.arm.com/zh/products/tools/software-tools/ds-5/ds-5-downloads.php)专业版、基础版或免费的DS-5公众版（针对Android系统）来获得它。
<li>目标ARM设备，HTC Sensation 4G
<ul class="bbc">
- [Qualcomm Snapdragon ](http://www.arm.com/zh/markets/mobile/qualcomm-snapdragon-chipset.php)1.2-GHz双核处理器，ARMv7架构
- Android 2.3.4版
- Linux内核2.6.35.13版


- HTC手机的内部代码。如果是HTC sensation 4G手机，那么内部代码是图中红框标示的PYRAMID。内部代码是HTC Android手机的标识，通过它可搜索到HTC发布的正确Linux内核源代码包。
- 安全锁的状态。目前我这台手机的安全锁状态为S-OFF（安全锁关闭），在图1中用红框标示。安全锁对实现本文目的十分重要。S-OFF表示设备的NAND Flash ROM处于解锁状态并且可写，这也就意味着无需进行签名检查就可以更新Android系统的某些分区；例如，通过自定义镜像文件来更新启动分区。HTC设备的默认设置为S-ON，这表示只能使用HTC官方的固件镜像文件来更新系统（因为启用了签名检查）。


- 在x86 PC上运行的64位Ubuntu 10.10 版本
- Linux系统下的GNU ARM Toolchain，本文所使用的是下载自[Mentor Graphics](https://sourcery.mentor.com/sgpp/lite/arm/portal/release1803).的CodeSourcery ARM GNU/Linux Toolchain。
- 从[Android开发者网站](http://developer.android.com/sdk/index.html)下载的Android SDK r16-linux安装程序。
- 通过Android SDK r16-linux安装程序下载安装的Android SDK平台工具包
- USB电缆 电缆两端为USB插头（A型）和微型USB插头（B型）
- 空的SD卡，容量为1GB或更大。
- 在Linux PC上配置通过USB访问HTC Android手机，方法如下：

