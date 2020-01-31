---
layout:     post
title:      Ubuntu 下利用 expect 脚本自动登录 ssh 作代理
subtitle:   
date:       2010-09-05
author:     spin6lock
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - python
---
这类文章网上已经有很多了，实在不想再重复，可惜一直没有一个双击就连上 ssh 的，要不写个 GUI？putty 很搞，还是弹出一个命令行出来填用户名密码，那我干脆直接在 terminal 搞定啦。

```
#!/usr/bin/expect -f   
#auto ssh login    
  
set timeout 20   
spawn ssh login_name@host_name   
expect *password:    
send 123456\r    
interact  

```

网上流传的大多都是上面一段代码，问题就在最后一句上面：

interact

即交互模式，我用 ssh 只是拿来做代理的话，只需要后台运行就可以了，哪来 interact 呢？还有考虑更周到的，加了个 timeout，每分钟发送一个空格防止被踢，我严重怀疑这个脚本的可行性，特别是 ssh 用上了 -n 的时候。另外还有 ssh 的 -f，我以为这个是用于作 Daemon 运行的，结果发现只是暂时将 ssh 放在后台了。

最后，我将 interact 改成了 expect eof，世界清静了。

当然，还是建议采取公钥加密的，这样就不用每次都输入密码了。

推荐：[http://ssorc.tw/rewrite.php/read-600.html](http://ssorc.tw/rewrite.php/read-600.html)
