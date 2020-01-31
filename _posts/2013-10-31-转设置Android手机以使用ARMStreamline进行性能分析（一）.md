---
layout:     post
title:      转设置 Android 手机以使用 ARMStreamline 进行性能分析（一）
subtitle:   
date:       2013-10-31
author:     spin6lock
header-img: img/post-bg-mma-6.jpg
catalog: true
tags:
    - python
---
##  

- Streamline 5.7 版。Streamline 是 [ARM Development Studio 5](http://www.arm.com/zh/products/tools/software-tools/ds-5/index.php) 的一个组成模块。因此，可通过下载 [ARM DS-5](http://www.arm.com/zh/products/tools/software-tools/ds-5/ds-5-downloads.php) 专业版、基础版或免费的 DS-5 公众版（针对 Android 系统）来获得它。
<li>目标 ARM 设备，HTC Sensation 4G
<ul class="bbc">
- [Qualcomm Snapdragon ](http://www.arm.com/zh/markets/mobile/qualcomm-snapdragon-chipset.php)1.2-GHz 双核处理器，ARMv7 架构
- Android 2.3.4 版
- Linux 内核 2.6.35.13 版


- HTC 手机的内部代码。如果是 HTC sensation 4G 手机，那么内部代码是图中红框标示的 PYRAMID。内部代码是 HTC Android 手机的标识，通过它可搜索到 HTC 发布的正确 Linux 内核源代码包。
- 安全锁的状态。目前我这台手机的安全锁状态为 S-OFF（安全锁关闭），在图 1 中用红框标示。安全锁对实现本文目的十分重要。S-OFF 表示设备的 NAND Flash ROM 处于解锁状态并且可写，这也就意味着无需进行签名检查就可以更新 Android 系统的某些分区；例如，通过自定义镜像文件来更新启动分区。HTC 设备的默认设置为 S-ON，这表示只能使用 HTC 官方的固件镜像文件来更新系统（因为启用了签名检查）。


- 在 x86 PC 上运行的 64 位 Ubuntu 10.10 版本
- Linux 系统下的 GNU ARM Toolchain，本文所使用的是下载自 [Mentor Graphics](https://sourcery.mentor.com/sgpp/lite/arm/portal/release1803). 的 CodeSourcery ARM GNU/Linux Toolchain。
- 从 [Android 开发者网站 ](http://developer.android.com/sdk/index.html) 下载的 Android SDK r16-linux 安装程序。
- 通过 Android SDK r16-linux 安装程序下载安装的 Android SDK 平台工具包
- USB 电缆 电缆两端为 USB 插头（A 型）和微型 USB 插头（B 型）
- 空的 SD 卡，容量为 1GB 或更大。
- 在 Linux PC 上配置通过 USB 访问 HTC Android 手机，方法如下：

