---
layout:     post
title:      根据 pythonprotobuf 自动生成 protobuf 包收发接口
subtitle:   
date:       2011-11-07
author:     spin6lock
header-img: img/post-bg-unix-linux.jpg
catalog: true
tags:
    - python
---
利用 protobuf 进行串行化和反串行化处理，封装出来的 rpc 服务很好用。但是有个缺点，就是测试时，一些很简单的接口都要重新实现一次，程序体内就一些简单的赋值语句。写了个代码生成器，用来生成 protobuf 对应的请求函数和回应函数，请求函数根据 req 的内容，生成赋值函数体；回应函数只是负责把服务器返回的包进行打印。

先用 .proto 文件生成 protobuf 的 xxx_pb2.py 文件，将其放入 protobuf 目录

```
#!/usr/bin/env python# -*- coding:utf8 -*-import sysimport protobuf # 生成的 protobuf python 文件目录 def dir_class(obj):    """ dir_class(obj) -> list of string """    names = dir(obj)    names = [name for name in names if not name.startswith('_')]    names = [name for name in names if not name.isupper()]    request_class = [name for name in names if "Req" in name]    response_class = [name for name in names if "Resp" in name]    return request_class, response_class     # 返回接收包和发送包的对应类名称列表 def dir_attr(obj):    """ dir_attr(obj) -> list of string """    names = dir(obj)    names = [name for name in names if not name.startswith('_')]    names = [name for name in names if name.islower()]    return names                             # 返回一个类的内部属性 def gen_req(obj, class_name):    text = []    attrs = dir_attr(obj)    line = gen_func_def(camercase_to_underscore(class_name), attrs)    text.append(line)    cp_statement = gen_cp(class_name, attrs)    text.extend(cp_statement)    line = "\tsingle_request(req)"    text.append(line)    return text                              # 生成请求类的函数体 def gen_func_def(func_name, arglist):    line = "def " + func_name + "("    if not arglist:        line += "):"        return line    line += ", ".join(arglist) + "):"    return linedef gen_cp(class_name, attrs):    text = []    text.append("\treq = " + class_name + "()")    for attr in attrs:        line = "\treq." + attr + " = " + attr        text.append(line)    return textdef camercase_to_underscore(var_name):    result = []    start = 0    for i, char in enumerate(var_name):        if char.isupper():            result.append(var_name[start:i])            start = i    result.append(var_name[start:])    underscore_name = "_".join([var.lower() for var in result])    underscore_name = underscore_name[1:]    return underscore_name                  # 驼峰命名法到下划线分割的命名 def underscore_to_camercase(var_name):    result = var_name.split("_")    result = [word.capitalize() for word in result]    return "".join(result)                  # 下划线分割的命名到驼峰法命名 def main():    with open(sys.argv[1]) as fh:        lines = fh.readlines()        for line in lines:            line = line.strip()            if line.startswith("protobuf"):                #import package                __import__(line, globals(), locals(), [], -1)                #analysis class                protobuf_package = eval(line)                    pb2_req, pb2_resp = dir_class(protobuf_package)                #gen request function and resp printer                req_funcs = []                for req in pb2_req:                    req_func = gen_req(eval(line + "." + req + "()"), req)                    req_funcs.extend(req_func)                    req_funcs.append("")                #write file                filename = line[len("protobuf") + 1:]                filename = filename[:-4]                import_statement = "from " + line + "" + "import *"                body = "\n".join(req_funcs)                with open(filename+".py", "w") as f:                    print filename                    f.write("\n".join([import_statement, body]))if __name__ == '__main__':    main()
```


