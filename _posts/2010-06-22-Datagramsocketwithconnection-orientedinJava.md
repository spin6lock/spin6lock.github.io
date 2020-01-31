---
layout:     post
title:      Datagramsocketwithconnection-orientedinJava
subtitle:   
date:       2010-06-22
author:     spin6lock
header-img: img/post-bg-mma-5.jpg
catalog: true
tags:
    - python
---
数据报通常采用 udp 协议进行传输，UDP 相较于 TCP 协议能够节省带宽，相应的获得较高速度，但不能保证包的安全抵达和顺序不变。

Java 关于 datagram 提供有 connect 方法，该方法绑定了远端的 IP 地址和端口号，即该 socket 以后只能向绑定目标主机发送数据或接受数据。

当目标地址不可达，且收到了该地址不可达的 ICMP 包时，会抛出 PortUnreachableException 异常，但不能保证一定抛出该异常。

** 该方法也不能保证包的顺序和安全抵达 **，只是为了发送的时候简便一点而已。。。 
