---
layout:     post
title:      为 sproto 手写了一个 pythonparser
subtitle:   
date:       2015-12-13
author:     spin6lock
header-img: img/post-bg-github-cup.jpg
catalog: true
tags:
    - python
---
这是 sproto 系列文章的第三篇，可以参考前面的《[ 为 sproto 添加 python 绑定 ](http://www.cnblogs.com/Lifehacker/p/python_sproto_introduction.html)》、《[ 为 python-sproto 添加 map 支持 ](http://www.cnblogs.com/Lifehacker/p/add_unorder_map_support_to_sproto.html)》。

```
.type {
    .field {
        name 0 : string
        buildin    1 :    integer
        type 2 : integer
        tag    3 :    integer
        array 4    : boolean
        key 5 : integer # If key exists, array must be true, and it's a map.
    }
    name 0 : string
    fields 1 : *field
}
.protocol {
    name 0 : string
    tag    1 :    integer
    request    2 :    integer    # index
    response 3 : integer # index
}
.group {
    type 0 : *type
    protocol 1 : *protocol
}
```

这么简单的结构，正好拿来练手写 parser。Lua 的 LPEG 库实在太强大，于是先试了一下 pypeg2 去解决这个问题。尝试的过程参见：https://github.com/spin6lock/sproto_python_parser，最后失败了。回想了一下，PEG 文法其实跟上下文无关文法相当类似，只是不存在二义性，能够通过一个 token 来完全决定接下来的解析树。这个跟递归下降法有点类似了，便顺手撸了一发：[https://github.com/spin6lock/yapsp](https://github.com/spin6lock/yapsp)

代码主要分成两部分，lexer 和 parser。lexer 辨别的 token 可以参见 [ 常量定义 ](https://github.com/spin6lock/yapsp/blob/master/constants.py)，基本上用正则表达式搞定了，只花了一点点时间。Parser 多花了好一段，主要是忘了要封装一些方便的函数出来使用，比如 expecting 和 optional。Parser 实现的是一个基于递归下降法的语法分析器，由于 sproto 的语法特别简单，所以可以透过窥视下一个 token，便知晓接下来要解析的是什么结构，然后调用相应的方法解析即可。
