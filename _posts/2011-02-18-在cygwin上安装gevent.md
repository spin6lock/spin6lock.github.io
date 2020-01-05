---
layout:     post
title:      在cygwin上安装gevent
subtitle:   
date:       2011-02-18
author:     Mehaei
header-img: img/post-bg-mma-4.jpg
catalog: true
tags:
    - python
---
由于公司点餐要用QQ，只能寄身于WinXP下做开发。但是win下各种不能折腾很不爽，幸而有Cygwin

然而，使用easy_install 居然安装不了Cygwin，弹出一大堆core.c的错误，一直没搞懂。只好与win的丑陋的命令行相伴，还设置了PATH指向cygwin的bin，为的就是能顺利ls。

遍寻不获后，今天看到这篇日志[http://d.hatena.ne.jp/ymotongpoo/20110108/1294494273](http://d.hatena.ne.jp/ymotongpoo/20110108/1294494273)，终于醒悟过来了。。。我没有装libevent，cygwin的源里也没有这个东东。

剩下的就简单了，./cofigure、 make、 make install安装libevent，使用

```
python setup.py install -I /opt/local/include -L /opt/local/lib
```

```

```

```
安装gevent。
```

```

```

```
done！
```
