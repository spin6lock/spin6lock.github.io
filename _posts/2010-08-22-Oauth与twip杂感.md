---
layout:     post
title:      Oauth与twip杂感
subtitle:   
date:       2010-08-22
author:     spin6lock
header-img: img/post-bg-miui6.jpg
catalog: true
tags:
    - python
---
今天帮忙搭建twip了，主要参考了[http://yht.in/archives/90](http://yht.in/archives/90)这篇文章。

twip的主要原理，就是通过一台在墙外而国内又可以访问的独立主机作为跳板，国内用户首先连接到该独立主机上，然后再通过主机与twitter交换数据。为了提高安全性，twitter今年6月份停止了http basic authorize，取而代之的是Oauth的认证。用户的登录过程由twitter完成，最后twitter将用户的认证结果和授权告诉应用。得益于twitter api的简洁，以及标准的数据交互方式（可选择xml、json和atom其中一种），大量的第三方应用如雨后春笋般涌现出来，极大地丰富了twitter的表现形式（我终于可以手机上推啦XD）。

发觉Oauth这套认证真的很不错，无需用户重复繁琐的注册步骤，即可对用户进行认证。稍后考虑一下用上这套认证，到时候注册就方便多了，反正面向的主要用户群都是twitter的老用户顺便扯一句，这年头连twitter和digg都不用MySQL了，也是，对于key-value这种字典型的应用，吞吐量又大，传统的关系数据库经常需要多表联合查询，的确会拖慢效率。

最后打开了服务器的gzip，twitter真的是流量大户，更新一次就20多kb了
