---
title: windows服务器信息收集工具
date: 2016-09-04 18:54:33
comments: true
tags: 信息收集工具
categories: 安全工具
---

　　在日常的安全服务工作中，经常会遇到需要收集目标服务器系统信息的需求，例如：系统日志，中间件日志，系统信息等。收集这些信息，有助于分析服务器安全状况，也有利于被入侵后的取证分析。然而客户网络环境往往很复杂，服务器较多，系统版本也不尽相同，给手工收集带来了很多麻烦，因此便研究开发了*服务器信息收集工具*。
<!-- more -->
## 功能介绍

* 收集系统日志
* 收集系统信息
	1. 开机时间
	2. IP_MAC地址
	3. 用户信息
	4. 操作系统版本
	5. 进程信息
	6. hosts文件
	7. 端口信息
* 收集中间件日志
	1. Apache
	2. IIS
	3. Tomcat
	4. JBOSS
* 全盘搜索日志文件

## 使用说明
程序帮助：
![](/upload_image/20160905/001.png)

1.运行程序，开始收集系统信息。
![](/upload_image/20160905/002.png)

2.程序运行期间，可以输入目标磁盘盘符，对该盘进行扫描，获取.log文件；如果不输入直接回车，默认为全盘扫描。
![](/upload_image/20160905/003.png)

3.运行完毕，会在当前目录下生成采集的日志以及系统信息文件夹。
![](/upload_image/20160905/004.png)


>注意：如果程序运行报错(MSVCR100.dll),请前往 [下载](https://github.com/tengzhangchao/Windows_Packages/raw/master/VC%2B%2B%20Redist/2010_vcredist_x64.exe) VC运行库进行安装,安装完成后再次运行程序即可。


## 工具下载

windows服务器信息收集工具 [下载地址](https://github.com/tengzhangchao/InForMation)

