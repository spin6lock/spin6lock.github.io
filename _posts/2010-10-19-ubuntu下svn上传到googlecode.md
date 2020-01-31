---
layout:     post
title:      ubuntu 下 svn 上传到 googlecode
subtitle:   
date:       2010-10-19
author:     spin6lock
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - python
---
在 Google code 上也混迹了一段时间，提交 patch 和 issue 都试过了，可惜一直没找到哥们给个 commitor 当当。今天特地去挖了个坑，试试 owner 的滋味。

1. 在 source 下的 checkout 里，可以很清晰地看到需要填写的命令。可是 ubuntu 的 svn 有点诡异，以 ownership checkout 一个 project，居然也不需要输入密码，搞了我很长时间。
1. 更纠结的还在后头，svn add 添加完文件，svn commit 进行提交，发现首先要输入的是一个 Gnome keyring(null) 的密码，我输了很多遍 google code 的密码和邮箱密码，都不对，原来那是本机用户的密码。
1. 接下来 google code 的服务器就会问你要帐号，若是 gmail 账户的话直接输入用户名即可，不用添加 @gmail。
1. 接下来输入的是 google code 的密码。可以在 http://code.google.com/hosting/settings 里找到，这个密码十分复杂的说，在命令行下输入相当有难度。
