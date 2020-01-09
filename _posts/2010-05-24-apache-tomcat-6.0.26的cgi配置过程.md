---
layout:     post
title:      apache-tomcat-6.0.26的cgi配置过程
subtitle:   
date:       2010-05-24
author:     spin6lock
header-img: img/post-bg-mma-0.png
catalog: true
tags:
    - python
---
这东西折磨我太久了，写篇笔记。

Apache的目录很好认，我下的是zip绿色版，解压开就看见running这个说明文件了，建议大家读读。

conf目录是放置配置文件的，bin则是可执行文件的位置，只需双击startup.bat，即可启动Apache。

要运行cgi，主要是改两个文件，一个是web.xml，一个是context.xml。

context.xml主要是改这么一行：

直接在context后加上privileged就可以了，用于放行可执行文件。

web.xml修改的是cgi那一段，其实默认也带有cgi的配置的，只是被注释掉而已。

还有：

配置过程中遇到一个问题，就是静态网页可以正常显示，但点击其中的cgi连接时，cgi就被当成文件下载了，而不是由服务器解释执行。

这个问题需要html文件、目录结构和以上web.xml配置的紧密配合才可以解决。

假设当前目录结构是：

cookie 

What is your customer id: <input name="id"><P>

上述的html代码，是无法正常工作的。点击按钮时，Apache会在html所在当前文件夹下寻找cgi文件。但默认的cgi前缀是WEB-INF/cgi-bin，路径不对，无法执行。改成/cookies/cgi-bin/cookie.cgi以后就可以了。

至于cgi没有执行，变成文件下载了，主要是因为web.xml中servlet-mapping那一段的问题，只有路径中带有/cgi-bin/*的cgi文件才会被执行的。

因此，只有web.xml的配置、目录结构以及html文件中指定的路径三者紧密配合，才有可能成功执行一个cgi。 
