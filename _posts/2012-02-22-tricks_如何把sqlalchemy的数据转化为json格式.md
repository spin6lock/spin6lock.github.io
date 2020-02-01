---
layout:     post
title:      "tricks: 如何把 sqlalchemy 的数据转化为 json 格式 "
subtitle:   
date:       2012-02-22
author:     spin6lock
header-img: img/post-bg-js-version.jpg
catalog: true
tags:
    - Python
---
sqlalchemy 最恶心的对象，就是通过 execute 得到的结果，那是 rowproxy 列表。为了优化，rowproxy 使用了 __slot__，使其失去了动态性，而又经常要转换成 json 格式，于是可以这样：

```
d=dict(rowproxy.items())

json.dumps(d)
```
