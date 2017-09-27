---
title: justniffer抓取流量大法
copyright: true
permalink: 1
top: 0
date: 2017-09-27 11:26:04
tags:
- justniffer
categories: 安全工具
password:
---
<blockquote class="blockquote-center">Understand yourself in order to better understanding others
知己方能解人</blockquote>
　　本篇简单介绍一款流量抓取神器---justniffer，其能在线抓取流量也能离线分析数据包。justniffer与网络抓包神器wireshark相比，用法更为简单且对网络影响较小。面对海量的流量，我们需要经常从中分析出恶意请求，从而去做好防御，因此我在此记录justniffer的一些基础用法，以做备份查阅。
<!--more-->
### Install
```bash
sudo add-apt-repository ppa:oreste-notelli/ppa 
sudo apt-get update
sudo apt-get install justniffer
```

### Usage
#### 基础命令
```bash
justniffer -i eth5 -u -l "%request.header.host  %request.method %request.url  %response.grep(\r\n\r\n(.*)) %request.grep(\r\n\r\n(.*))"
```
#### 重点参数
* -i 指定监听的端口
* -l 指定日志输出格式
* -u 将不可打印的字符解析为.

#### 日志格式
* %request.header.host #请求头中的HOST
* %request.method #请求类型
* %request.url #请求URL
* %request.grep(\r\n\r\n(.*)) #请求数据包
* %response.grep(\r\n\r\n(.*)) #response的数据包

### 后期处理
一般来说我们在抓取流量后，需要先保存在本地然后再进行规则的分析。然而如何保存，保存后该怎么提取关键内容呢？这里提供一个小小的方法。

#### 抓取流量存入文件
可以使用如下命令抓取指定几个参数的流量内容，并存入到文件：
```bash
justniffer -i eth5 -u -l "%request.header.host NMASKnmask %request.method NMASKnmask %request.url NMASKnmask %response.grep(\r\n\r\n(.*)) NMASKnmask %request.grep(\r\n\r\n(.*))" | awk -F nmask '$1 !~ /^-/ && $2 ~ /(GET|POST).*/ {print$2,$1,$3,$4,$5}'  >> /log/20170927.log 2>&1 
```
说明：该命令获取了流量的host、method、url、response_body、request_body内容(注意：这里只筛选了GET、POST的请求)，然后将其存入了/log/20170927.log文件中。我们可以运行此命令一段时间，比如1个小时，当结束进程后我们便收集了一个小时的流量信息。

#### 处理日志文件
打开/log/20170927.log文件，我们看到的每一行的内容格式如下：
```bash
GET NMASK www.baidu.com NMASK /test.html NMASK response_body={"result":"123"} NMASK request_body={"get":"123"}
```
说明：每一行文件内容都包含一份流量信息，流量信息分为五个内容，每个内容间用NMASK（特殊字符串，可自定义）隔开。然后我们便可以写python脚本，遍历日志文件，并用split("NMASK")获取每一个流量信息了。


更多的配置信息、命令参数，可参考：http://www.jianshu.com/p/02021de8f82e
