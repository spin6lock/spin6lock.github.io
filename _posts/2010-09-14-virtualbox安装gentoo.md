---
layout:     post
title:      virtualbox安装gentoo
subtitle:   
date:       2010-09-14
author:     spin6lock
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - python
---
一直想尝试一下fvwm，又不想搞坏现在的ubuntu，顺便就搞个gentoo玩玩。

基本的安装顺序照官方的guidebook就可以了，但配置内核的时候要注意如下选项：

```
Processor type and features  --->
    [*] Tickless System (Dynamic Ticks)
    [ ] High Resolution Timer Support
    [ ] Symmetric multi-processing support
        Subarchitecture Type (PC-compatible)  --->
    [ ] Machine Check Exception
Power management and ACPI options  --->
    [*] Power Management support
    [ ] Suspend to RAM and standby
    [ ] Hibernation (aka 'suspend to disk')
    [*] ACPI (Advanced Configuration and Power Interface) Support  --->
Device Drivers  --->
    < > ATA/ATAPI/MFM/RLL support
    <*> Serial ATA and Parallel ATA drivers
        <*> AHCI SATA Support
        [*] ATA SFF support
        <*> Intel ESB, ICH, PIIX3, PIIX4 PATA/SATA support
    [*] Network device support  --->
        [*] Ethernet (10 or 100Mbit)  --->
            [*] EISA, VLB, PCI and on board controllers
            <M>   AMD PCnet32 PCI support
        [*] Ethernet (1000 Mbit)  --->
            <M> Intel(R) PRO/1000 Gigabit Ethernet support
        [ ] Ethernet (10000 Mbit)  --->
    Graphics support --->
        <*> Direct Rendering Manager (XFree86 4.1.0 and higher DRI support)  --->
            < > all options can be empty
    <M> Sound card support --->
        <M> Advanced Linux Sound Architecture --->
            [*] PCI sound Devices --->
                <M> Intel/SiS/nVidia/AMD/ALi AC97 Controller
    Input device support --->
        [*] Mice --->
           <*> PS/2 mouse

```

按以上配置的时候就可以得到virtualbox-friendly 的kernel了

配置完成后继续按照官方指南做就可以了。

有两个地方花了我很多时间，一个是文件系统，一个是网卡驱动，照以上配置应该可以顺利完成。网络方面，我采用NAT共享，所以在minimal CD的时候就要顺道把dhcpcd装上，免得启动以后上不了网emerge。

mirrorselect貌似不起作用，检查配置的时候记得顺手加上，我用的是163的源，速度蛮快的。

我的最终目标是安装X，所以还要麻烦一点。基本的virtualbox Guest addition要装上，然后是

xfree86-input-virtualbox

xfree86-video-virtualbox

最后配置/etc/X11/xorg.conf

```
Section "Device"
   Identifier   "Configured Video Device"
   Driver      "vboxvideo"
EndSection

Section "Monitor"
   Identifier   "Configured Monitor"
EndSection

Section "Screen"
    Identifier   "Default Screen"
   Monitor      "Configured Monitor"
   Device      "Configured Video Device"
   DefaultDepth    24
   SubSection      "Display"
      Depth           24
      Modes           "1280x1024"
   EndSubSection
EndSection

Section "InputDevice"
        Identifier  "vboxmouse"
        Driver          "vboxmouse"
        Option          "CorePointer"
        Option          "Device"        "/dev/input/mice"
EndSection

Section "ServerLayout"
        Identifier      "Default Layout"
        Screen          "Default Screen"        0 0
        InputDevice     "vboxmouse"
EndSection

```

官方指南里说xorg-x11和xorg-server是等效的，只是xorg-x11带了很多字体，推荐用xorg-server。

没想到x-term、xclock、tvm等等都要自己手动装

参考：


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://www.cnblogs.com/likun/archive/2009/10/15/1584208.html](http://www.cnblogs.com/likun/archive/2009/10/15/1584208.html)


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://www.ha97.com/2333.html](http://www.ha97.com/2333.html)


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://en.gentoo-wiki.com/wiki/Virtualbox_Guest](http://en.gentoo-wiki.com/wiki/Virtualbox_Guest)


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://forums.virtualbox.org/viewtopic.php?t=15679#](http://forums.virtualbox.org/viewtopic.php?t=15679)


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://www.gentoo.org/doc/en/xorg-config.xml](http://www.gentoo.org/doc/en/xorg-config.xml)


<meta http-equiv="content-type" content="text/html; charset=utf-8" />
[http://ubuntuforums.org/showthread.php?t=777759](http://ubuntuforums.org/showthread.php?t=777759)
