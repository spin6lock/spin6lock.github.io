---
layout:     post
title:      【翻译】HowwemakeGitHubfast( 我们如何让 github 更快 )
subtitle:   
date:       2012-05-20
author:     spin6lock
header-img: img/post-bg-alibaba.jpg
catalog: true
tags:
    - python
---
译者注：我是一名开源爱好者，十分喜爱 github，github 也是一个乐于分享的站点。这篇文章介绍了 github 为应对更高访问量而搭建的架构，虽然已经是 09 年的文章，仍有一定的参考价值，因此翻译此文分享给大家

<li id="post_530" class="hentry post">
<h2>[ 我们如何让 github 变得更快 ](https://github.com/blog/530-how-we-made-github-fast) <small></small></h2>

<img src="http://www.cnblogs.com/Lifehacker/admin/ 我们如何让 github 变得更快 _files/25c7c18223fb42a4c6ae1c8db6f50f9b" alt="" width="16" height="16" /> [mojombo](https://github.com/mojombo) [October 20, 2009](https://github.com/blog/530-how-we-made-github-fast#comments)
 


Translations: [Беларускі](http://www.fatcow.com/edu/how-we-made-github-fast-be-be/), [Deutsch](http://www.leiste.de/science/wie-we-made-github-schnelle), [Русский](http://web-meister.ru/science/kak-my-sdelali-github-bystrym).
现在工作已经上了轨道，我想和各位分享一下，为了让 github 更快速，更具扩展性，我们在 github 架构上作的改动。
 
在这篇文章的第一版里，我花了相当长的篇幅，仔细解释我们所做的每一个技术选择。但是，这篇文章迅速变得混乱，演讲与关于架构的讨论混在一起。所以我决定先简单的解释架构本身，再通过随后的文章详细解释我们做出的技术选择。
 
现代 web 应用有很多扩展的方式。我这里描述的只是我们所选择的那种。这不应该被视为唯一的扩展方式。请将之视为一个独特的案例，满足我们单一需求的案例。
<h3>理解所用协议</h3>
我们向最终用户开放了三种协议 : HTTP, SSH, 和 Git. 当使用网页浏览器上网时 , 你使用的是 HTTP 协议 . 当你 clone，pull 或者 push 去一个私有的 URL 例如 git@github.com:mojombo/jekyll.git 时，你在使用 SSH 协议 . 当你 clone 或者 pull 一个公开的 URL 时，例如 `git://github.com/mojombo/jekyll.git`， 你在使用 Git 协议。
要了解这个体系，最简单的方法是跟踪这些请求是如何在系统内传递的。
<h3>跟踪 HTTP 请求</h3>
在这个例子里，我将向你展示，对 [http://github.com/mojombo/jekyll](http://github.com/mojombo/jekyll) 请求一页树状图时发生了什么。
 
从互联网上来的请求，首先会到达负载均衡器。对于这个任务，我们使用了一对跑着 [ldirectord](http://www.vergenet.net/linux/ldirectord/) 的 Xen 实例来完成。暂且将其称为 `lb1a` 和 `lb1b`. 任何时间里，这两台机器都有一个处于活动状态，另一个时刻准备进行故障切换。负载均衡器没有做什么神奇的事。它只是负责把 TCP 数据包根据来源 IP 和端口转发到不同的服务器，并且负责清理负载池里的异常服务器。当池里没有任何可用的服务器时，负载均衡器将返回一个简洁的静态页面（而非拒绝连接）。
 
对于主站的请求，负载均衡器会把你的请求传到 4 个前端机器的一个。这些机器的配置，都是 8 核心，16G 内存的裸机环境（bare metal server）它们称为 `fe1`, , `fe4`。[Nginx](http://nginx.net/) 负责接受连接，并将其发往 Unix socket，这个 socket 是通过 16 个 [Unicorn](http://github.com/blog/517-unicorn) 工作进程支持的。16 个 Unicorn 工作进程的其中一个，会调用 [Rails](http://rubyonrails.org/) 代码完成请求。
 
很多页面需要数据库查询。我们的 MySQL 数据库运行在两台 8 核心 , 32GB 内存的裸机服务器上，配备有 15k RPM SAS 硬盘。 它们是 `db1a` 和 `db1b`.。它们在任何时候，均处于一主一从的状态。MySQL 同步是通过 [DRBD](http://www.drbd.org/) 完成的。
 
如果一个页面需要 Git 仓库的信息，而这个信息不在缓存中，那就会调用我们的 [Grit](http://github.com/mojombo/grit) 库获取数据。为了适应我们的 Rackspace 设置，我们对 Grit 做了一点修改。我们首先把所有需要访问文件系统的调用都封装到 Grit::Git 对象身上。 然后将 Grit::Git 替换为一个通过 RPC 调用 Smoke 服务的桩 (stub) Smoke 对仓库有直接的磁盘访问权限，从而把 Grit::Git 封装成一个服务。Smoke 意即云中的 Grit。
 
Grit 桩对 `smoke` 发起 RPC 调用，经过负载均衡发送到 `fe` 上。每一个前端跑了四个 [ProxyMachine](http://github.com/mojombo/proxymachine) 实例，处在 [HAProxy](http://haproxy.1wt.eu/) 后，扮演着 Smoke 调用的路由代理的角色。ProxyMachine 是一层内容敏感的 (OSI 第 7 层 ) TCP 路由代理， 我们可以通过它使用 Ruby 编写路由算法。 代理服务器将每个请求中的仓库所属用户名抽出。然后我们会调用一个鉴权库 Chimney ( 意为烟囱，与前文的 smoke 语带相关 ) 来定位到用户。一个用户的路由表项就是用户仓库所在的文件服务器的主机名 (hostname)
 
Chimney 的路由项是向 [Redis](http://code.google.com/p/redis/) 查询得到的。Redis 在数据库服务器上面运行。我们将 Redis 用作一个 key/value 对持续化储存的数据库，储存路由信息和其他丰富的信息。
 
一旦 Smoke 代理发现了用户的路由项，就会建立一个到文件服务器的透明代理。我们有四对文件服务器。他们的名字是 `fs1a`, `fs1b`, , `fs4a`, `fs4b`。这都是 8 核心、16GB 内存 裸机服务器，每一个配备有 6 个 300GB 15K RPM SAS 硬盘， 组织为 RAID 10 磁盘队列。任何时间里，每对机器都处于双机热备的主备方式。所有的仓库数据都会定期通过 DRBD 进行主从备份。
 
每个文件服务器运行着两个 [Ernie](http://github.com/mojombo/ernie) RPC 服务，它们都处在 HAProxy 之后。每一个 Ernie 拥有 15 个 Ruby workers。这些工作进程接受 RPC 调用并进行 Grit 调用。返回值是通过 Smoke 代理返回到 Rails 应用的，对应的 Grit 桩则返回预期的 Grit 响应。
 
当 Unicorn 完成了 Rails 的调用后，响应包通过 Nginx 直接传回到客户端（期间不经过负载均衡器）。
 
最后，你看到了一个相当漂亮的网页。
 
上面的场景是缓存没有命中时发生的。在多数情况下，Rails 的代码会使用 Evan Weaver 的 Ruby [memcached](http://github.com/fauna/memcached/) 客户端查询 [Memcache](http://www.danga.com/memcached/) 服务器， 每个从 (slave) 文件服务器上都会运行。因为这些机器相当空闲，我们在每台机上放置了 12GB 的 Memcache。暂且称它们为 `memcache1`, , `memcache4`.
<h3>BERT 和 BERT-RPC</h3>
对于我们的数据串行化和 RPC 协议，我们使用 BERT 和 BERT-RPC。你从前从未听说过它们，因为它们是全新的。我对我尝试过的所有可选项都不满意，我也希望实现萦绕在心头的一个想法，所以我创造了它们。在你对 NIH 综合征生厌之前 ( 或帮助你解决这个症状 )，请阅读我与之相关的另一篇文章：[Introducing BERT and BERT-RPC](http://github.com/blog/531-introducing-bert-and-bert-rpc)（对 BERT 和 BERT-RPC 的简介）。文章里会介绍这些技术是怎么来的，以及我希望用它们来解决什么样的问题。
 
如果你只想看看规范说明，请点击 [http://bert-rpc.org](http://bert-rpc.org/)。
 
对于代码狂，请 check out 我的 Ruby BERT 串行库 [BERT](http://github.com/mojombo/bert)， 我的 Ruby BERT-RPC 客户端 [BERTRPC](http://github.com/mojombo/bertrpc)，以及我的 Erlang/Ruby 混合 BERT-RPC 服务器 [Ernie](http://github.com/mojombo/ernie)。这就是我们 Github 用于储存所有仓库数据的库，经过实战检验 :)
 
<h3>跟踪 SSH 请求</h3>
Git 使用 SSH 作为加密通讯协议，用于你和服务器之间的通讯。为了了解我们的架构是如何处理 SSH 连接的，首先需要知道 SSH 是如何运作的。
 
Git 依赖于 SSH 提供的在远端服务器执行命令的功能。例如，执行 ssh tom@frost ls -al 会在 tom 的 home 目录上运行 `ls -al` ，home 目录所在的机器是 `frost` 。我可以在我的本地终端上得到结果。SSH 实际上把远程服务器上的 STDIN, STDOUT, 以及 STDERR 挂接到我本地终端上来了。
 
如果你执行 git clone tom@frost:mojombo/bert, Git 实际执行的会是，SSH 到 `frost`，以 `tom` 的身份登录，然后远程执行 `git upload-pack mojombo/bert` 命令。然后你的客户端就能和远程服务器在 SSH 连接里通讯。很简洁是吧？
 
当然，允许任意执行指令是很危险的。所以 SSH 有个功能，用于限制能够远程执行的命令。简单来说，可以限制为 [git-shell](http://www.kernel.org/pub/software/scm/git/docs/git-shell.html) ，一个 Git 附带的小玩意。这些脚本会保证，你执行的是以下 `git upload-pack`, `git receive-pack` 或者 `git upload-archive` 这三者中的一个。如果真的是其中之一，则会调用 [exec](http://linux.die.net/man/3/exec) 用新进程替换当前进程。然后，就能够得到相应结果，就像你直接执行那个命令一样。
 
现在你知道了 Git 的 SSH 的基本原理了，接下来我会向你介绍这一切是怎么在 Github 架构里完成的。
 
首先，你的 Git 客户端会初始化一个 SSH 会话这个连接首先到达我们的负载均衡器。
然后，这个连接会到达其中一个前端，由 [SSHD](http://www.au.kernel.org/software/scm/git/docs/git-daemon.html) 接受。 我们对 SSH 守护精灵做了 patch（补丁），使其可以在 MySQL 数据库里进行公钥查找。你的公钥标示了你的用户身份，这个信息会和原始命令参数一起送达到我们的专有脚本 Gerve (Git sERVE)。请将 Gerve 理解为 `git-shell` 的超级智能版。
 
Gerve 可以检测你是否对仓库有相应的执行权限。如果你是仓库属主，则拥有所有权限。否则， 会发起多个 SQL 查询去定位你的权限。
 
当访问被允许后， Gerve 使用 Chimney 来查找仓库的路由。现在的目标，已经变成在合适的文件服务器上执行你的原始命令，并且将你的本地机器挂接到那上面来。免去了另一次 SSH 的启动，牛吧？
 
或许这听起来有些疯狂，但是这方案工作的很好！Gerve 只是使用 `exec(3)` 来将自己的进程替换为 ssh git@<路由> <命令> <参数>. 这次调用之后，你的客户端就挂接在一个前端机器的进程上，而前端机器的进程则挂接在一个文件服务器的进程上。
 
想想这种解决方案有多么美妙：在确认了权限和仓库的位置之后，前端机器在会话的剩余时间里，只充当一个透明代理。这个方案唯一的缺陷，就是内部的 SSH 需要进行无谓的加解密操作（内网安全，无必要加解密）。我们可以将内部的 SSH 替换为某种更为简单高效的连接，但是原方案实在是太简单直接（而且还非常快！），所以目前我们还没有太大的动力去做这个优化。
<h3>跟踪一个 git 请求</h3>
执行公共仓库的 clone 和 pull 操作就跟 SSH 的一样。 不需要 SSH 进行鉴权和加密，只需一个服务器端的 [Git Daemon](http://www.au.kernel.org/software/scm/git/docs/git-daemon.html)。这个 daemon 负责接受连接，检验所需运行的命令， 然后使用 `fork(2)` 和 `exec(3)` 来产生子命令进程。
记住这个概念，下文我将为你展示一个公开的 clone 操作是怎么进行的。
首先，你的 Git 客户端发起了一个 [ 请求 ](http://github.com/mojombo/egitd/blob/master/docs/protocol.txt) ，这个请求包含了你需要执行的命令和对应的仓库名。请求首先进入我们的负载均衡系统。
 
从那里开始，请求将发往其中一个前端。每个前端跑 4 个 ProxyMachine 实例，前面则有 HAProxy 挡着作为 Git 协议的路由代理。代理会从请求中抽取出仓库名（或者 gist 的名字）。然后使用 Chimney 查询路由表。如果没有发生其他的错误，代理就会通过 Git 协议向 Git 客户端发回合适的信息。当路由查询完毕，仓库名（例如 `mojombo/bert`）就会转换为磁盘路径名 ( 例如 `a/a8/e2/95/mojombo/bert.git`). 以前的配置里，我们没有使用代理，所以我们需要一个修改过的 daemon，使其能够将对应的用户 / 仓库转换为合适的文件路径。通过代理完成这一步骤，我们就能使用一个未经修改的 daemon，使得升级路径变得更简单。
 
然后，Git 代理建立了一个到文件服务器的透明代理，转发（经过修改仓库路径）的请求。每个文件服务器运行着两个 Git Daemon 进程，均处于 HAProxy 后面。Daemon 会使用文件打包协议，将数据流打回到 Git 代理，直接和你的 Git 客户端通信。
 
当你的代理得到了所有数据，你就已经克隆了仓库，而且可以开始工作了！
<h3>子系统和网站系统</h3>
除了主要的 web 应用程序和 Git 系统外，我们还运行着多种子系统和网站系统。子系统包括工作队列，打包下载，账单管理，镜像系统，svn 导入等。网站系统包括 GitHub 网页，Gist，gem 服务器，还有一打的内部工具。这些子系统的一部分是如何在新架构下运行的，我们创造了哪些新技术，去让应用跑得更为平稳，将会在未来的一系列文章中讲解，敬请期待
<h3>总结</h3>
这里描述的架构很好的适应了我们对网站架构的扩展，而且还让整个站点的性能得到了质的提升。以前，我们的 Rails 应用平均响应时间是 500ms 到数秒，取决于系统的负载。转移到裸机和 Rackspace 的联合储存 (federated storage) 以后，我们的 Rails 应用响应时间降到了 100ms 以下。而且，工作队列可以轻松应付每天 28000 个背景作业而游刃有余了。当前的硬件集威力还没有完全发挥，我们有更大的成长空间，而且当需要扩展时，我们能够轻易加入更多的服务器。我对这一切感到惬意，如果你像我一样，你一定在每天享受崭新的 GitHub 了！

</li>

### 理解所用协议

### BERT 和 BERT-RPC

### 跟踪一个 git 请求

### 总结
