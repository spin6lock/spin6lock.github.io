---
layout:     post
title:      Techparty- 广州 10 月 31 日 Docker 专场沙龙后记
subtitle:   
date:       2015-10-31
author:     spin6lock
header-img: img/post-bg-BJJ.jpg
catalog: true
tags:
    - python
---
华为的童鞋技术能力很强，但是两位讲师的都没听进去。重点听了两个，一个是芒果 TV 的 Docker 之路，另一个是 Coding 的实践和思考。

芒果 TV 的主讲人是一直仰慕的 CMGS，从豆瓣出来后去了国企芒果台。因为内部阻力问题，无法实现 PaaS。转而实现了细粒度的调度。物理机 +Docker 为芒果台省了不少机器，而且性能还比 AWS 的要强。实践上，主要用到了 MacVLan，在二层网络上做网络调度。还有 Devicemapper，但是 dm 受镜像大小的影响比较大，超过 2G 大小的镜像就会有明显的性能下降。Docker 里跑的，主要是 Redis cluster。80G 的 redis 实例，分成了 80 个 1G 的 instance 来跑，分别错开 AOF 时机，避免触发 OOM。网络设置用的是 Eru-agent，自己开发的私货，同时负责监控。Docker 自带的监控在早期版本里，一直是个脑残，每秒取一次 metric 数据，严重影响性能。

Coding 的主讲人是叶雨飞。叶大吐槽了 Docker 的种种缺点，registry 废柴，dockerfile 和部署用的配置混为一谈，hub 上的镜像良莠不齐。然后鲜明的提出了三点：Build-Package-Run。对于运维人员来说，应该做的是运行一个 build.sh，然后把 packagebuild 出来。具体怎么 build，应该交回各项目自我管理自我实现。叶大现场还列举了 3 行的 dockerfile，实在是大开眼界。底包由内部每天更新，然后第一行 FROM 当日更新好的底包，第二行 add 相应的包，第三行直接 run 包。叶大对动态伸缩也有明确的认识，一般公司都用不着，很多东西可以依赖原有的部署系统实现，不需要另搞一套。灵活性越高，需要的额外工作越高。容器只是当作物理隔离用的东西，就够用了。镜像的 locale，timezone 之类的，甚至可以直接依赖宿主机。当然，也要保证镜像能够包得起，挪得动，可以封装物理机之间的差异，不会依赖某台特定物理机来跑业务。

具体的 ppt 还是要等 [ 珠三角技术沙龙 ](http://techparty.org) 的官网了

UPDATE：

[ 官网总结链接：](http://techparty.org/guangzhou/2015/11/01/guangzhou-docker-event-summary.html)

[ 芒果 TV：](http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/Docker2.pdf)

[ 码市 docker 总结：](http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/CodingDocker%E6%8A%80%E6%9C%AF%E5%AE%9E%E8%B7%B5%E4%B8%8E%E7%9A%84%E6%80%9D%E8%80%83.pdf)
