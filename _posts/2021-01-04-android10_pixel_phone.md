---
layout:     post
title:      "Pixel 刷入 Android10"
subtitle:   ""
date:       2021-01-04
author:     "spin6lock"
catalog:    true
tags:
---
2021 年 6 月 1 日后，[Google 相册的高画质存储也会算入存储空间，Pixel 手机除外 ](https://support.google.com/photos/answer/6220791?co=GENIE.Platform%3DAndroid&hl=zh-Hans)，趁着优惠入手 Pixel 来薅羊毛 :) 机器到手后刷下官方系统

* 开机后点击设置 - 关于手机 - 版本号，点击 7 次后打开开发者选项，点击系统 - 高级 - 开发者选项，打开 usb 调试和 OEM 解锁
* 从官方网站下载镜像：[marlin](https://developers.google.com/android/images#marlin) ( 选最新的）
* 从官方网站下载 platform-tools：[https://dl.google.com/android/repository/platform-tools_r30.0.5-linux.zip](https://dl.google.com/android/repository/platform-tools_r30.0.5-linux.zip)
* 解压 platform-tools: `unzip platform-tools_r30.0.5-linux.zip`
* 进入 platform-tools 目录，插入数据线，检查是否连接正常：`adb devices` 这里应该能看到手机 ( 注意检查数据线，有些线只能用来充电 )
* 进入 bootloader：`adb reboot bootloader`
* 解锁 bootloader：`sudo fastboot flashing unlock`
* 将镜像解压到 platform-tools 目录，将 flash-all.sh 中的 fastboot 改为 ./fastboot，执行 `sudo ./flash-all.sh`
