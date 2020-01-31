---
layout:     post
title:      tricks: 如何把 sqlalchemy 的数据转化为 json 格式
subtitle:   
date:       2012-02-22
author:     spin6lock
header-img: img/post-bg-js-version.jpg
catalog: true
tags:
    - python
---
d=dict(rowproxy.items())

json.dumps(d)
