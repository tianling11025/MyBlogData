---
title: nginx负载均衡
copyright: true
permalink: 1
top: 0
date: 2017-08-22 14:08:36
tags:
- linux
categories: 技术研究
password:
---
<blockquote class="blockquote-center">Give more than you planned to
多多给予，不必计较</blockquote>
　　nginx功能强大且常用作反向代理或者负载均衡，当我们部署了一个web系统之后，面对日益增多的访问流量，采用nginx做负载均衡是一个实惠的方案，本文用来记录nginx实现负载均衡的一些操作。
<!-- more -->
### 实验环境
　　为了能够更符合真实环境，我在本机host上绑定了一个域名phantomjs.me，其ip地址为192.168.1.2，是一台安装了nginx的linux服务器，用来模拟负载均衡服务器；另外同一内网中还有3台web服务器，其ip分别是192.168.1.3，192.168.1.4，192.168.1.5。

### 实验目的　　
　　当我们访问phantomjs.me域名时，负载均衡服务器能够将流量负载到3台web服务器中，负载的方式可以自由选择。

### 方案设计
* （A）192.168.1.2负载均衡服务器监听80端口，用作负载。
* （B）192.168.1.3Web服务器监听80端口。
* （C）192.168.1.4Web服务器监听80端口。
* （D）192.168.1.5Web服务器监听80端口。

说明：A服务器作为负载均衡服务器，域名直接解析到A服务器（192.168.1.2:80）上。由A服务器将流量负载均衡到B服务器（192.168.1.3:80）、C服务器（192.168.1.4:80）和D服务器（192.168.1.5:80）上。负载均衡可以针对不同的服务器，也可以针对同一台服务器的不同端口，主要看实际需求。


### nginx具体配置
　　编辑A服务器的nginx.conf，文件位置在nginx安装目录下，一般在/etc/nginx/nginx.conf。在http段加入以下代码：
```bash
upstream phantoms.me{ # 要与server_name的名字一致
      server 192.168.1.3:80; #分别对应三台web服务器
      server 192.168.1.4:80;
      server 192.168.1.5:80;
}

server{ 
    listen 80; #nginx开启的端口
    server_name phantoms.me; #测试域名
    location / { 
        proxy_pass         http://phantomjs.me; 
        proxy_set_header   Host             $host; 
        proxy_set_header   X-Real-IP        $remote_addr; 
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for; 
    } 
    access_log /var/log/nginx.log;  #添加日志记录
}
```
重启nginx
```bash
/etc/init.d/nginx restart
```
最后访问http://phantomjs.me

#### server中可用的参数
默认upstream server后的参数 weight=1 max_fails=1 fail_timeout=10s。

* weight：服务器权重
* max_fails=number:最大失败尝试次数
* fail_timeout=time:设置服务器不可用的时长
* backup：备用主机
* down：手动标记不再处理任何用户请求

### nginx反向代理
这里顺便记录一下，用nginx配置反向代理的方法，这种方法也被大量用在网页劫持（黑产）中，这里不详细介绍了。
#### 配置
将以下内容添加到nginx配置文件的server中：
```bash
location /update/{#将本地update目录代理到baidu.com/update目录下，即访问本地update其实是在访问baidu的update。
        proxy_pass         http://baidu.com/update; 
}
```
重启nginx，尝试访问*http://phantomjs.me/update/*，其实际获取的是baidu的update目录资源。

关于nginx负载均衡更详细的内容，可以访问：http://www.jusene.me/2017/05/24/nginx-proxy/

### 参考文章
http://www.jianshu.com/p/ac8956f79206