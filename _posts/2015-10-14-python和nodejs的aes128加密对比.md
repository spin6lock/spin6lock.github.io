---
layout:     post
title:      python和nodejs的aes128加密对比
subtitle:   
date:       2015-10-14
author:     Mehaei
header-img: img/post-bg-android.jpg
catalog: true
tags:
    - python
---
之前的机器人是用python写的，有同事想改写成nodejs版，但是验证一直通不过，于是帮忙爬了一下文档。

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

但是有个问题，nodejs版加密出来的密文，总是比python版要长。感觉nodejs最后的final方法，输出了多余的东西。参考了一些网文，如果密文不够一个block，update是没有输出的，如果超过一个block，update只会输出一个block，剩余的放在final里返回。用python版解密看了一下，原来final在密文刚好一个block的情况下，会返回padding字符串。。。。
