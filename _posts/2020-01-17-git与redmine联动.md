---
layout:     post
title:      "git 与 redmine 联动 "
subtitle:   ""
date:       2020-01-17
author:     "spin6lock"
catalog:    true
tags:
    - git 
    - Redmine
    - Python
---

现在留给开发的提交权限越来越少了，qc 同学为了保证测试覆盖，让搞了个钩子，提交信息里必须写单号，没有 qc 单子的提交会弹钉钉警告，提错版本的也会被警告，心累。最近一周比较闲，决定用 Python 脚本做个类似的检查辅助一下

[ 代码仓库 ](https://github.com/spin6lock/git_with_redmine) fix_issue 是用来关单的，redmine 的页面开着，一段时间后做完，手动标记完成时，如果中间有人改动过，就会将其他人的改动冲掉。。用脚本关就只会改状态了。同时，每个单子的完成状态都不一样，对于功能开发的单子，会比 bug 单多几个状态。。。

check_push 是用来做钩子的，用于检查提交的信息里有没有单号，单号的版本对不对。每一次提交如果有单号，都会去 redmine 检查一次（#0 除外）。如果单号对应的版本，和当前提交的分支版本不一致，就会提交失败。最后还利用 difflib 的字符串相似性，从自己的所有单里找一下，看看有没有标题类似，而版本正确的，自动提示正确单号。这样，从主干 `git cherry-pick` 一个提交过来，即使单号错了，也会被拦下来，提示正确单号，只要动动手 `git commit --amend` 改掉就行

all_issue 是列出当前指派给自己的所有单号，配合 fix_issue，可以批量关闭 redmine 单，比较好用。例如：
``` bash
    ./all_issue.py | grep 版本 1 | xargs ./fix_issue
```
就能批量关单了

最后搞了个 fix_conflict，在大提交 `git cherry-pick` 以后很容易有冲突，冲突后要手动一个个文件打开，编辑冲突，然后 `git add` 一下。这个工具可以帮忙自动调 `$EDITOR` 环境变量来打开冲突文件，最后帮忙 `git add`。~~ 已知的缺陷是，a 文件在分支 1 还在，但分支 2 删掉了，在分支 2 上 cherry-pick 分支 1 的提交，冲突文件里就会有 delete by us 的冲突，最后导致错误 `git add`。目前尚未解决 ~~ EDIT: 已解决 [spin6lock/git_with_redmine@d1c83b6](https://github.com/spin6lock/git_with_redmine/commit/d1c83b61d151b2b6c5fe3d2ccab970222f45937b)

博客将评论系统从 Disqus 换成了 utteranc，还是老外的比较注重权限和隐私。国内的类似插件要求评论者给访问权限，还是整个账号的，太危险了。（说的就是 Gitalk）
