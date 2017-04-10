---
title: PyShell 木马后门
date: 2016-09-05
comments: true
tags: 
- 木马后门
- pyshell
categories: 安全工具
---

　　在渗透测试过程中，经常会遇到一种状况：获取到了目标服务器的shell，需要进一步开展内网渗透，然而由于各种原因无法远程登录服务器，此时内网渗透往往很难开展。由此难点，我研发了一款具有针对性的后门程序，功能有点类似于NC(瑞士军刀)，但不局限于NC的功能，在此分享以表对NC的敬意。
<!-- more -->
### 使用方法
```bash
[HELP]  PyShell.exe [-listen(-slave)] [ip] [port]        #绿色免环境版
[HELP]  python PyShell.py [-listen(-slave)] [ip] [port]  
```
### 功能参数
```bash
[HELP]  exit    ----退出连接
[HELP]  kill    ----退出连接并自毁程序
[HELP]  playtask    ----创建计划任务
[HELP]  python -p file.py    ----在肉鸡上执行本地python脚本
```

### 实战演示

#### 环境准备

本机的IP地址为：10.0.3.119 
本机上装了一个虚拟机，IP地址为：192.168.67.130 

本机充当为目标服务器(被攻端),虚拟机充当为攻击机(攻击端)

#### 运行木马

首先在虚拟机上运行PyShell程序，监听一个未被使用的端口，如：2222

接着在本机上运行PyShell程序，连接虚拟机的这个端口
![](/upload_image/20160905_2/001.png)

可以看到，虚拟机上反弹了一个shell
![](/upload_image/20160905_2/002.png)

在虚拟机shell中查询ip地址，是本机的10网段
![](/upload_image/20160905_2/003.png)

在虚拟机shell中执行命令，使本机执行python脚本，进行内网端口扫描
![](/upload_image/20160905_2/004.png)

>提示：python脚本并未传到本机，而是通过数据包形式传递到了PyShell文件内执行，数据流量经过16进制+Base64加密，可以绕过防火墙

创建计划任务
![](/upload_image/20160905_2/005.png)

本机查看结果
![](/upload_image/20160905_2/006.png)


### 优缺点
* 程序对互相传输的数据进行了加密，以绕过防火墙。

* 当需要在肉鸡上执行python脚本时，不需要在肉鸡上上传相应的脚本文件，只需将本地脚本内容加密传输到肉鸡，并执行即可。

* 此程序在执行完命令以后，并不能时时回显结果，也就是说python脚本运行完以后才会返回输出，有待完善。


### 工具下载

PyShell 木马后门  [下载地址](https://github.com/tengzhangchao/PyShell/)


