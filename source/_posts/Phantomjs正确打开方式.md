---
title: Phantomjs正确打开方式
date: 2017-03-31 11:30:58
comments: true
tags: Phantomjs
categories: 编程之道
---
<blockquote class="blockquote-center">你是如何走出人生的阴霾的？
多走几步</blockquote>

　　前段时间分析了[Selenium+Phantomjs的使用方法以及性能优化问题](http://thief.one/2017/03/01/Phantomjs%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)，期间也分析了利用[Selenium+phantomjs爬虫爬过的一些坑问题](http://thief.one/2017/03/01/Phantomjs%E7%88%AC%E8%BF%87%E7%9A%84%E9%82%A3%E4%BA%9B%E5%9D%91/)。然而在使用phantomjs的过程中，并没有正真提升phantomjs的性能，爬虫性能也没有很好的提升。经过网友的提醒，发现其实是使用phantomjs的方法出了问题，因此无论怎么优化，都不能从根本上去提升性能。那么本篇就来好好说说，Phantomjs正确的打开方式。
<!--more -->
### 抛弃selenium+phantomjs
　　之前我一直使用selenium去使用phantomjs，原因是因为selenium封装了phantomjs一部分功能，selenium又提供了python的接口模块，在python语言中可以很好地去使用selenium，间接地就可以使用phantomjs。然而，我现在要说的是，是时候抛弃selenium+phantomjs了，原因之一此封装的接口很久没有更新了（没人维护了），原因之二selenium只实现了一部分phantomjs功能，且很不完善。

### phantomjs APi
　　通过查看phantomjs官方介绍，我们可以发现phantomjs的功能异常强大，绝不仅仅是selenium封装的功能那么简陋。phantomjs提供了很多种APi，具体可以查看：[phantomjs api介绍](http://thief.one/2017/03/13/Phantomjs-Api%E4%BB%8B%E7%BB%8D/)，其中最常用的要属Phantomjs WebService与Phantomjs WebPage，前者用于开启http服务，后者用于发起http请求。

### Phantomjs正确使用方式
正确打开方式应该使用phantomjs Webservice作为一种web服务的形式（api）,将其与其他语言分离开来（比如python）。

#### 设计流程：
　　Python通过http请求下发任务，Phantomjs Webservice获取任务后去处理，处理完以后再将结果返回给Python。任务调度、存储等复杂操作交给Python去做，Python可以写成异步并发去请求Phantomjs Webservice，需要注意的是目前一个Phantomjs Webservice只支持10个并发。但我们可以在一台服务器上多开几个phantomjs Webservice启用不同的端口即可，或者可以多台服务器做个集群，用nginx做反向代理。

#### Phantomjs Webservice
新建test.js，写入如下代码：
```bash
var webserver = require('webserver');
var server = webserver.create();
var service = server.listen(8080, function(request, response) {

  var postRaw=request.postRaw;
  var aaa=new Array();
  aaa=postRaw.split("=");
  var url="http://"+aaa[0];
  var md5_url=aaa[1];
  console.log(url); //输出传入的url

  //获取源码
  var webPage = require('webpage');
  var page = webPage.create();
  page.open(url, function (status) {
    var url = page.url;
    console.log('url: ' + url);  //输入获取到的目标网站title
  });

  // //页面截图
  // var webPage = require('webpage');
  // var page = webPage.create();
  // page.viewportSize = { width: 1920, height: 1080 };
  // page.open(url, function start(status) {
  //   page.render(md5_url+'.jpg', {format: 'jpg', quality: '100'});
  // });

  //response返回信息
  response.status=200;
  response.write(md5_url+'.jpg');
  response.close();
});
```
作用：处理http请求，获取url，进行截图或者获取源码操作。
使用：
```bash
phantomjs.exe test.js
```
会在本地开启web服务，端口为8080。

#### Python Client
新建http_request.py，写入如下代码：
```bash
#! -*- coding:utf-8 -*-

import requests
import md5
from multiprocessing.dummy import Process

domain_list=["thief.one"]*10

url="http://localhost:8080"

def http_request(domain):
    m1 = md5.new()
    m1.update(domain)
    md5_domain=m1.hexdigest()

    payload={domain:md5_domain}

    requests.post(url,data=payload)

if __name__=="__main__":
    for domain in domain_list:
        t=Process(target=http_request,args=(domain,))
        t.start()

```
作用：异步并发下发任务。

#### 运行截图
运行python以后，异步下发10个任务，Phantomjs服务器端接收到url并开始处理，并发处理10个任务并输入结果。
![](/upload_image/20170331/1.png)


>转载请说明出处:[Phantomjs正确打开方式 | nMask'Blog](http://thief.one/2017/03/31/Phantomjs正确打开方式/)
本文地址：http://thief.one/2017/03/31/Phantomjs正确打开方式/




