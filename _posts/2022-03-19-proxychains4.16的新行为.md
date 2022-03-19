---
layout:     post
title:      "proxychains4.16 的新行为 "
subtitle:   ""
date:       2022-03-19
author:     "spin6lock"
catalog:    true
tags:
- tag
    proxychains
    dns
    ssh
    strace
---

proxychains 用来转发命令行工具的流量十分趁手，但是最近升级到 4.16 后没法上 github 了，于是好好研究了一下新的配置，写篇博客记录下

proxychains 是利用了 LD_PRELOAD 的方式抢先加载，然后将命令行程序的网络流量都按 Socks5 或者 HTTP 代理的方式转发出去。如果访问的是域名，则还需要进行一次 DNS 解析，再用 socks5 代理或者 HTTP 代理直接链接 IP 进行访问。当然，为了更完整的隐私保护，一般会在配置文件里打开 proxy_dns，由 proxychains 负责转发域名查询请求

之前的版本里，DNS 解析这个事情是透过 proxyresolv 这个小脚本完成的，不仅因为要额外 fork 进程而变慢，这个脚本里默认的 DNS 服务器还是 4.2.2.2, 一个不再对外提供服务的 DNS 服务器。新版本里改进了 DNS 解析的方式，提供了三种方式：
1. proxy_dns 用一个额外线程做 dns 查询，并且按 remote_dns_subnet 的配置分配一个假 ip，当目标程序访问假 ip 的时候，再将流量转发到真正的服务器
2. proxy_dns_old 采用老的 proxyresolv 脚本来进行 dns 查询代理
3. proxy_dns_daemon 在后台自己跑一个 proxychains4-daemon 进程，优点在没有线程分配

当采用 proxy_dns 的时候，curl 工作的很好，但是以 ssh 方式 git clone 却出现了问题。换成 proxy_dns_daemon 后解决了。猜测是 ssh 工作的时候，需要先查询域名对应的 ip 是否满足白名单，然后再进行连接，而 dns 查询相对比较慢，还没查到 ip 的时候 ssh 就终止了，提示查不到域名。当采用独立进程的时候，返回的是一个假 ip，ssh 查到 ip 后进行连接，proxychains 就直接转发流量了，所以没有问题

验证这个假设可以用两种方式完成，一种是通过查看 ssh 的日志本身。通过 `GIT_SSH_COMMAND="ssh -vvv" proxychains git clone xxx` 可以让 ssh 打出详细的调试日志，这边看 proxy_dns 方式的 ssh 日志，的确是 lookup 的时候就中止了。另一种是用 strace 将系统调用打印出来，但是中间干扰比较多，proxychains、git、ssh 这三者都有大量的读文件操作，可以用 -e trace='!%file' 表示过滤文件相关的 syscall。当然，最后还是没看出来到底啥问题，于是去查了下 issue，发现最近的一个 [issue 描述了 ssh 的问题 ](https://github.com/rofl0r/proxychains-ng/issues/439)。Linux 内核 5.9 添加了新的 close_range 接口，openssh 用这个接口替换了以前的 close 接口，直接把 proxychains 里查询 ip 线程的 fd 关掉了 …… 作者推荐了两种解决办法，一是通过 proxy_dns_daemon 查询，二是通过编译开关关掉 openssh 对 close_range 接口的使用

