---
title: 利用Whatweb获取Web指纹信息
copyright: true
permalink: 1
top: 0
date: 2018-01-11 19:50:06
tags:
- whatweb
categories: 编程之道
password:
---
<blockquote class="blockquote-center">我都寂寞多久了还是没好
感觉全世界都在窃窃嘲笑</blockquote>

　　又是很久没有更新博客啦，为啥呢？因为在忙开发、开发、开发。我最近在研究指纹扫描以及漏洞扫描方面的设计与开发，从前端、后端到数据存储、消息队列再到分布式部署，感觉自己简直快成全栈了。不过开发过程中也有很多收获，有时间我会写博客分享一下。
<!--more-->
　　那么今天写点啥呢？就分享个很老的安全工具吧——whatweb，相信很多朋友应该知道，用来扫web指纹的。为啥会用到它，因为项目需要啊，其实也可以不用，因为我自己写了很多扫描指纹的插件，这个只是作为备案选择而已。但既然用到了，那就理所当然要为它打call。好了，照旧先介绍如何安装，再介绍如何使用，本文重点在于环境安装，以及如何在python代码中比较`优雅`的使用whatweb。

### 安装升级ruby
whatweb是用ruby开发的，因此服务器上需要安装ruby，且对版本有要求，貌似必须2.0以上（没记错的话）。目前很多服务器内置的ruby是1.8的，或者用yum install ruby安装的也是1.8的，因此需要安装或者升级版本到2.0以上才行。

#### 升级方案one（推荐）
先删除原来的ruby：
```bash
yum remove ruby ruby-devel
```
下载ruby安装包，并进行编译安装：
```bash
wget http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.2.tar.gz
tar xvfvz ruby-2.1.2.tar.gz
./configure
make
sudo make install
```
将ruby添加到环境变量，ruby安装在/usr/local/bin/目录下，因此编辑 ~/.bash_profile文件，添加一下内容：
```bash
PATH=$PATH:/usr/local/bin/
```
不要忘了生效一下：
```bash
source ~/.bash_profile
```
参考：http://ask.xmodulo.com/upgrade-ruby-centos.html

#### 升级方案two
先安装rvm，这是ruby的包管理器:
```bash
$ curl -L get.rvm.io | bash -s stable  
$ source ~/.bash_profile
```
测试是否安装成功:
```bash
rvm -v
```
利用rvm升级ruby:
```bash 
ruby -v  #查看当前ruby版本  
rvm list known  #列出已知的ruby版本
rvm install 2.0 #安装ruby 2.0
```

### 安装whatweb
说起来这个就很简单，直接去github上clone下项目：
```bash
git clone https://github.com/urbanadventurer/WhatWeb.git
```
项目内已经有编译好的可执行文件，whatweb，只需要添加个环境变量：
```bash
PATH=$PATH:/root/WhatWeb-master/
```

### 使用whatweb
具体详细的使用方式就要参考[github](https://github.com/urbanadventurer/WhatWeb)了，我这边只介绍怎么在python中使用whatweb。

废话不多说，直接上代码：
```bash
#! -*- coding:utf-8 -*-

import commands
import re

# 正则表达式
p_httpserver=re.compile(r"HTTPServer\x1b\[0m\[\x1b\[1m\x1b\[36m([^,]+?)\x1b\[0m\]")
p_title=re.compile(r"Title\x1b\[0m\[\x1b\[1m\x1b\[33m(.+?)\x1b\[0m\]")
p_ip=re.compile(r"IP\x1b\[0m\[\x1b\[37m([^,]+?)\x1b\[0m\]")
p_country=re.compile(r"Country\x1b\[0m\[\x1b\[37m([^,]+?)\x1b\[0m\]")
p_cookies=re.compile(r"Cookies\x1b\[0m\[\x1b\[37m([^,]+?)\x1b\[0m\]")
p_x_powered_by=re.compile(r"X-Powered-By\x1b\[0m\[\x1b\[37m([^,]+?)\x1b\[0m\]")

def re_grep(p,content):
  # 正则处理
  L=p.findall(content)
  if len(L)>0:
    return L[0]
  else:
    return ""

def whatweb(url):
    # whatweb扫描
    result=""
    httpserver=""
    title=""
    ip=""
    cookies=""
    country=""
    power_by=""

    try:
        status,result=commands.getstatusoutput('whatweb '+url)
        # print status,result
    except IndexError,e:
        print e
    else:   
        httpserver=re_grep(p_httpserver,result)
        title=re_grep(p_title,result)
        ip=re_grep(p_ip,result)
        country=re_grep(p_country,result)
        cookies=re_grep(p_cookies,result)
        power_by=re_grep(p_x_powered_by,result)

    return httpserver,title,cookies,country,power_by


if __name__=="__main__":

    result=whatweb("thief.one")
    for i in result:
        print i

```
说明：解释一下代码，主要就是一个正则表达式，因为运行whatweb会直接将结果打印，当然也有其他命令可以让其结果输出到文本等，但如果想要批量自动化扫描的话，需要实时获取whatweb的内容，生成文件的方式显然不行，因此我用了commands库，让python执行系统命令并获取返回结果，然后就是几个正则对结果的匹配。

结束之语：又水了一篇，嗯嗯！

`如果有朋友有更好地在python代码中使用whatweb的方法，麻烦告知，我是被whatweb的输出折腾的够呛，因此才选择了用正则，无奈之举。`
