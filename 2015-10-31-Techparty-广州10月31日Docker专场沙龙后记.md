---
layout:     post
title:      Techparty-广州10月31日Docker专场沙龙后记
subtitle:   
date:       2015-10-31
author:     Mehaei
header-img: img/post-bg-BJJ.jpg
catalog: true
tags:
    - python
---
华为的童鞋技术能力很强，但是两位讲师的都没听进去。重点听了两个，一个是芒果TV的Docker 之路，另一个是Coding的实践和思考。

芒果TV的主讲人是一直仰慕的CMGS，从豆瓣出来后去了国企芒果台。因为内部阻力问题，无法实现PaaS。转而实现了细粒度的调度。物理机+Docker为芒果台省了不少机器，而且性能还比AWS的要强。实践上，主要用到了MacVLan，在二层网络上做网络调度。还有Devicemapper，但是dm受镜像大小的影响比较大，超过2G大小的镜像就会有明显的性能下降。Docker里跑的，主要是Redis cluster。80G的redis实例，分成了80个1G的instance来跑，分别错开AOF时机，避免触发OOM。网络设置用的是Eru-agent，自己开发的私货，同时负责监控。Docker自带的监控在早期版本里，一直是个脑残，每秒取一次metric数据，严重影响性能。

Coding的主讲人是叶雨飞。叶大吐槽了Docker的种种缺点，registry废柴，dockerfile和部署用的配置混为一谈，hub上的镜像良莠不齐。然后鲜明的提出了三点：Build-Package-Run。对于运维人员来说，应该做的是运行一个build.sh，然后把packagebuild出来。具体怎么build，应该交回各项目自我管理自我实现。叶大现场还列举了3行的dockerfile，实在是大开眼界。底包由内部每天更新，然后第一行FROM 当日更新好的底包，第二行add 相应的包，第三行直接run包。叶大对动态伸缩也有明确的认识，一般公司都用不着，很多东西可以依赖原有的部署系统实现，不需要另搞一套。灵活性越高，需要的额外工作越高。容器只是当作物理隔离用的东西，就够用了。镜像的locale，timezone之类的，甚至可以直接依赖宿主机。当然，也要保证镜像能够包得起，挪得动，可以封装物理机之间的差异，不会依赖某台特定物理机来跑业务。

具体的ppt还是要等[珠三角技术沙龙](http://techparty.org)的官网了

UPDATE：

官网总结：[http://techparty.org/guangzhou/2015/11/01/guangzhou-docker-event-summary.html](http://techparty.org/guangzhou/2015/11/01/guangzhou-docker-event-summary.html)

芒果TV：[http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/Docker2.pdf](http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/Docker2.pdf)

码市docker总结：[http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/CodingDocker%E6%8A%80%E6%9C%AF%E5%AE%9E%E8%B7%B5%E4%B8%8E%E7%9A%84%E6%80%9D%E8%80%83.pdf](http://7fvga6.com1.z0.glb.clouddn.com/techparty/gztechparty201510/ppt/CodingDocker%E6%8A%80%E6%9C%AF%E5%AE%9E%E8%B7%B5%E4%B8%8E%E7%9A%84%E6%80%9D%E8%80%83.pdf)
