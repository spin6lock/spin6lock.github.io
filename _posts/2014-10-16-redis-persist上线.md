---
layout:     post
title:      redis-persist 上线
subtitle:   
date:       2014-10-16
author:     spin6lock
header-img: img/post-bg-hacker.jpg
catalog: true
tags:
    - python
---
九月份惨不忍睹，因为代码质量不够高，直接被 Boss 喷成了筛子。被反复教育说要高质量的代码，要可维护、高性能

幸而，最后一周终于在紧张的加班中，灰度上线 redis-land-go 了，项目也改名为 redis-persist，[github 在此 ](https://github.com/xjdrew/redis-persist)。

之前实现的，是 redis 到 leveldb，以及 skynet 从 leveldb 中读取数据的接口。最后一周添加的，是 SA 同事可能会用到的功能。主要是：

- dump
- restore_one
- restore_all
- sync
- sync_all
- count
- diff
- keys
- check_all
- fast_check

这些指令可以分成三类，一类是从 redis 拷贝到 leveldb 的，比如 sync 开头的指令；一类是从 leveldb 拷贝到 redis 中的，典型如 restore 开头的指令；剩下的是用来检验两侧数据的，比如检查一个玩家数据的 diff，检查数量的 count，还有列出 leveldb 部分玩家 uid 的 keys

这里的 fast_check 是针对当前玩家存储做的一个特殊优化，在 leveldb 中用前缀分出了一个特殊的 key 表，里面是玩家 uid- 玩家数据 version 的 key-value 对。这个表足够小，可以整个放进内存里，所以对于只需比对数据版本号的情况，能够在极短时间完成。redis 和 leveldb 通过网络连接，不在一台机器上时，12w 数据不超过 1 分钟。

同时，折腾这套工具的时候，还顺便看了一下 leveldb 的结构。leveldb 有个 sstable 的概念，sstable 就是内存里一块按 key 有序排列好的表，可以改动的时候叫 memtable，准备写入磁盘的是另一个表，叫 sstable。当数据比较少的时候，层级也比较少，具体哪个 ldb 文件对应哪一段 key 范围，是记录在 MANIFEST 里面的。写入的记录，首先记入 log 里，这是顺序写，所以极快。然后是定期后台整理，将 sstable 和磁盘上已有的 ldb 文件合并，使得磁盘的数据越来越有序。
