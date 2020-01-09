---
layout:     post
title:      PullRequest找原作者做review
subtitle:   
date:       2019-07-30
author:     spin6lock
header-img: img/post-bg-mma-6.jpg
catalog: true
tags:
    - python
---
最近对代码库进行了一次全局替换，改了150个左右的文件，发了PR后需要找原作者确认一下，于是写了个工具做git blame，[地址在这里](https://github.com/spin6lock/check_original_author)

写完发现一个问题，如果只是新增一个函数，没有调用，是应该不用找原作者的......但是，要识别出新增一个函数，没想象中容易，需要基于ast来做diff，才能发现。也就是说，这个工具对于批量替换的功能，才比较好用，其他改动不太合适，蛋疼
