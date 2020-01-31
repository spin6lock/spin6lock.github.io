---
layout:     post
title:      apache-tomcat-6.0.26 的 cgi 配置过程
subtitle:   
date:       2010-05-24
author:     spin6lock
header-img: img/post-bg-mma-0.png
catalog: true
tags:
    - python
---
这东西折磨我太久了，写篇笔记。

Apache 的目录很好认，我下的是 zip 绿色版，解压开就看见 running 这个说明文件了，建议大家读读。

conf 目录是放置配置文件的，bin 则是可执行文件的位置，只需双击 startup.bat，即可启动 Apache。

要运行 cgi，主要是改两个文件，一个是 web.xml，一个是 context.xml。

context.xml 主要是改这么一行：

直接在 context 后加上 privileged 就可以了，用于放行可执行文件。

web.xml 修改的是 cgi 那一段，其实默认也带有 cgi 的配置的，只是被注释掉而已。

还有：

配置过程中遇到一个问题，就是静态网页可以正常显示，但点击其中的 cgi 连接时，cgi 就被当成文件下载了，而不是由服务器解释执行。

这个问题需要 html 文件、目录结构和以上 web.xml 配置的紧密配合才可以解决。

假设当前目录结构是：

cookie 

What is your customer id: <input name="id"><P>

上述的 html 代码，是无法正常工作的。点击按钮时，Apache 会在 html 所在当前文件夹下寻找 cgi 文件。但默认的 cgi 前缀是 WEB-INF/cgi-bin，路径不对，无法执行。改成 /cookies/cgi-bin/cookie.cgi 以后就可以了。

至于 cgi 没有执行，变成文件下载了，主要是因为 web.xml 中 servlet-mapping 那一段的问题，只有路径中带有 /cgi-bin/* 的 cgi 文件才会被执行的。

因此，只有 web.xml 的配置、目录结构以及 html 文件中指定的路径三者紧密配合，才有可能成功执行一个 cgi。 
