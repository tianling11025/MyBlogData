---
title: WireShark过滤规则
date: 2017-02-09 11:02:14
comments: true
tags: wireshark
categories: 安全工具
---
　　wireshark是一款网络流量抓取分析神器，也是安全工具使用排行中排名第一的工具。使用wireshark必须要牢记一些常用的数据包过滤规则，对于寻找一些特定的包会事半功倍。

### IP过滤
ip源地址：　　ip.src　　　　ip.src==10.0.3.109
ip目的地址: 　　ip.dst　　　　ip.dst==10.0.3.114

### 端口过滤
tcp.port==80　　　　所有端口为80的包
tcp.dstport==80　　　目的端口为80的包
tcp.srcport==80　　　源端口为80的包

### 协议过滤
http
tcp
icmp
.......

### http模式过滤
http.request.method=="GET"　　查找GET包
http.request.method=="POST"　　查找POST包

### 连接符
and　　&
or　　||

### 自助模式
可以打开wireshark的Expression会弹出Filter Expression窗口：
![](/upload_image/20170209/1.png)
