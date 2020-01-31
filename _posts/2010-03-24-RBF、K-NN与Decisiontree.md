---
layout:     post
title:      RBF、K-NN 与 Decisiontree
subtitle:   
date:       2010-03-24
author:     spin6lock
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - python
---
要做一个 classifier，的确不易。面对需要训练的 classifier，是否 training error 越少越好呢？显然不是，因为虽然 training error 降低了，但 test error 不见得就会降低，实际表现为一个拐点。如下图：

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/%E6%A8%A1%E5%BC%8F%E8%AF%86%E5%88%AB-training-error%E4%B8%8Etest-error.png" width="489" height="308" alt="" /> 

为了平衡 error 的权重，我们引入了额外的函数 lambda*，训练效果由 error 和 lambda* 共同评价。下面讨论一下 lambda 的取值：

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/lambda_is_0.png" width="453" height="298" border="5" alt="" /> 

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/lambda_is_between_0and1.png" width="453" height="298" border="5" alt="" /> （存疑）

因此，我们采取多个函数综合评估的方式进行，即 RBF（radial base function）

RBF 采取多个正态分布函数进行评估，各函数的均值和方差不一样。

（待续）

K-NN 最近邻算法。俗话说物以类聚，人以群分。该算法就是采用离目标点最近的 k 个邻居，对目标点进行分类。但 k 值的选取非常关键，而且易受干扰。

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/decisionTree.png" width="453" height="298" alt="" /> 

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/decisionTree2.png" width="453" height="298" alt="" /> 
