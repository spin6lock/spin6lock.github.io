---
layout:     post
title:      TheImplementationofLua5.0阅读笔记（一）
subtitle:   
date:       2013-07-16
author:     spin6lock
header-img: img/post-bg-desk.jpg
catalog: true
tags:
    - python
---
没想到Lua的作者理论水平这么高，这篇文章读的我顿生高屋建瓴之感。云风分享了一篇中译：[http://www.codingnow.com/2000/download/The%20Implementation%20of%20Lua5.0.pdf](http://www.codingnow.com/2000/download/The%20Implementation%20of%20Lua5.0.pdf)

全篇的主题有4个：1.基于寄存器的虚拟机；2.用于将table作为数组使用的新算法；3.闭包的实现；4.以及协程。第二点我关注不多，会写的比较简略。

1 简介

简介主要就是说，我们搞Lua嘛，就是一个实验室出来的产品，没想到今天在工业界特别是游戏界红得发紫，这主要是得益于Lua轻灵小巧，注重可移植性。除了上面提到的4点，这篇文章还有一些铺垫的章节，帮助你们理解我们这个牛逼哄哄的东西。（这些铺垫的东东也很牛逼，建议参考中译）

2 Lua的设计和实现

我们写的Lua简洁，高效，可移植，非常容易嵌入。

3 Lua的类型系统

这段看代码比较简洁：

```
typedef struct {
   int t;
  Value v; 
} TObject;

typedef union {
  GCObject *gc;
  void *p;
  lua_Number n;
  int b;
} Value;
```

作者顺便扯了一下对象的装箱拆箱，嘲笑python的实现比Lua要慢。

4 Lua的Table

牛逼的地方在于，如果table是当array用，数字的key比较紧凑，我们就会拿一个真实的数组去储存它，即省空间又快速，如果是当成单纯的关联组来用，那么数组部分则不会分配，避免浪费

5 函数和闭包的实现

闭包在lua里应用得非常广泛。每一个函数都会被编译成一个prototype作为原型。实际执行的时候，则会为其生成一个闭包，包含了对函数原型的引用，对全局变量的引用表，以及对upvalue的引用（用来访问外部的局部变量）。

以函数为第一类对象，以及带词法作用域的语言，大多会遇到外部局部变量访问的问题。考虑下面的例子：

```
function add(x)
    return function(y)
                   return x + y
               end
end

add2 = add(2)
print(add2(5))
```

当调用add2的时候，add函数已经返回，那么add2函数体内的x会不会随着add函数的退栈而被销毁呢？如果不被销毁，又应该如何保存这个变量呢？

Lua巧妙的使用了upvalue解决这一问题，参考下图：

<img src="http://images.cnitblog.com/blog/90397/201307/16115447-3d58f97b68d044a5aae91c0a2f1c63da.png" alt="" width="648" height="469" />

每当创建一个新闭包，Lua就会检查外部定义的局部变量是否有加入upvalue链表，如果没有就创建一个upvalue加入双向链表里。所有对外部定义的局部变量访问，都是通过upvalue的指针进行间接访问的。当外部函数退出时，因为函数退栈，局部变量被清理，这时候局部变量就会被转存在upvalue的值域里，然后把upvalue的指针指向自身的值域。对于定义局部变量的函数，这些局部变量还是栈上的元素，不许通过upvalue访问。

对于多层函数嵌套的情况，当一个函数需要访问的变量不在上一层函数的局部变量，就访问上一层函数的闭包。闭包具有传递性，会由外部函数传递到内部。

下篇：[The implementation of Lua 5.0 阅读笔记（二）](http://www.cnblogs.com/Lifehacker/p/the_implementation_of_lua5_review_part2.html)
