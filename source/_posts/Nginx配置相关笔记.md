---
title: Nginx配置相关笔记
copyright: true
permalink: 1
top: 0
date: 2018-07-26 17:45:34
tags:
- nginx
categories: 技术研究
password:
---
<blockquote class="blockquote-center">好久没更，来水一篇～！～</blockquote>
　　就在刚刚，我花了四百大洋租了台腾讯云香港的服务器（～心在滴血～），因此我的博客终于可以宣告回国了。PS：之前一直使用github-page，众所周知速度贼慢，后面换成了新加坡的VPS服务器，速度就更慢了，没办法只能花大价钱买国内的云服务器。博客迁移得过程比较简单，无非就是添加nginx解析，因此本篇有点水，主要为了记录一下nginx配置web服务的一些笔记。
<!-- more -->

### http 301 https
我的博客使用了腾讯云免费签发的证书，因此可以使用https访问，默认情况下http也是可以访问的，那么如何将http请求301重定向到https，便是第一个要解决的问题。
编辑/etc/nginx/nginx.conf文件：
```bash
......
server {
       listen         80;
       server_name    thief.one;
       return         301 https://$server_name$request_uri;
}

server {
    listen 443;
    server_name thief.one;
    ......
}
......
```
创建一个80端口，一个443端口的web服务，并且将80端口的服务重定向到*https://....*。重启nginx后，访问*http://thief.one*会被301重定向到*https://thief.one*


### 禁止访问某些目录文件
由于我的博客项目存放在git上，因此服务器web目录内含有.git目录，也算是敏感信息泄露（当然都是一些静态的网页，其实也没有什么危害），那么如何在nginx中配置访问.git目录403是要解决的第二个问题。
编辑/etc/nginx/nginx.conf文件：
```bash
server {
    listen 443;
    server_name thief.one;
    ......

    location /.git/ {
            deny    all;
    }
}
```
添加一个location，禁止访问某目录。重启nginx后，尝试访问*https://thief.one/.git/config* 返回403

### 负载均衡
这个之前总结过：https://thief.one/2017/08/22/1/

### 只能通过域名访问
如果博客不想通过IP被访问到，需要在nginx上配置禁止ip访问，或者访问ip跳转到域名。
编辑/etc/nginx/nginx.conf文件：
```bash
server {
        listen       80 default_server;
        listen       443 default_server;
        return 403
}
```
重启nginx，访问：*http://150.109.106.49/* 返回403。


### 权限问题
首先说明一下，一般我不推荐使用root权限启动nginx服务。但如果nginx服务是用root权限安装的，且网站放在root目录下，启动nginx解析网站会有权限问题（因为配置文件中默认不是用root权限启动），因此需要更改配置文件为：
```bash
user root;
```
更安全的方法是用普通用户权限安装nginx，并将web目录移到普通用户目录下，用普通用户权限启动nginx服务。


*nginx配置相关问题笔记，之后我都会记录在此篇中*








