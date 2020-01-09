---
layout:     post
title:      初探groupcache
subtitle:   
date:       2014-01-09
author:     spin6lock
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - python
---
groupcache是用于dl.google.com的一个memcached的替代品，相对于memcached，提供更小的功能集和更高的效率，以第三方库的形式提供服务。

groupcache的常见部署可参考下图：

<img src="http://images.cnitblog.com/blog/90397/201401/091629188481.jpg" alt="" />

不同于memcached，groupcache面向的是静态的缓存系统，比如google家的下载站，用来缓存对应的文件区块。一经set操作，key对应的value就不再变化。使用的时候，需要自定义缓存缺失时使用的set操作。当发生miss的时候，首先会从根据key的consist hash值找到对应的peer，去peer里寻找对应的value。如果找不到，则使用自定义的get函数从慢缓存（比如db，文件读取）获取alue，并填充对应peer。下一次获取，就直接从cache里取出来，不再访问慢缓存。另外，为避免网络变成瓶颈，本地peer获取cache后，会存在本地的localCache里，通过LRU算法进行管理。

groupcache的代码分为consistenhash, groupcachepb, lru, singleflight等几个目录，分别存放一致性哈希，groupcache的protobuf协议，lru算法实现，用来保证求值操作只执行一次的singleflight。本篇主要看看singleflight。

23 // call is an in-flight or completed Do call   24 type call struct {   25     wg  sync.WaitGroup   26     val interface{}   27     err error   28 }

这里定义了一个call结构，包含了用来同步的wg等待组，一个用于承载任意值的val，以及err错误信息。

 32 type Group struct {   33     mu sync.Mutex       // protects m   34     m  map[string]*call // lazily initialized   35 }

这里定义的是Group结构，一个Group内key是唯一的，类似于命名空间。groupcache使用了Mutex保护map变量。

41 func (g *Group) Do(key string, fn func() (interface{}, error)) (interface{}, error) {   42     g.mu.Lock()   43     if g.m == nil {   44         g.m = make(map[string]*call)   45     }   46     if c, ok := g.m[key]; ok {   47         g.mu.Unlock()   48         c.wg.Wait()   49         return c.val, c.err   50     }   51     c := new(call)   52     c.wg.Add(1)   53     g.m[key] = c   54     g.mu.Unlock()   55   56     c.val, c.err = fn()   57     c.wg.Done()   58   59     g.mu.Lock()   60     delete(g.m, key)   61     g.mu.Unlock()   62   63     return c.val, c.err   64 }

这里Do定义的就是一个带锁保护的保证单次执行的函数。因为consistent hash定位到的peer是唯一的，因此这里只需要同步该进程内的goroutine即可。为了减少锁的影响，锁控制的范围被切成了好几段。整个完整流程包括3步：1. 初始化g.m变量 2. 赋值g.m[key]变量为val 3.删除g.m的key。第一步会加锁，第一个进入的go程会走到第二步进行赋值操作，到其他go程进入1的时候，第二步key对应的值已经有了，可以直接释放锁了。然后到第三步，第一个进入的go程会加锁，然后删除key，再解锁。前面尽早释放锁，就是为了第三步这里不需要长久的等待。
