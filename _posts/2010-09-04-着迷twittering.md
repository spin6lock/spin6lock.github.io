---
layout:     post
title:      着迷twittering
subtitle:   
date:       2010-09-04
author:     Mehaei
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - python
---
似乎最近迷上了翻过伟大的长城这项体育活动，而且还是为翻墙而翻墙那一种。。。

继twip之后，又迷上了gtap这个twitter api proxy。这个代理架设在gae上，用的还是我熟悉的python语言，非常亲切。当然，那坨Django的代码也不是我暂时能够捣鼓出来的，hack的时候用了点拙劣的手法。

twitter这种思维碎片，我总喜欢将其归为短信一类，因此手机发推才比较接近我的习惯。鉴于非智能机hack的难度较高，没有vpn和ssh可用，只好用gae做proxy了。既然gtap支持Oauth，当然是一个不错的选择（我对于第三方要求原始帐号和密码都比较反感。。。）。但手机界最节省流量的twitter proxy，应该算是birdnest了，号称50% off。参考过birdnest的代码进行测试，我觉得50%这个数字太保守，一般情况下能省掉三分之二的流量。原理其实很简单，每条推只传输基本元素，例如What、Who、When，这样省下的流量就很可观了。另外，这需要客户端的配合，假如你的客户端需要多媒体的支持，例如显示对方推友的头像，推中的图片自动显示缩略图，这种纯文字的api proxy就不合适了。

可惜的是，birdnest不支持Oauth认证，而twitter已经停止了basic authorization的认证方式，于是我就参考了birdnest的代码将textOnly的特性加入了gtap。（[via issue 71](http://code.google.com/p/gtap/issues/detail?id=71)）这几天回顾了一下，又加了一个过滤特定Client的功能。某君用了Google2Tweet这款插件，但我已经在Greader上follow了，不需要接收这些冗余信息了，再屏蔽之。结果是50条推基本在35-48KB之间（开启gzip）。我很好奇这离压缩的极限有多远，有位laobubu的网友自己写了服务端和客户端，采用了自己的数据格式进行传输，据称每次可以在1KB左右，参见其作品快速推FastTwitter。

我用来配套的是jibjib，基本的读推、发推、锐推、mention以及私信都支持，但我follow的人不多，获取最流行的信息有点难度。加上没有列表和搜索的支持，着实让人头痛。不过Java于我一向比较头大，hack这个暂时有点难度。非智能机似乎还真没有多少好用的java客户端，稍后可能会投靠奶瓶推这种web版客户端，当然要在有可用php空间的情况下了。话说jibjib的作者更新很勤快，twip的cnyegle狐狸也是！坦白说，狐狸你的VPN让我动心了，尤其是可以蹭CMCC这点~~~
