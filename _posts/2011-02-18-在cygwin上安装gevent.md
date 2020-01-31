---
layout:     post
title:      在 cygwin 上安装 gevent
subtitle:   
date:       2011-02-18
author:     spin6lock
header-img: img/post-bg-mma-4.jpg
catalog: true
tags:
    - python
---
由于公司点餐要用 QQ，只能寄身于 WinXP 下做开发。但是 win 下各种不能折腾很不爽，幸而有 Cygwin

然而，使用 easy_install 居然安装不了 Cygwin，弹出一大堆 core.c 的错误，一直没搞懂。只好与 win 的丑陋的命令行相伴，还设置了 PATH 指向 cygwin 的 bin，为的就是能顺利 ls。

遍寻不获后，今天看到这篇日志 [http://d.hatena.ne.jp/ymotongpoo/20110108/1294494273](http://d.hatena.ne.jp/ymotongpoo/20110108/1294494273)，终于醒悟过来了。。。我没有装 libevent，cygwin 的源里也没有这个东东。

剩下的就简单了，./cofigure、 make、 make install 安装 libevent，使用

```
python setup.py install -I /opt/local/include -L /opt/local/lib
```

```

```

```
安装 gevent。
```

```

```

```
done！
```
