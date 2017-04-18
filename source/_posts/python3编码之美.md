---
title: python3编码之美
date: 2017-04-18 10:21:59
comments: true
tags: 
- python编码
categories: 编程之道
permalink: 01
---
<blockquote class="blockquote-center">终是谁使弦断，花落肩头，恍惚迷离</blockquote>
　　之前一直在使用python2.x版本，其中的编码问题颇为头疼，根据使用经验以及实验测试，前些日子总结了一些关于python2.x的编码问题，会在本文最后给出地址。本篇主要描述python3中的编码，如果称Python2的编码为殇，那么Python3的编码就应该为美了。
<!--more -->
　　我在python2编码之殇一文的最后介绍过，想要解决python2中的编码问题，最直接有效的方法就是将所有外部的字符串转变为unicode格式，再在python内部了流转。python3正是在这方面做了很大的优化。
　　python3中也有2种编码格式，分别为str与byte，这里的str相当于2中的unicode，byte相当于2中的str。再者python3将python源代码编码从ascii改成了utf-8，从外部接收的编码自动转化成了str(2中的unicode)，大大减少产生编码异常的点，光说没用，我用实验证明。

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

### 传送门
[Python2编码之殇](http://thief.one/2017/02/16/%E8%A7%A3%E5%86%B3Python2-x%E7%BC%96%E7%A0%81%E4%B9%8B%E6%AE%87/)
[Python2编码之殇续集](http://thief.one/2017/04/14/1/)

>转载请说明出处:[Python3编码之美|nMask'Blog](http://thief.one/2017/04/18/1/)
本文地址：http://thief.one/2017/04/18/1/
