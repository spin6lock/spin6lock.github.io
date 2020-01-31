---
layout:     post
title:      HTTPPostmultipartform-data 支持
subtitle:   
date:       2018-12-24
author:     spin6lock
header-img: img/post-bg-cook.jpg
catalog: true
tags:
    - python
---
最近需要向平台发送录像文件，但是 Skynet 没有 multipart/form-data 的 Post 请求支持，写篇 blog 记录一下

所以只能有最原始的 httpc.request 方法了。请求头比较灵活，可以自己设置为 Content-type: multipart/form-data; 除了这个，还需要设置一个 boundary，用来分割需要同时上传多个 field 的情况。每个 field 长这样：

```
--------------------------d74496d66958873e
Content-Disposition: form-data; name="secret"; filename="file.txt"
Content-Type: text/plain

contents of the file
--------------------------d74496d66958873e--
```

其中 --------------------------d74496d66958873e 这个就是 boundary，最后会加上 -- 表示结束。

特别鸣谢 cURL 的文档：https://ec.haxx.se/http-multipart.html，里面写的非常详细。还提到了一个 Expect 参数，让服务器可以用 100 continue 来让客户端继续传，如果因为身份认证等问题出错，可以直接返回错误码，中断客户端上传，避免上传了一大堆然后发现没权限的浪费。

对于多个 field 的编码，可以用这个库：https://github.com/Kong/lua-multipart，会帮你将 body 编码好
