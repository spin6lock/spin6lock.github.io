---
layout:     post
title:      CrossSiteRequestForgeries跨站伪请求
subtitle:   
date:       2010-07-09
author:     spin6lock
header-img: img/post-bg-mma-6.jpg
catalog: true
tags:
    - python
---
今天看Django的tutorial，里面提到了这样一种跨站攻击：

假设有客户Bob 在浏览论坛页面（Bob真可怜～～～），Alice发布了一个很热的帖子，里面有

而在这个场景里，论坛和银行都是Bob所信任的，这就是csrf的可怕之处 。Django推荐凡是影响服务器端数据的动作，均使用post，另外还引入了csrf_token预防事故。
