---
layout:     post
title:      python-twitter 与第三方 api 协作
subtitle:   
date:       2010-08-25
author:     spin6lock
header-img: img/post-bg-YesOrNo.jpg
catalog: true
tags:
    - python
---
上回讲到搭建了 twip 作为 twitter api proxy，那当然要好好地利用一下。正好最近做了一个 twitter 的机器人，每次都要翻代理上推实在麻烦，另外一个问题是 twitter 对 http basic authorization 的限制逐渐收紧，现在的 api 限制为 60 per hour，稍后会再次缩减到 45，而 oauth 则相反，准备在 150/h 的基础上逐渐推到 1500/h（[via](https://groups.google.com/group/twitter-development-talk/browse_thread/thread/a1076d83d70d0450)）。因此，利用 twip 的 oauth 特性进行中转会是相当不错的选择。

这个机器人以前是通过 proxychains，以 ssh 直连到 twitter 官网进行操作的，服务器端需要执行

这命令十分头痛，似乎 tee 没有发挥到应有的作用，screen 也不能 detach 了。现在，使用 twip 进行中转后，只需

就可以了。

当然，python-twitter 0.6 还不支持 api proxy，但 python twitter 都是采用 http basic authorization，那么理论上只需要更改 api 的地址即可。我 checkout 了最新的代码，欣喜地发现了原来的 http://twitter.com 已经被 basic_url 参数取代了，兴冲冲地试试，沮丧地发现这个参数是留给 Oauth 的。     这个有点不解，如果 python-twitter 本身直接采用 oauth，那么没有必要修改 base_url。如果采取的第三方 api，难道 python-twitter 也通过 oauth 跟第三方进行认证吗？           后来采取了最直接的方法，直接拿了一个 twitter.py 放在 code 目录里改，将所有的 twitter.com 都改成自己的 twip 地址，世界清静了。。。注意，要将 python-twitter 的 api 认证里面的密码改成 twip 里的密码，否则会遇到 HTTP 401。

这个问题已经有同胞反映过，追踪 google code 上 issue89 可以跟进该问题的进一步发展。
