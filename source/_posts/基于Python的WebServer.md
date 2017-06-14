---
title: 基于Python的WebServer
date: 2016-09-14 15:12:39
comments: true
tags: 
- python运维脚本
categories: 安全工具
password:
copyright: true
---

　　WebServer的主要功能是用来运行代码，处理http请求等服务，比如常见的Apache，IIS，Nginx等都可以用来解析代码，处理请求。以上几种容器（中间件）功能强大，但是安装配置比较麻烦，对于像我这样的菜鸟来说，搭建一个web服务器可能要花几天时间。如果我们搭建web服务器并不是专门为了处理大规模的请求，而只是为了测试使用，那么一个方便速成的WebServer就至关重要了。
<!-- more -->
#### Python WebServer编程介绍

* BaseHTTPServer: 提供基本的Web服务和处理器类，分别是HTTPServer和BaseHTTPRequestHandler。
* SimpleHTTPServer: 包含执行GET和HEAD请求的SimpleHTTPRequestHandler类。
* CGIHTTPServer: 包含处理POST请求和执行CGIHTTPRequestHandler类

```bash
python -m SimpleHTTPServer 8000
```
python内置很多好用的库，此时打开浏览器，访问localhost:8000端口即可。

#### PyWebServer介绍

　　由于用python搭建一个简易的WebServer十分方便，因此我便写一个简单的启动器，类似于SimpleHTTPServer。为了方便没有安装python环境的windows机子启动，用pyinstaller工具将py程序打包成了exe可执行程序。

##### Linux下运行代码

```bash
python PyWebServer.py -h
python PyWebServer.py -i 10.0.0.1 -p 8888   ##指定ip与端口,默认为8888
```
##### windows下运行代码

```bash
PyWebServer.exe -h  
PyWebServer.exe -p 8888      ##指定端口,默认为8888
```
运行完以后,可以在其他机子上访问，进行文件下载等操作！

#### PyWebServer功能

功能可以自由想象发挥，比如说：
* 可以在服务器上运行程序，解析一段精心构造的py代码，远程执行系统命令。（如不在同一网段，需要转发端口）
* 可以在服务器上运行程序，用来替代FTP等工具，下载服务器上的文件（当服务器是linux时，使用比较方便）
......

#### 工具下载

PyWebServer 	[下载地址](https://github.com/tengzhangchao/PyWebServer)



