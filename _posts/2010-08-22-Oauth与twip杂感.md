---
layout:     post
title:      Oauth 与 twip 杂感
subtitle:   
date:       2010-08-22
author:     spin6lock
header-img: img/post-bg-miui6.jpg
catalog: true
tags:
    - python
---
今天帮忙搭建 twip 了，主要参考了 [http://yht.in/archives/90](http://yht.in/archives/90) 这篇文章。

twip 的主要原理，就是通过一台在墙外而国内又可以访问的独立主机作为跳板，国内用户首先连接到该独立主机上，然后再通过主机与 twitter 交换数据。为了提高安全性，twitter 今年 6 月份停止了 http basic authorize，取而代之的是 Oauth 的认证。用户的登录过程由 twitter 完成，最后 twitter 将用户的认证结果和授权告诉应用。得益于 twitter api 的简洁，以及标准的数据交互方式（可选择 xml、json 和 atom 其中一种），大量的第三方应用如雨后春笋般涌现出来，极大地丰富了 twitter 的表现形式（我终于可以手机上推啦 XD）。

发觉 Oauth 这套认证真的很不错，无需用户重复繁琐的注册步骤，即可对用户进行认证。稍后考虑一下用上这套认证，到时候注册就方便多了，反正面向的主要用户群都是 twitter 的老用户顺便扯一句，这年头连 twitter 和 digg 都不用 MySQL 了，也是，对于 key-value 这种字典型的应用，吞吐量又大，传统的关系数据库经常需要多表联合查询，的确会拖慢效率。

最后打开了服务器的 gzip，twitter 真的是流量大户，更新一次就 20 多 kb 了
