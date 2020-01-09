---
layout:     post
title:      HTTPPostmultipartform-data支持
subtitle:   
date:       2018-12-24
author:     spin6lock
header-img: img/post-bg-cook.jpg
catalog: true
tags:
    - python
---
最近需要向平台发送录像文件，但是Skynet没有multipart/form-data的Post请求支持，写篇blog记录一下

所以只能有最原始的httpc.request方法了。请求头比较灵活，可以自己设置为Content-type: multipart/form-data; 除了这个，还需要设置一个boundary，用来分割需要同时上传多个field的情况。每个field长这样：

```
--------------------------d74496d66958873e
Content-Disposition: form-data; name="secret"; filename="file.txt"
Content-Type: text/plain

contents of the file
--------------------------d74496d66958873e--
```

其中--------------------------d74496d66958873e 这个就是boundary，最后会加上--表示结束。

特别鸣谢cURL的文档：https://ec.haxx.se/http-multipart.html，里面写的非常详细。还提到了一个Expect参数，让服务器可以用100 continue来让客户端继续传，如果因为身份认证等问题出错，可以直接返回错误码，中断客户端上传，避免上传了一大堆然后发现没权限的浪费。

对于多个field的编码，可以用这个库：https://github.com/Kong/lua-multipart，会帮你将body编码好
