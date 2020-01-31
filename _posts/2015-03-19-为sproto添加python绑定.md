---
layout:     post
title:      为 sproto 添加 python 绑定
subtitle:   
date:       2015-03-19
author:     spin6lock
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - python
---
项目地址：[https://github.com/spin6lock/python-sproto](https://github.com/spin6lock/python-sproto)

第一次写 Python 的 C 扩展，留点笔记记录一下。主要的参考文档是：[Extending Python with C/C++](https://docs.python.org/2/extending/extending.html), 之前也看过 cython，但是用 Python 语法写 C 还是没学会，稍后再尝试用 cython 写一遍看看。

作为一个 C 扩展，是以 Module 的方式 import 进去代码里使用的，所以需要注册一下，把自己的接口告诉 Python 解释器。代码如下图：

```
static PyMethodDef pysproto_methods[] = {
    {"sproto_create", py_sproto_create, METH_VARARGS},
    {"sproto_type", py_sproto_type, METH_VARARGS},
    {"sproto_encode", py_sproto_encode, METH_VARARGS},
    {"sproto_decode", py_sproto_decode, METH_VARARGS},
    {"sproto_pack", py_sproto_pack, METH_VARARGS},
    {"sproto_unpack", py_sproto_unpack, METH_VARARGS},
    {"sproto_protocol", py_sproto_protocol, METH_VARARGS},
    {NULL, NULL}
};

PyMODINIT_FUNC
initpysproto(void){
    PyObject *m;
    m = Py_InitModule("pysproto", pysproto_methods);
    if (m == NULL) {
        return;
    }
    SprotoError = PyErr_NewException("pysproto.error", NULL, NULL);
    Py_INCREF(SprotoError);
    PyModule_AddObject(m, "error", SprotoError);
}
```

```
pysproto_methods 是一个数组，每个元素是一个三元组 { 暴露给 python 的方法名，对应的 C 函数名，参数格式 }，以 {NULL, NULL} 表示结束。init 模块名 (void) 是一个特殊的函数，当 Python 里输入 import 模块名的时候，C 层就会调用 init 模块名 来执行模块的初始化工作。Py_InitModule 表示将上面的模块方法数组暴露给 Python，下面的代码向模块注册了一个 SprotoError，表明模块自带的异常类型。Python 传参数给 C：参见 py_sproto_create，通过 PyArg_ParseTuple 函数接收参数。
```

```
    char *buffer;
    int sz = 0;
    struct sproto *sp;
    if (!PyArg_ParseTuple(args, "s#", &buffer, &sz)) {
        return NULL;
    }
```

C 需要返回给 Python 的，一般有 int，string 和指针三类。前面两类都可以通过 Py_BuildValue 解决，参考如下：

```
PyObject *data = Py_BuildValue("s#", (char*)value, length);
```

如果要在不同的 C 函数之间传递 C 指针，则需要用到 PyCapsule_New 来建立一个 Capsule，把 C 指针包起来。这个 capsule 可以指定名字，方便 Python 代码里打印。还可以指定 destructor，当这个 Capsule 脱出当前 scope，被 gc 回收的时候，就会调用 destructor 来析构。Python 还贴心的提供了一个 Context，用来给这个 Capsule 带上额外的数据，方便后续使用。

对于 python-sproto 来说，之前有个问题一直没处理好，sproto_type 其实是对 sproto 的一个指针，指向其成员。所以，如果 sproto 被 gc 掉了，sproto_type 就有可能出错。而且这个出错是取决于 gc 时机，如果 gc 没跑，sproto 那块内存还在，就不会出错。这种隐藏的 bug 比较难查。简单来说，就是 C 扩展暴露给 Python 的对象，相互之间对生命周期有依赖关系。sproto_type 依赖于 sproto，所以 sproto 的生命周期至少应该和 sproto_type 一样长。为了向解释器说明这件事，需要用到 Py_XINCREF 和 Py_XDECREF，当生成新的 sproto_type 的时候，给 sproto 调用 Py_XINCREF，表示对 sproto 的引用加 1，销毁的时候就在析构函数里减 1，表示取消引用。

更优雅的做法，应该是把这类生命周期相关的信息，写在脚本里，而不是在 C 里处理。对外提供的可以是一个 Python 的类，这个类自己管理相关对象的生命周期，只要这个类还在，就能保证生命周期正确。
