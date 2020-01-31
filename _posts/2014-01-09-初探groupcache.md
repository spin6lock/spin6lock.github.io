---
layout:     post
title:      初探 groupcache
subtitle:   
date:       2014-01-09
author:     spin6lock
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - python
---
groupcache 是用于 dl.google.com 的一个 memcached 的替代品，相对于 memcached，提供更小的功能集和更高的效率，以第三方库的形式提供服务。

groupcache 的常见部署可参考下图：

<img src="http://images.cnitblog.com/blog/90397/201401/091629188481.jpg" alt="" />

不同于 memcached，groupcache 面向的是静态的缓存系统，比如 google 家的下载站，用来缓存对应的文件区块。一经 set 操作，key 对应的 value 就不再变化。使用的时候，需要自定义缓存缺失时使用的 set 操作。当发生 miss 的时候，首先会从根据 key 的 consist hash 值找到对应的 peer，去 peer 里寻找对应的 value。如果找不到，则使用自定义的 get 函数从慢缓存（比如 db，文件读取）获取 alue，并填充对应 peer。下一次获取，就直接从 cache 里取出来，不再访问慢缓存。另外，为避免网络变成瓶颈，本地 peer 获取 cache 后，会存在本地的 localCache 里，通过 LRU 算法进行管理。

groupcache 的代码分为 consistenhash, groupcachepb, lru, singleflight 等几个目录，分别存放一致性哈希，groupcache 的 protobuf 协议，lru 算法实现，用来保证求值操作只执行一次的 singleflight。本篇主要看看 singleflight。

23 // call is an in-flight or completed Do call   24 type call struct {   25     wg  sync.WaitGroup   26     val interface{}   27     err error   28 }

这里定义了一个 call 结构，包含了用来同步的 wg 等待组，一个用于承载任意值的 val，以及 err 错误信息。

 32 type Group struct {   33     mu sync.Mutex       // protects m   34     m  map[string]*call // lazily initialized   35 }

这里定义的是 Group 结构，一个 Group 内 key 是唯一的，类似于命名空间。groupcache 使用了 Mutex 保护 map 变量。

41 func (g *Group) Do(key string, fn func() (interface{}, error)) (interface{}, error) {   42     g.mu.Lock()   43     if g.m == nil {   44         g.m = make(map[string]*call)   45     }   46     if c, ok := g.m[key]; ok {   47         g.mu.Unlock()   48         c.wg.Wait()   49         return c.val, c.err   50     }   51     c := new(call)   52     c.wg.Add(1)   53     g.m[key] = c   54     g.mu.Unlock()   55   56     c.val, c.err = fn()   57     c.wg.Done()   58   59     g.mu.Lock()   60     delete(g.m, key)   61     g.mu.Unlock()   62   63     return c.val, c.err   64 }

这里 Do 定义的就是一个带锁保护的保证单次执行的函数。因为 consistent hash 定位到的 peer 是唯一的，因此这里只需要同步该进程内的 goroutine 即可。为了减少锁的影响，锁控制的范围被切成了好几段。整个完整流程包括 3 步：1. 初始化 g.m 变量 2. 赋值 g.m[key] 变量为 val 3. 删除 g.m 的 key。第一步会加锁，第一个进入的 go 程会走到第二步进行赋值操作，到其他 go 程进入 1 的时候，第二步 key 对应的值已经有了，可以直接释放锁了。然后到第三步，第一个进入的 go 程会加锁，然后删除 key，再解锁。前面尽早释放锁，就是为了第三步这里不需要长久的等待。
