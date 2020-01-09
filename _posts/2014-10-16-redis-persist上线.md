---
layout:     post
title:      redis-persist上线
subtitle:   
date:       2014-10-16
author:     spin6lock
header-img: img/post-bg-hacker.jpg
catalog: true
tags:
    - python
---
九月份惨不忍睹，因为代码质量不够高，直接被Boss喷成了筛子。被反复教育说要高质量的代码，要可维护、高性能

幸而，最后一周终于在紧张的加班中，灰度上线redis-land-go了，项目也改名为redis-persist，[github在此](https://github.com/xjdrew/redis-persist)。

之前实现的，是redis到leveldb，以及skynet从leveldb中读取数据的接口。最后一周添加的，是SA同事可能会用到的功能。主要是：

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

这些指令可以分成三类，一类是从redis拷贝到leveldb的，比如sync开头的指令；一类是从leveldb拷贝到redis中的，典型如restore开头的指令；剩下的是用来检验两侧数据的，比如检查一个玩家数据的diff，检查数量的count，还有列出leveldb部分玩家uid的keys

这里的fast_check是针对当前玩家存储做的一个特殊优化，在leveldb中用前缀分出了一个特殊的key表，里面是玩家uid-玩家数据version的key-value对。这个表足够小，可以整个放进内存里，所以对于只需比对数据版本号的情况，能够在极短时间完成。redis和leveldb通过网络连接，不在一台机器上时，12w数据不超过1分钟。

同时，折腾这套工具的时候，还顺便看了一下leveldb的结构。leveldb有个sstable的概念，sstable就是内存里一块按key有序排列好的表，可以改动的时候叫memtable，准备写入磁盘的是另一个表，叫sstable。当数据比较少的时候，层级也比较少，具体哪个ldb文件对应哪一段key范围，是记录在MANIFEST里面的。写入的记录，首先记入log里，这是顺序写，所以极快。然后是定期后台整理，将sstable和磁盘上已有的ldb文件合并，使得磁盘的数据越来越有序。
