---
layout:     post
title:      "当lua_sharedata碰上上限"
subtitle:   ""
date:       2024-10-14
author:     "spin6lock"
catalog:    true
tags:
- skynet
- sharedata
---
最近在使用sharedata共享配置表的时候遇到了问题，报了stack overflow，[最小复现的例子贴在这里了](https://github.com/cloudwu/skynet/issues/1981)。之前因为忙，没有细读过sharedata 的代码，这次事故正好临急抱佛脚读一遍，匆忙记点笔记，以后好回忆起来。sharedata是为了不同服务之间共享配置表而诞生的，通过sharedata接口拿到的是一个 c 的代理对象，并不直接持有配置表本身。正是通过这个代理，实现了配置表的无感热更，以及服务之间的配置内存共享。对于字符串来说，这个C代理持有的并不是字符串本身，而是一个索引，指向lua栈上的一个位置，真正需要的时候，再去lua栈上去拿这个字符串。在初始化的时候，会用一个 table来做字符串的去重，如果是一个新的字符串，则推到栈上并将栈的位置记录下来。以后这个字符串再次出现，也只会用同一个索引来代表，有点类似lua本身的短字符串共享。

正是这个实现，引入了一个上限，配置表里的字符串，数量不能超过lua栈的上限（100万个）。要解决这个问题，可以改lua栈的上限，或者用lua table/userdata重新实现一遍，不依赖lua栈，不过，性能可能差一点。我们最后直接分离配置来解决，100万的上限是针对一次```sharedata.new("foobar", big_table)```，那我多搞几个key就好了
