---
layout:     post
title:      "goroutine 数据竞态 "
subtitle:   ""
date:       2020-07-18
author:     "spin6lock"
catalog:    true
tags:
---
最近写了个 [ 小玩具 ](https://github.com/spin6lock/goscon_proxy/)，用来去掉 goscon 相关的握手细节，这样压测程序可以透明的连接游戏服务器了。单连接测试的时候没问题，但是当连接数上去后，会出现莫名其妙的数据解析错误。感觉是出现了竞态条件了，于是用 `go build -race` 来重新构建，再测试的时候就有异常栈抛出可供分析了，还是蛮方便的

先看修复前的代码：
```golang
 75     go func() {
 76         for {
 77             size, err := scon.Read(scp_buf)
 78             if err != nil {
 79                 log.Printf("scon read error:%s\n", err.Error())
 80                 break
 81             }
 82             data := scp_buf[:size]
 83             log.Println("Read data from scp:", data)
 84             writeCh <- data
 85         }
 86         ch <- ""
 87         log.Println("scon.Read exit")
 88     }()
 89     go readPipe(readCh, ch, scon)
 90     go writePipe(writeCh, ch, conn)

108 func writePipe(writeCh chan []byte, ctrlCh chan string, conn net.Conn) {
109     for {
110         select {
111         case data := <-writeCh:
112             conn.Write(data)
113         case <-ctrlCh:
114             log.Println("writePipe got close")
115             return
116         }
117     }
118 }
```
golang 的 data race 检测提示 77 行的 `scon.Read` 与 112 行的 `conn.Write` 有竞态，112 行正在读的时候，77 行写了，导致数据异常。想了一会终于想明白了。。。82 行的赋值并没有拷贝过程，只是创建了一个 Slice，这个 Slice 指向 `scp_buf` 这个字节数组。当 `writePipe` 从 `writeCh` 中读出 data 后，75 行的 go 协程就能继续跑了，于是 `scon.Read` 继续修改 `scp_buf`，而 `conn.Write` 在读指向 `scp_buf` 的 `data`，导致数据异常。

针对这种情况，可以对 scp_buf 加读写锁；也可以多复制一份 data 数据出来，供 `writePipe` 读；或者通过 Ring 环形链表来实现两个 buf 替换，`scon.Read` 写其中一个的时候，`writePipe` 读另外一个，Ring 的大小就是缓冲区的大小，从 goscon 读和写入客户端的速度相差较大的话，可以多搞点缓冲区。目前采取的是多复制一份 data 数据来解决
