---
layout:     post
title:      为sproto添加python绑定
subtitle:   
date:       2015-03-19
author:     spin6lock
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - python
---
项目地址：[https://github.com/spin6lock/python-sproto](https://github.com/spin6lock/python-sproto)

第一次写Python的C扩展，留点笔记记录一下。主要的参考文档是：[Extending Python with C/C++](https://docs.python.org/2/extending/extending.html), 之前也看过cython，但是用Python语法写C还是没学会，稍后再尝试用cython写一遍看看。

作为一个C扩展，是以Module的方式import进去代码里使用的，所以需要注册一下，把自己的接口告诉Python解释器。代码如下图：

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
pysproto_methods是一个数组，每个元素是一个三元组{暴露给python的方法名，对应的C函数名，参数格式}，以{NULL, NULL}表示结束。init模块名(void)是一个特殊的函数，当Python里输入import 模块名的时候，C层就会调用 init模块名 来执行模块的初始化工作。Py_InitModule表示将上面的模块方法数组暴露给Python，下面的代码向模块注册了一个SprotoError，表明模块自带的异常类型。Python传参数给C：参见py_sproto_create，通过PyArg_ParseTuple函数接收参数。
```

```
    char *buffer;
    int sz = 0;
    struct sproto *sp;
    if (!PyArg_ParseTuple(args, "s#", &buffer, &sz)) {
        return NULL;
    }
```

C需要返回给Python的，一般有int，string和指针三类。前面两类都可以通过Py_BuildValue解决，参考如下：

```
PyObject *data = Py_BuildValue("s#", (char*)value, length);
```

如果要在不同的C函数之间传递C指针，则需要用到PyCapsule_New来建立一个Capsule，把C指针包起来。这个capsule可以指定名字，方便Python代码里打印。还可以指定destructor，当这个Capsule脱出当前scope，被gc回收的时候，就会调用destructor来析构。Python还贴心的提供了一个Context，用来给这个Capsule带上额外的数据，方便后续使用。

对于python-sproto来说，之前有个问题一直没处理好，sproto_type其实是对sproto的一个指针，指向其成员。所以，如果sproto被gc掉了，sproto_type就有可能出错。而且这个出错是取决于gc时机，如果gc没跑，sproto那块内存还在，就不会出错。这种隐藏的bug比较难查。简单来说，就是C扩展暴露给Python的对象，相互之间对生命周期有依赖关系。sproto_type依赖于sproto，所以sproto的生命周期至少应该和sproto_type一样长。为了向解释器说明这件事，需要用到Py_XINCREF和Py_XDECREF，当生成新的sproto_type的时候，给sproto调用Py_XINCREF，表示对sproto的引用加1，销毁的时候就在析构函数里减1，表示取消引用。

更优雅的做法，应该是把这类生命周期相关的信息，写在脚本里，而不是在C里处理。对外提供的可以是一个Python的类，这个类自己管理相关对象的生命周期，只要这个类还在，就能保证生命周期正确。
