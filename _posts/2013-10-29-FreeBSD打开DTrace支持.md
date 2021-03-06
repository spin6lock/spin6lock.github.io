---
layout:     post
title:      FreeBSD 打开 DTrace 支持
subtitle:   
date:       2013-10-29
author:     spin6lock
header-img: img/post-bg-unix-linux.jpg
catalog: true
tags:
    - python
---
主要翻译自：[https://wiki.freebsd.org/DTrace](https://wiki.freebsd.org/DTrace)

FreeBSD 跟 Linux 发行版一个比较大的差异，就是提倡源码构建。因此这里提到比较多的编译开关设置。自 2012 年 5 月后，DTrace 支持默认是打开的，因此以下步骤不再需要了。留意 uname -a 输出的日期即可。

添加内核编译选项，打开 DTrace 支持

1. 打开调试符号

```
makeoptions DEBUG="-g"       # build kernel with gdb(1) debug symbols
```

2. 对于 10.0 之前的 FreeBSD，添加：

```
options KDTRACE_HOOKS      # all architectures - enable general DTrace hooks
options DDB_CTF            # all architectures - kernel ELF linker loads CTF data
```

3. 对于 AMD64（64 位处理器），添加：

```
options KDTRACE_FRAME        # amd64 - ensure frames are compiled in
```

4. 对于 9.0 或之后的系统，WITH_CTF=1 需要在内核设置里添加：

```
makeoptions WITH_CTF=1
```

（关于编译内核的步骤，可以参考：http://tthtlc.wordpress.com/2012/08/12/enabling-dtrace-on-freebsd-9/，内核的代码都在 /usr/src, 拿一份比如 /usr/src/sys/amd64/conf 里的 GENERIC 复制以下，添加上面的选项就可以了。）

重编译并安装内核

1. 对于 FreeBSD 9 及以后的系统

```
make buildkernel KERNCONF=DTRACE
```

2. 对于 FreeBSD 8-STABLE 及更老的系统

```
make buildkernel WITH_CTF=1 KERNCONF=DTRACE
```

3. 安装内核并重启

```
make installkernel KERNCONF=DTRACE
shutdown -r now
```

查看安装效果

1. 加载内核 DTrace 模块

kldload dtraceall

2. 确认 dtrace 安装正确：

dtrace -l|head

3. 尝试添加 DTrace 监控：

dtrace -n 'syscall:::entry { @num[execname] = count(); }'

如果你看到输出是：

```
dtrace: invalid probe specifier syscall:::entry { @num[execname] = count(); }: "/usr/lib/dtrace/psinfo.d", line 37: failed to copy type of 'pr_uid': Type information is in parent and unavailable
```

说明前面没做好，重头再来吧

用户空间的 DTrace

对于 FreeBSD 9.0 及以后的版本

1. 对于用户态的 DTrace 支持，需要在你的 /etc/make.conf 文件里添加：

CFLAGS+=-fno-omit-frame-pointer

这是用以提供栈跟踪的，可以提供更多信息

2. 重新安装 world：

make WITH_CTF=1 buildworld

make installworld
