---
layout:     post
title:      从一段代码里看 FreeBSD 与 Linux 内存分配的不同
subtitle:   
date:       2013-02-23
author:     spin6lock
header-img: img/post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - python
---
唉，拖延症无以复加了。

最近，公司移植服务器端游戏引擎到 Linux 上的时候，遇上了段错误。问题代码大略如下：

```
char *arr = malloc(len);
...
if (IsInvalid(arr[0])){
    arr++;
}
...
free(arr);
```

很明显，对操作系统分配的内存块进行了指针操作后，再扔回到 free 函数进行释放，是会导致异常行为的。但是，该引擎的代码已经有较长的历史了，为什么在 FreeBSD 上没有遇到问题呢？

这主要是因为 FreeBSD 与 Linux 的内存分配机制不同引起的。
