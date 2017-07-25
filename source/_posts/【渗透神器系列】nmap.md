---
title: 【渗透神器系列】nmap
date: 2017-05-02 14:55:27
comments: true
tags:
- 渗透神器
- nmap
categories: 安全工具
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">这个世界好比一座大熔炉，烧炼出一批又一批品质不同而且和原先的品质也不相同的灵魂</blockquote>
　　本篇作为渗透神器系列第三篇，将介绍一款经典的端口扫描工具--nmap。目前市面上成熟的端口扫描器有很多，比如massscan(全网扫描器)，zenmap(nmap的GUI版)等，但我个人还是钟爱nmap，原因很简单，因为它很强大，并且支持扩展。Nmap最新几个版本中，加入了nmap script Engine(NSE)功能，支持扩展脚本，即可以在nmap中加载自定义的nse脚本，以达到扫描的目的。目前官方的nse脚本已达500多个，nse脚本地址[https://nmap.org/nsedoc/](https://nmap.org/nsedoc/)，或者查看[github库](https://github.com/nmap/nmap)。
　　本篇将会介绍如何编写以及使用nse脚本，以便能最大程度地发挥出nmap的强大功能（扩展功能），当然本文后本段也会简单介绍下nmap工具的基本使用方法以及参数设置。
<!--more -->
### NSE
　　nse全称是*nmap脚本引擎*，脚本后缀名为.nse，脚本用Lua语言编写，遵循特定的规则。nse脚本存放在nmap安装目录下的scripts目录下，目前官方提供的大概有500多个，功能涵盖了常用的漏洞检测、端口检测、基线检测等。
#### nse script exploit
在scripts目录下新建一个文件，如：hello.nse，写入以下内容：
```bash
-- The Head Section --
-- The Rule Section --
portrule = function(host, port)
return port.protocol == "tcp" and port.number == 80 and port.state == "open"
end
-- The Action Section --
action = function(host, port)
return "Hello world"
end
```
以上代码运行后，会检测目标ip是否开放了80端口，若开放则返回helloworld。
nse脚本遵循nmap api规范，其包含三部分内容，其中--开头的行为注释内容。
##### The Head Section
该部分包含一些元数据，主要描述脚本的功能，作者，影响力，类别及其他。
##### The Rule Section
该部分定义脚本的一些规则，至少包含下面列表中的一个函数：
* portrule
* hostrule
* prerule
* postrule

##### The Action Section
该部分定义脚本逻辑，即满足条件后执行的内容，比如上面例子为输出helloworld。

#### 调用内置库
NSE脚本可以调用内置库，比如http库、shortport库、nmap库等。
导入方式：
```bash
local http = require "http"
local nmap = require "nmap"
local shortport = require "shortport"
```
更多nse-api参考：https://nmap.org/book/nse-api.html
更多lua语法参考：http://www.runoob.com/lua/lua-tutorial.html
#### nse script usage
当在scripts下面编写完hello.nse脚本后，如何加载使用呢？
方法一：
```bash
nmap --script-updatedb 更新脚本库
nmap --script=hello    使用该脚本
```
方法二：
```bash
nmap --script=d:/..../hello.nse 绝对路径
```
其他参数：
```bash
-sC: 等价于–script=default，使用默认类别的脚本进行扫描 可更换其他类别
–script=<Lua scripts>: <Lua scripts>使用某个或某类脚本进行扫描，支持通配符描述
–script-args=<n1=v1,[n2=v2,...]>: 为脚本提供默认参数
–script-args-file=filename: 使用文件来为脚本提供参数
–script-trace: 显示脚本执行过程中发送与接收的数据
–script-updatedb: 更新脚本数据库
–script-help=<scripts>: 显示脚本的帮助信息，其中<scripts>部分可以逗号分隔的文件或脚本类别
```
#### nse example
对目标机器进行扫描,同时对smb的用户进行枚举。
```bash
nmap  --script=smb-enum-users  target_ip
```
对目标机器所开启的smb共享进行枚举。
```bash
nmap  --script=smb-enum-shares target_ip
```
对目标机器的用户名和密码进行暴力猜测。
```bash
nmap  --script=smb-brute target_ip
```
对目标机器测试心脏滴血漏洞。
```bash
nmap -sV --script=ssl-heartbleed target_ip
```
再举几个硬件设备的例子：
```bash
modbus-discover.nse （该脚本可以调用Modbus 43（2B功能码）功能码读取设备信息）
modbus-enum.nse （Modbus TCP设备枚举脚本）
s7-enumerate.nse （西门子S7 PLC设备发现脚本，可以枚举PLC的一些基本信息）
enip-enumerate.nse （可以读取EtherNet/IP设备的基本信息）
BACnet-discover-enumerate.nse （可以读取BACnet设备的基本信息）
iec-identify.nse （IEC104协议asdu address枚举脚本）
mms-identify.nse （IEC-61850-8-1协议信息枚举脚本）
```
### nmap introduce
以上内容为nmap nse扩展脚本的基础知识，其中涉及到nse脚本编写的语法规则等，本篇暂不做详细介绍，可参考官方文档。以下内容为nmap基础使用，包含命令行参数等内容。
#### nmap parameter
nmap参数：
```bash
nmap [Scan Type(s)] [Options] {target specification}

scan type(s) 用于指定扫描类型
options 用于指定选项
target specification 用于指定扫描目标

-s 指定扫描类型
如下：
-sP (ping扫描) *存活主机探测
-sS (TCP SYN扫描 隐身扫描)  *默认扫描方式
-sT (tcp 扫描) * syn 不能用时就tcp扫描
-sU （UDP 扫描）
-sA  （ACK扫描） *三次握手 用于探测出防火墙过滤端口 实际渗透中没多大用

-sV   （版本探测）
-A    操作系统探测
-O （启用操作系统检测）
-v    详细
选项说明
-P0  [指定端口] (无ping扫描)
-PU  [指定端口] (udp ping扫描)
-PS [指定端口] (TCP SYN ping 扫描)
-PA  [指定端口] (tcp ack ping扫描) 
-PI   使用真正的pingICMP echo请求来扫描目标主机是否正在运行

-iL 指定扫描主机列表
-iR 随机选择目标

--exclude 排除扫描目标
--excludefile 排除文件中目标列表

-n (不用域名解析)
-R (为所有目标解析域名)

-T  时间优化（每隔多久发一次包 ） -T5 最快 -T0 最慢
-F  快速扫描
-e  指定网络接口
-M 设置tcp扫描线程
```
#### nmap output
输出结果：
```bash
-oS  保存扫描结果输出
-oN  把扫描结果重定向到一个可读的文件logfilename中
-oM  每个结果一行输出
-oA  同上
--append-output 附在原来的结果前面
```
#### nmap status
nmap端口状态：
```bash
open（开放的）
closed（关闭的）
filtered（被过滤的）不确定开放还是关闭
unfiltered （未被过滤的）
openfiltered （开放或者被过滤的）
closedfiltered （关闭或者未被过滤的)
```
#### nmap常用命令
以下命令部分收集于网络，部分来自个人总结。
轻量级扫描：
```bash
nmap -sP 192.168.0.0/24   判断哪些主机存活
nmap -sT 192.168.0.3   开放了哪些端口
nmap -sS 192.168.0.127 开放了哪些端口（隐蔽扫描）
nmap -sU 192.168.0.127 开放了哪些端口（UDP）
nmap -sS -O  192.168.0.127 操作系统识别
nmap -sT -p 80 -oG – 192.168.1.* | grep open    列出开放了指定端口的主机列表
nmap -sV -p 80 thief.one  列出服务器类型(列出操作系统，开发端口，服务器类型,网站脚本类型等)
```
批量扫描：
```bash
nmap -sT -sV -O -P0 --open -n -oN result.txt -p80-89,8080-8099,8000-8009,7001-7009,9000-9099,21,443,873,2601,2604,3128,4440,6082,6379,8888,3389,9200,11211,27017,28017,389,8443,4848,8649,995,9440,9871,2222,2082,3311,18100,9956,1433,3306,1900,49705,50030,7778,5432,7080,5900,50070,5000,5560,10000 -iL ip.txt
```
批量扫描：
```bash
nmap -sT -sV -p80-89,8080-8099,8000-8009,7001-7009,9000-9099,21,443,873,2601,2604,3128,4440,6082,6379,8888,3389,9200,11211,27017,28017,389,8443,4848,8649,995,9440,9871,2222,2082,3311,18100,9956,1433,3306,1900,49705,50030,7778,5432,7080,5900,50070,5000,5560,10000 --open --max-hostgroup 10 --max-parallelism 10 --max-rtt-timeout 1000ms --host-timeout 800s --max-scan-delay 2000ms -iL ~/Desktop/ip.txt -oN ~/Desktop/result/result.txt
```
### nmap api
nmap支持很多语言的扩展，本文简单介绍下python中如何使用nmap。
#### python-nmap
安装：pip install python-nmap
作用：利用python调用nmap接口，实现端口扫描。
使用：
```bash
>>> import nmap
>>> nm = nmap.PortScanner()
>>> nm.scan('127.0.0.1', '22-443')
>>> nm.command_line()
```
更多使用方法，参考：http://xael.org/pages/python-nmap-en.html

### 传送门
[【渗透神器系列】DNS信息查询](http://thief.one/2017/07/12/1/)
[【渗透神器系列】nc](http://thief.one/2017/04/10/1/)
[【渗透神器系列】Fiddler](http://thief.one/2017/04/27/1)
[【渗透神器系列】搜索引擎](http://thief.one/2017/05/19/1)
[【渗透神器系列】WireShark](http://thief.one/2017/02/09/WireShark%E8%BF%87%E6%BB%A4%E8%A7%84%E5%88%99/)
