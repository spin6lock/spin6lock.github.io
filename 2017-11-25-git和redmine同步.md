---
layout:     post
title:      git和redmine同步
subtitle:   
date:       2017-11-25
author:     Mehaei
header-img: img/post-bg-miui6.jpg
catalog: true
tags:
    - python
---
最近实现了github以及内部的gitbucket与redmine的同步。

redmine是内部使用的一套工单系统，用于跟踪bug和需求，由于最近同时开发的版本比较多，在不同分支的提交容易漏掉。现在改为用redmine的工单跟踪需求和bug修复，提交的时候，只要在提交日志里写上单号，机器人就可以将提交信息同步到表单，可以方便的跟踪到提交有没有漏提交到指定分支。

实现上居然很简单，整个过程还是很愉悦的。gitbucket方面比较简单，gitbucket的仓库属主可以添加一个hook，每次提交的时候gitbucket会调一下hook。调用里会包含提交的详细信息，包括分支、提交信息、具体改动的网页版地址。只要用正则搜出单号，然后利用redmine的rest api提交到表单里，就完成任务了。

github的动手前觉得困难一点，因为github在外网，工单系统是内网访问的。没想到github体贴的推荐了ngrok作为安全的内网穿透工具。指定好协议和端口号之后，启动ngrok客户端，会自动随机生成一个https的二级域名。对这个域名的访问，会落到内网的ngrok客户端上。中间的通讯是加密的。这项服务这么优秀，居然还是免费的！比国内的花某壳好多了。

打通内外网之后，剩下的步骤就和gitbucket的相差不多了。github的好处是每个人都可以对仓库设置自己的hook，还不止一个。遇到的小小的梗，是github的时间就是国内时区的，不像gitbucket还要从零时区算时间偏移。调试也很方便，每一次推送都可以在github上查阅到具体的请求内容，还能方便的redeliver，调到合适为止。

以后可以在表单里写明需要提交到哪些分支，然后提交后隔一段时间自动检查，发现有漏提交就提醒程序或者策划，不过目前很懒，没有动力做这个QAQ
