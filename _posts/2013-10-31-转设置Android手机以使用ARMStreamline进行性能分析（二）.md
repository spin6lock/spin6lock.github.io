---
layout:     post
title:      转设置Android手机以使用ARMStreamline进行性能分析（二）
subtitle:   
date:       2013-10-31
author:     spin6lock
header-img: img/post-bg-mma-5.jpg
catalog: true
tags:
    - python
---
##  

- General Setup(常规设置)，确保启用了Profiling Support (分析支持)选项。
- Kernel Hacking(内核开发)，在子菜单中，导航至Tracers子菜单，然后按下Enter。确保启用Trace进程上下文开关选项。
- Kernel Features(内核功能)，确保启用High Resolution Timer Support (高分辨率定时器支持)。如果正在使用对称多处理器(SMP)设备，则启用Use local timer interrupts （使用本地定时器中断）。


- 为加快工作速度，先下载一个内核更新包作为模板。对于HTC Sensation 4G手机，可通过Google来查找某些[kernel update packages](http://forum.xda-developers.com/showthread.php?t=1200403)（内核更新包）。
- 将其解压至工作文件夹<workdir>
- 用重新编译的内核文件zImage来替换<workdir>/kernel文件夹中的zImage文件。
- 将init.rc复制到<workdir>/kernel 文件夹
- 在<workdir>/kernel文件夹中编辑或创建mkbooting.sh脚本来更新启动镜像


- 将重新编译的内核模块（wifi驱动程序）复制到<workdir>/system/lib/modules文件夹
- 将gator.ko和gatord复制到<workdir>/system/xbin 文件夹
- 在<workdir>/META-INF/com/google/android/updater-script文件夹中编辑updater-script文件。添加下列行来更新系统分区，并将gatord程序的权限设置成可执行。


- 在<workdir>/META-INF/com/google/android/updater-script文件夹中编辑updater-script文件。添加下列行来更新启动分区（内核及init.rc）。


- 将<workdir>文件夹压缩为update.zip文件。请注意！切勿将<workdir>文件夹本身包括在内。
- 将update.zip文件复制到目标手机的SD卡根文件夹下。

