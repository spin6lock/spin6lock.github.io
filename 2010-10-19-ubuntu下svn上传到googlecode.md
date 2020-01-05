---
layout:     post
title:      ubuntu下svn上传到googlecode
subtitle:   
date:       2010-10-19
author:     Mehaei
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - python
---
在Google code上也混迹了一段时间，提交patch和issue都试过了，可惜一直没找到哥们给个commitor当当。今天特地去挖了个坑，试试owner的滋味。

1. 在source下的checkout里，可以很清晰地看到需要填写的命令。可是ubuntu的svn有点诡异，以ownership checkout一个project，居然也不需要输入密码，搞了我很长时间。
1. 更纠结的还在后头，svn add添加完文件，svn commit进行提交，发现首先要输入的是一个Gnome keyring(null)的密码，我输了很多遍google code的密码和邮箱密码，都不对，原来那是本机用户的密码。
1. 接下来google code的服务器就会问你要帐号，若是gmail账户的话直接输入用户名即可，不用添加@gmail。
1. 接下来输入的是google code的密码。可以在http://code.google.com/hosting/settings里找到，这个密码十分复杂的说，在命令行下输入相当有难度。
