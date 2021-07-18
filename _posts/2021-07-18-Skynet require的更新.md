---
layout:     post
title:      "Skynet require 的更新 "
subtitle:   ""
date:       2021-07-18
author:     "spin6lock"
catalog:    true
tags:
- skynet
- require
---

最近升级项目依赖的中间件，中间件组的同学强力推荐（~~打发XD~~）我去看看 skynet.require 的修改，很有趣，而且是其中一个比较大的不兼容改动，我重新看了 [Skynet 的代码 ](https://github.com/cloudwu/skynet/commits/master/lualib/skynet/require.lua) 确实比以前更好用了，这里简单分享一下

服务启动的时候，往往会用到 sharedata 服务来全局共享一份数据表。sharedata 服务的 API 初始化时会使用 skynet.call 来调用 sharedata 服务，因为 call 最终会调用 yield，而 require 是一个 C 实现的函数，无法在其中 yield，就会报错。为了解决这个问题，一般是将这段 call 放进 Skynet.init 包裹的匿名函数中运行

对于启动时就需要读配置表的文件 foobar 而言，require 了 sharedata 的 API 并不代表就可以直接使用了（可能还没跑 skynet.init 中的函数）因此，必须将 require foobar 的初始化流程也包在 skynet.init 中，同时保证先调用到 sharedata 服务 API 的 skynet.init，再调用到 foobar 的 skynet.init，这样最后跑 skynet.init 函数链的顺序才是正确的

新版本用 Lua 版本的 skynet.require 替换了 require, 从而允许在 require 过程中也可以发起 call 了。严格来说，是在官方 require 后，再由 lua 层跑完 skynet.init 里的函数链，再返回原有 require 的流程继续执行。这样，用到 require sharedata API 的逻辑，在跑完 require 后，得到的就是一个可用的 API 了，不再需要自己控制 skynet.init 来保证顺序的正确性了

再次感谢涛神的分享哇 XDD
