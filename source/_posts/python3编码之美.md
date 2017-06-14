---
title: python3编码之美
date: 2017-04-18 10:21:59
comments: true
tags: 
- python编码
categories: 编程之道
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">终是谁使弦断，花落肩头，恍惚迷离</blockquote>
　　之前一直在使用python2.x版本，其中的编码问题颇为头疼，根据使用经验以及实验测试，前些日子总结了一些关于python2.x的编码问题，会在本文最后给出地址。本篇主要描述python3中的编码，如果称Python2的编码为殇，那么Python3的编码就应该为美了。
<!--more -->
　　我在python2编码之殇一文的最后介绍过，想要解决python2中的编码问题，最直接有效的方法就是将所有外部的字符串转变为unicode格式，再在python内部了流转。python3正是在这方面做了很大的优化。
　　python3中也有2种编码格式，分别为str与byte，这里的str相当于2中的unicode，byte相当于2中的str。再者python3将python源代码编码从ascii改成了utf-8，从外部接收的编码自动转化成了str(2中的unicode)，大大减少产生编码异常的点。与2一样，3中的编码原则就是将外部接收的字符编码成str（unicode字符），输出时再编码成bytes编码。光说没用，我用实验证明。

### bytes/str/unicode区别
更新于2017年5月2号
#### python3的bytes与str
　　bytes表示字符的原始8位值，str表示Unicode字符。将unicode字符表示为二进制数据（原始8位值），最常见的编码方式就是UTF-8。python2与3中的unicode字符没有和特定的二进制编码相关联，因此需要使用encode方法。
　　在python3中bytes与str是绝对不会等价的，即使字符内容为""，因此在传入字符序列时必须注意其类型。
#### python2的str与unicode
　　str表示字符的原始8位值，unicode表示Unicode字符。
　　在python2中，如果str只包含7位ASCII字符（英文字符），那么unicode与str实例类似于同一种类型（等价的），那么在这种情况下，以下几种操作是正常的：

* 可以用+号连接str与unicode
* 可以用=与!=来判断str与unicode
* 可以用’%s’来表示Unicode实例

### 系统以及源代码编码
3.x已经把源代码编码以及系统编码从ascii都变成了utf-8，避免了中文报错。
```bash
>>> import sys
>>> print(sys.getdefaultencoding())
utf-8
>>> print(sys.getfilesystemencoding())
utf-8
>>>
```
其次，我们可以看到我们定义的a为str（相当于2.x中unicode），而它在windows控制台输出时也没有因为编码问题而报错。
```bash
>>> a="你好"
>>>print(a)
你好
```

### 字符串编码
```bash
>>> a="你好"
>>> print(type(a))
<class 'str'>
>>> b=a.encode("utf-8")
>>> print(type(b))
<class 'bytes'>
>>>
```
我们可以看到，3.x中的str格式类似于2.x中的unicode，而2.x中的str相当于3.x中的bytes.

### 网页编码
![](/upload_image/20170418/1.png)
结果：
![](/upload_image/20170418/2.png)
返回的是bytes格式的，只要decode转化为str就ok了。

### 文件编码
![](/upload_image/20170418/3.png)
结果：从文件中读取出来的是str（2.x中的unicode），因此不用转码。
#### open函数
注意python2中open句柄是str(原始二进制)的，而python3中是str(unicode字符)，因此一下代码在python2中正常，在python3中会报错：
```bash
with open("test","w") as w:
    w.write("123")
```
因为python3中，要求传入的值为str类型，而不是bytes类型，open函数自带encoding方法。
解决方法：
```bash
with open("test","wb") as w:
    w.write("123")
```
同理，read函数也是一样，写成rb，就可以兼容2与3了。

### 传送门
[Python2编码之殇](http://thief.one/2017/02/16/%E8%A7%A3%E5%86%B3Python2-x%E7%BC%96%E7%A0%81%E4%B9%8B%E6%AE%87/)
[Python2编码之殇续集](http://thief.one/2017/04/14/1/)

