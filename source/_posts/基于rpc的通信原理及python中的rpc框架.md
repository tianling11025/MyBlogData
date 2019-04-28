---
title: 基于rpc通信的原理及python中的rpc框架
copyright: true
permalink: 1
top: 0
date: 2018-10-22 16:08:53
tags:
- python
- rpc
categories: 编程之道
password:
---
<blockquote class="blockquote-center">这场名叫人生的旅途，有太多风景不及回顾</blockquote>
　　最近在逛知乎的时候无意中看到了一则技术贴，讨论的主题大概是："Web开发中，使用RPC还是RESTFUL更好？"（其实是很老的话题了）。由于本人之前在web开发中只使用过restful，因此对这个问题的答案本身并不清楚，于是便抱着学习的态度查阅了一番资料，事后觉得有必要在此记录一番。
<!-- more -->

### 概念
　　REST表示的是描述性状态传递（representational state transfer），REST整个就是关于 客户端和服务端之间的关系的，其中服务端要提供格式简单的描述性数据，常用的是JSON和XML。
　　RPC指的是远程过程调用(remote procedure call)，本质上在JavaScript、PHP、Python等中调用都是一样的：取方法名，传参数。因为不是每个人都喜欢XML，RPC-API可以使用 JSON-RPC协议，也可以考虑自定义基于JSON的API，像Slack是用它的Web-API实现的。

### 区别与类同
　　基于RPC的API适用于动作（过程、命令等）；基于REST的API适用于领域模型（资源或实体），基于数据的CRUD (create, read, update, delete)操作。
　　接口调用通常包含两个部分，序列化和通信协议。常见的序列化协议包括json、xml、hession、protobuf、thrift、text、bytes等；通信比较流行的是http、soap、websockect，RPC通常基于TCP实现。那么restful使用的序列化协议通常是json，通信协议是http；rpc是一种通信协议，因此如果序列化使用json的话，那么就是json-rpc。

### 大牛们的见解
　　大牛1：restful首先是要求必须把所有的应用定义成为“resource”，然后只能针对资源做有限的四种操作。然而所有的接口，服务器端原本就存在有相应的函数，它们本来就有自身的命名空间，接受的参数、返回值、异常等等。只需要采用轻便的方式暴露出来即可，无需把一堆函数重新归纳到“资源”，再削减脑袋把所有的操作都映射为“增删改查”。
　　大牛2：RPC的思想是把本地函数映射到API，也就是说一个API对应的是一个function，我本地有一个getAllUsers，远程也能通过某种约定的协议来调用这个getAllUsers。RPC中的主体都是动作，是个动词，表示我要做什么。而REST则不然，它的URL主体是资源，是个名词。
　　大牛3：http相对更规范、标准、通用，无论哪种语言都支持http协议。RPC协议性能要高的多，例如Protobuf、Thrift、Kyro等。对外开放给全世界的API推荐采用RESTful，是否严格按照规范是一个要权衡的问题。要综合成本、稳定性、易用性、业务场景等等多种因素。内部调用推荐采用RPC方式。当然不能一概而论，还要看具体的业务场景。

以上答案来源：
https://blog.csdn.net/douliw/article/details/52592188 
https://www.zhihu.com/question/28570307

### 个人见解
接下来谈谈个人见解～！～，好吧，目前我没啥见解，先让我自己动手用用看rpc协议再说。

### python的rdc协议框架-zerorpc
　　Zerorpc是一个基于ZeroMQ和MessagePack开发的远程过程调用协议（RPC）实现。和 Zerorpc 一起使用的 Service API 被称为 zeroservice。Zerorpc 可以通过编程或命令行方式调用。
官方demo.py如下：
```bash
import zerorpc
class Cooler(object):
    """ Various convenience methods to make things cooler. """
    def add_man(self, sentence):
        """ End a sentence with ", man!" to make it sound cooler, and
        return the result. """
        return sentence + ", man!"
    def add_42(self, n):
        """ Add 42 to an integer argument to make it cooler, and return the
        result. """
        return n + 42
    def boat(self, sentence):
        """ Replace a sentence with "I'm on a boat!", and return that,
        because it's cooler. """
        return "I'm on a boat!"
s = zerorpc.Server(Cooler())
s.bind("tcp://0.0.0.0:4242")
s.run()
```
运行以上代码：
```bash
$ zerorpc -j tcp://localhost:4242 add_42 1
43
```
分析一下：从demo来看，就是远程通过rpc协议（tcp）进行了函数调用！！！这个操作还是有点666的，因为使用restful只能对资源或者说数据进行操作，而rpc协议直接对函数进行操作，且代码简单。

参考一下github：https://github.com/dotcloud/zerorpc-python

### 个人见解
　　简单说下个人理解，个人认为rpc与restful本身定位方向是有所不同的，restful偏向资源或者说数据的通信，注重接口的规范性，总之更加通用；rpc协议用于服务功能的调用，具体说就是函数的调用，可以适合更复杂通信需求的场景。因此以上有个大牛的说法我还是比较认同的，对内可以选择使用rpc，因为性能优势等原因，而对外使用resutful，因为通用。

