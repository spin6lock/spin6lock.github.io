---
layout:     post
title:      "tricks: 如何把 sqlalchemy 的数据转化为 json 格式"
subtitle:   
date:       2012-02-22
author:     spin6lock
header-img: img/post-bg-js-version.jpg
catalog: true
tags:
    - Python
---
sqlalchemy最恶心的对象，就是通过execute得到的结果，那是rowproxy列表。为了优化，rowproxy使用了__slot__，使其失去了动态性，而又经常要转换成json格式，于是可以这样：

```
d=dict(rowproxy.items())

json.dumps(d)
```
