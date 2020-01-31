---
layout:     post
title:      sshtunnel 翻过伟大的长城
subtitle:   
date:       2010-08-19
author:     spin6lock
header-img: img/post-bg-mma-4.jpg
catalog: true
tags:
    - python
---
项目进入到一个稳定期，就等词库的扩张了。我打算在 twitter 上架设一个 twitter 机器人，搞搞新意思。看了下 twitter api 的文档，发现 python 的 twitter 库还真不少，看中的有两款：python-twitter 和
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
tweepy, 稍微看了看，python-twitter 首页就有示例了，就你吧。

以迅雷不及掩耳盗铃之势装好了 simlejson 和 oauth 的依赖，就可以开始工作了。本地测试通过～～由于众所周知的原因，不能直接访问到 twitter，似乎 python-twitter 这个库也找不到设置代理的接口。不想 hardcode，跑去问 google 大神了。google 说 proxychains 是个好东西：通过设置 LD_PRELOAD 环境变量，使所有 TCP 连接都经过代理出去。（奇怪的是我找不到这个变量，却能够使用代理。。。）

既然要处理代理的事，顺便就把 ssh tunnel 搞定了。以前一直没搞懂，究竟执行 ssh -D 以后，forward 的是服务器端还是本地。后来终于想通了，本地通过 ssh 加密连接到服务器上，服务器负责转发功能。假设执行的是 ssh -D 12345，则设置 socks 代理后，数据就发往本地的 12345，这些数据通过加密的 ssh 信道传到服务器，服务器上再通过非加密通道 forward 出去。因为代理的 TCP 连接都通过 ssh 传输到远端服务器，就像在 ssh 隧道中通行一样，所以称为 ssh tunnel.
