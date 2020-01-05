---
layout:     post
title:      tricks:如何把sqlalchemy的数据转化为json格式
subtitle:   
date:       2012-02-22
author:     Mehaei
header-img: img/post-bg-js-version.jpg
catalog: true
tags:
    - python
---
d=dict(rowproxy.items())

json.dumps(d)
