---
layout:     post
title:      pythonsproto 支持 64 位有符号整数
subtitle:   
date:       2016-03-29
author:     spin6lock
header-img: img/post-bg-mma-2.jpg
catalog: true
tags:
    - python
---
小伙伴需要 64 位整数做物品的 id，之前 python sproto 的判断有问题，写篇日志记录一下。

之前有问题的代码是这样的：

```
             if (!PyInt_Check(data)) {
                 PyErr_SetObject(SprotoError, PyString_FromFormat("type mismatch, tag:%s, expected int", tagname));
                 return -1;
             }
             long i = PyInt_AsLong(data);
             int vh = i >> 31;
             if (vh == 0 || vh == -1) {
                 *(uint32_t *)args->value = (uint32_t)i;
                 return 4;
             } else {
```

这里有两个问题。一，long 只保证有 32bit（via [wiki](https://en.wikipedia.org/wiki/C_data_types)），有可能 data 是 64bit 的，这个时候就会丢数据。二，vh 的定义是 int，这里会丢数据。vh 是 i 通过位移得到的，目的是判断高位有没有数据，如果只有符号位有意义，就不用 64bit 存了，可以转到 32bit 里放数据。但是，我把 vh 强转成 int，这样刚好就丢掉了符号位，然后让次高位充当了符号位，这时候得到的数据是错误的。

现在改成了这样：

```
            if (PyInt_Check(data) || PyLong_Check(data)) {
                 long long i = PyLong_AsLongLong(data);
                 long long vh = i >> 31; 
                 if (vh == 0 || vh == -1) {
                     *(int32_t *)args->value = (int32_t)i;
                     return 4;
                 } else {
                     *(int64_t *)args->value = (int64_t)i;
                     return 8; 
                 }
```

看起来没问题了 :) 
