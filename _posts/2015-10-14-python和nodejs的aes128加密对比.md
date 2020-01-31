---
layout:     post
title:      python 和 nodejs 的 aes128 加密对比
subtitle:   
date:       2015-10-14
author:     spin6lock
header-img: img/post-bg-android.jpg
catalog: true
tags:
    - python
---
之前的机器人是用 python 写的，有同事想改写成 nodejs 版，但是验证一直通不过，于是帮忙爬了一下文档。

```
#encoding:utf8

from Crypto.Cipher import AES
import binascii

key = 'abcdabcdabcdabcd'
plaintext = 'Secret Message A'

encobj = AES.new(key, AES.MODE_ECB)
ciphertext = encobj.encrypt(plaintext)

# Resulting ciphertext in hex
print ciphertext.encode('hex')
```

```
var crypto = require("crypto");
var key = new Buffer('abcdabcdabcdabcd','ascii');
var text = 'Secret Message A';

var cipher = crypto.createCipheriv('AES-128-ECB',key,'');
var decipher = crypto.createDecipheriv('AES-128-ECB',key,'');
var c1 = []
var c2 = []
c1.push(cipher.update(text, "ascii", "hex"))
c1.push(cipher.final("hex"))
var encrypted_text = c1.join('')
console.log(encrypted_text)
c2.push(decipher.update(encrypted_text, "hex", "ascii"))
c2.push(decipher.final("ascii"))
console.log(c2.join(''))
```

但是有个问题，nodejs 版加密出来的密文，总是比 python 版要长。感觉 nodejs 最后的 final 方法，输出了多余的东西。参考了一些网文，如果密文不够一个 block，update 是没有输出的，如果超过一个 block，update 只会输出一个 block，剩余的放在 final 里返回。用 python 版解密看了一下，原来 final 在密文刚好一个 block 的情况下，会返回 padding 字符串。。。。
