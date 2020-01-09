---
layout:     post
title:      python-twitter与第三方api协作
subtitle:   
date:       2010-08-25
author:     spin6lock
header-img: img/post-bg-YesOrNo.jpg
catalog: true
tags:
    - python
---
上回讲到搭建了twip作为twitter api proxy，那当然要好好地利用一下。正好最近做了一个twitter的机器人，每次都要翻代理上推实在麻烦，另外一个问题是twitter对http basic authorization的限制逐渐收紧，现在的api限制为60 per hour，稍后会再次缩减到45，而oauth则相反，准备在150/h的基础上逐渐推到1500/h（[via](https://groups.google.com/group/twitter-development-talk/browse_thread/thread/a1076d83d70d0450)）。因此，利用twip的oauth特性进行中转会是相当不错的选择。

这个机器人以前是通过proxychains，以ssh直连到twitter官网进行操作的，服务器端需要执行

这命令十分头痛，似乎tee没有发挥到应有的作用，screen也不能detach了。现在，使用twip进行中转后，只需

就可以了。

当然，python-twitter 0.6还不支持api proxy，但python twitter都是采用http basic authorization，那么理论上只需要更改api的地址即可。我checkout了最新的代码，欣喜地发现了原来的http://twitter.com已经被basic_url参数取代了，兴冲冲地试试，沮丧地发现这个参数是留给Oauth的。     这个有点不解，如果python-twitter本身直接采用oauth，那么没有必要修改base_url。如果采取的第三方api，难道python-twitter也通过oauth跟第三方进行认证吗？           后来采取了最直接的方法，直接拿了一个twitter.py放在code目录里改，将所有的twitter.com都改成自己的twip地址，世界清静了。。。注意，要将python-twitter 的api认证里面的密码改成twip里的密码，否则会遇到HTTP 401。

这个问题已经有同胞反映过，追踪google code上issue89可以跟进该问题的进一步发展。
