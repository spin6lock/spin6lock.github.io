---
layout:     post
title:      Datagramsocketwithconnection-orientedinJava
subtitle:   
date:       2010-06-22
author:     Mehaei
header-img: img/post-bg-mma-5.jpg
catalog: true
tags:
    - python
---
数据报通常采用udp协议进行传输，UDP相较于TCP协议能够节省带宽，相应的获得较高速度，但不能保证包的安全抵达和顺序不变。

Java关于datagram提供有connect方法，该方法绑定了远端的IP地址和端口号，即该socket以后只能向绑定目标主机发送数据或接受数据。

当目标地址不可达，且收到了该地址不可达的ICMP包时，会抛出PortUnreachableException异常，但不能保证一定抛出该异常。

**该方法也不能保证包的顺序和安全抵达**，只是为了发送的时候简便一点而已。。。 
