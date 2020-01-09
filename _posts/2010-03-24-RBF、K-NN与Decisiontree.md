---
layout:     post
title:      RBF、K-NN与Decisiontree
subtitle:   
date:       2010-03-24
author:     spin6lock
header-img: img/home-bg-geek.jpg
catalog: true
tags:
    - python
---
要做一个classifier，的确不易。面对需要训练的classifier，是否training error越少越好呢？显然不是，因为虽然training error降低了，但test error不见得就会降低，实际表现为一个拐点。如下图：

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/%E6%A8%A1%E5%BC%8F%E8%AF%86%E5%88%AB-training-error%E4%B8%8Etest-error.png" width="489" height="308" alt="" /> 

为了平衡error的权重，我们引入了额外的函数lambda*，训练效果由error和 lambda*共同评价。下面讨论一下lambda的取值：

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/lambda_is_0.png" width="453" height="298" border="5" alt="" /> 

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/lambda_is_between_0and1.png" width="453" height="298" border="5" alt="" /> （存疑）

因此，我们采取多个函数综合评估的方式进行，即RBF（radial base function）

RBF采取多个正态分布函数进行评估，各函数的均值和方差不一样。

（待续）

K-NN 最近邻算法。俗话说物以类聚，人以群分。该算法就是采用离目标点最近的k个邻居，对目标点进行分类。但k值的选取非常关键，而且易受干扰。

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/decisionTree.png" width="453" height="298" alt="" /> 

<img src="http://images.cnblogs.com/cnblogs_com/lifehacker/decisionTree2.png" width="453" height="298" alt="" /> 
