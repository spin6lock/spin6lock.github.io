---
layout:     post
title:      迅捷 FASTFWR171-3G 实战 OpenWRT
subtitle:   
date:       2013-04-13
author:     spin6lock
header-img: img/post-bg-swift2.jpg
catalog: true
tags:
    - python
---
FAST 是 TP-LINK 的一个子品牌，所推出的 FWR171-3G 与 TP-LINK wr703n 的硬件采用相同规格，而前者要便宜 20 块，区别只在品牌、外观与软件界面。于是果断入手，然后尝试 OpenWRT。

上手后第一件事，就是通过官方界面进行线路测试。目前的网络连接是，通过 RJ45 接口接入光猫进行 PPPOE 拨号，然后利用 wifi 信号完成无线路由功能。遗憾的是，通过官方界面进行拨号连接时提示密码错误，无法联通。于是，去找到了 wr703n 的固件刷上，文件是 [wr703nv1_cn_3_12_11_up(110926)(Fast-FWR171-3G).bin](http://dl.vmall.com/c0zm3y2wb9) 注意上传过程比较慢，上传和设备重启中不要断电或断开连接。

上传完成后，登入看到经典的蓝色 TPlink 界面，继续进行线路测试。经过测试，成功通过光猫 PPPOE 拨号。接下来就要进行 OpenWRT 的刷写了，首先下载文件 [openwrt-ar71xx-generic-tl-wr703n-v1-squashfs-factory.bin](http://115.com/file/aqv8bukv) 升级，注意，升级完后就没有 web 界面了，若对命令行有畏难情绪，请谨慎操作。刷入后，就只能通过 telnet 连上，然后通过 passwd 指令设置 root 的密码，输入密码的时候默认没有回显，是正常情况，提示密码较弱的可以忽略或更换更高强度密码。使用 passwd 设置密码后，以后就不能用 telnet 进行连接，需要用 ssh，在 windows 下操作建议用 [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)。

当时走到这一步，由于懒 / 疏忽，没有进行 squashfs-sysupgrade.bin 的刷写，然后就直接接入网络了，结果 pppoe 死活拨不上号。要实现前文所述的拨号方案（pppoe+wifi 路由），需要修改 /etc/config/wireless 文件：

　config wifi-device 'radio0'	　　option type 'mac80211'	　　option hwmode '11ng'	　　option path 'platform/ar933x_wmac'	　　option htmode 'HT20'	　　list ht_capab 'SHORT-GI-20'	　　list ht_capab 'SHORT-GI-40'	　　list ht_capab 'RX-STBC1'	　　list ht_capab 'DSSS_CCK-40'	　　option txpower '17'	　　option channel '6'

```
config wifi-iface
    option device 'radio0'
    option network 'lan'
    option mode 'ap'
    option ssid ' 路由无线 ssid'
    option encryption 'psk2'
    option key ' 密码 '
```

当然，radio0 的 disable 一行需要删掉或注释掉，注意文件中的注释即可。

以及修改 /etc/config/network:

```
config interface 'loopback'
    option ifname 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config interface 'lan'
    option type 'bridge'
    option proto 'static'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
    
config interface 'wan'
    option ifname 'eth0'
    option proto 'pppoe'
    option username ' 帐号 '
    option password ' 密码 '
    option peerdns '1'
    option defaultroute '1'
```

（有博客表示 eth0 就是 wan 口，这是不对的，eth0 表示的只是以太网口，eth1 是另一个以太网口，对于 wr703n 来说不存在，wlan0 则是无线网卡口）

设置后一直无法上网，也没有办法装 luci web 管理界面。因为没有刷入 sysupgrade 的时候，内核不支持 PPPOE！！！可以通过 lsmod 查看当前加载的内核模块，insmod 安装内核模块。openwrt 的模块管理位置有点奇怪，还没找到。。。

由于一直卡在这步，我就反复改这两个文件，结果改错了进不了路由器。于是，只好自己焊接 ttl 线进行救砖。救砖前已经尝试过开机时快速插拔 reset 孔，无果。。。

手残只能焊成这样：

<img src="http://images.cnitblog.com/blog/90397/201304/13234137-73c2d3642dc540e18c0226e73b10c2a8.jpg" alt="" />

（左侧是信号地，右侧黑色是 TP_IN, 黄色是 TP_OUT, 对应的是 RX, TX）

通过 USB 转 ttl 线，成功连入路由器改回正确的配置，然后通过 dhcp 先安装好 luci，刷入 [sysupgrade](http://pan.baidu.com/share/link?shareid=265600&uk=587667030#dir/path=%2F%E5%85%B1%E4%BA%AB%E6%96%87%E6%A1%A3%2FOpenWrt%2FTL-WR703N%2F%E6%8A%8ATL-WR703N%E6%89%93%E9%80%A0%E6%88%90%E7%9C%9F%E6%AD%A3%E7%9A%84AirPlay%E6%92%AD%E6%94%BE%E5%99%A8%EF%BC%88%E7%BB%AD%EF%BC%89%E4%B8%8D%E9%9C%80U%E7%9B%98%E7%9B%B4%E8%A3%85%E7%89%88) 即可。当然，更好的办法应该是在本机开启 http 文件共享，利用路由器的 wget 进行下载，用 mtp 进行刷写。

现在，路由器已经可以通过 rj45 接口顺利 pppoe 拨号，并通过 wifi 共享，不过挂载硬盘有问题，估计是驱动的问题，但 rom 太小装不下驱动了，以后试试 u 盘增加容量后再刷驱动。。。
