---
layout:     post
title:      为python-sproto添加map支持
subtitle:   
date:       2015-06-04
author:     spin6lock
header-img: img/post-bg-e2e-ux.jpg
catalog: true
tags:
    - python
---
上个月太忙了，做完这个修改还没写博客，现在补一下。。

之前使用protobuf做协议打包的时候，经常会有个痛点，没法用具体数据的值作为key来索引数据。比如现在客户端上传了造兵协议，协议大概长这样：

```
{
   {
      troop_type = 101,
      amount = 1,
   },
   {
      troop_tyoe = 102,
      amount = 2,
   },    
}
```

可以看到，造兵协议是一个数组，数组里每个元素是一个结构，包含troop_type（兵种类别）和amount（数量）。每次收到的时候，都需要遍历一次来建立一个以troop_type为key的字典，或者使用时根据troop_type来遍历查找。

```
{
   [101] = {
      troop_type = 1,
      amount = 1,
   },
   [102] = {
      troop_tyoe = 2,
      amount = 2,
   },    
}
```

最后，还添加了一点异常处理，若解包过程中出错，会把解出来的这个字典直接释放掉。有点担心异常处理的时候，会不会导致引用计数没有处理好，引起内存泄漏。以后有空再做一下内存泄漏分析~具体的修改可以参考：https://github.com/spin6lock/python-sproto.git
