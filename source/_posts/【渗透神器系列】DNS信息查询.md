---
title: 【渗透神器系列】DNS信息查询
copyright: true
permalink: 1
top: 0
date: 2017-07-12 16:29:12
tags:
- 渗透神器
- DNS
categories: 安全工具
password:
---
<blockquote class="blockquote-center">Never put off what you can do today until tomorrow
今日事今日毕</blockquote>
　　好久没有写文章啦，最近忙着换工作，搞事情，麻烦事一大推，凑空整理一篇DNS信息查询等工具用法吧。DNS查询在渗透或者运维工作经常遇到，尤其是内部有DNS服务器的公司，需要定时监测DNS解析的是否正常，有无被DNS劫持的情况。因此，学会一些工具快速查询检测DNS服务器状况显得尤为重要，本篇就介绍几款常见的DNS信息查询工具。
<!-- more -->
### nslookup
　　nslookup是用来监测网络中DNS服务器是否可以实现域名解析的工具，简单来说可以获取域名对应的ip。与ping的区别在于，nslookup返回的结果更丰富，而且主要针对dns服务器的排错，收集dns服务器的信息。（其实ping的过程也去请求了dns的记录，然后对ip发送icmp数据包）
#### Usage

##### 非交互式（直接在shell中输入查询）：
查询thief.one域名对应的ip，这里指定了前往114.114.114.114－dns服务器进行查询。
```bash
nslookup thief.one 114.114.114.114
```
![](/upload_image/20170712/3.png)
查询thief.one域名DNS服务商。
```bash
nslookup -type=ns thief.one
```
![](/upload_image/20170712/1.png)
查询thief.one的邮件服务器。
```bash
nslookup -type=mx thief.one
```
![](/upload_image/20170712/2.png)

##### 交互式（先输入nslookup，然后再输入命令）：
```bash
nslookup
>
```
进入交互式界面，输入查询命令
```bash
>set type=a              #设置更改要查询的dns解析类型
>thief.one               #输入要查询的域名
>set type=mx             #设置更改要查询的dns解析类型
>thief.one
>server 114.114.114.114  #设置更改要查询的dns服务器地址
>ls thief.one #ls命令列出某个域中的所有域名
```
可以更改的type类型：
```bash
-A    #A记录
-AAAA
-CNAME #CNAME纪录
-HINFO
-MB
-MG
-MR
-MX #电子邮件交换记录，记录一个邮件域名对应的IP地址
-NS #域名服务器记录,记录该域名由哪台域名服务器解析
-PTR #反向记录,也即从IP地址到域名的一条记录
-TXT #记录域名的相关文本信息
```
### host
与nslookup类似，也是查询域名对应的dns信息。
#### Usage
```bash
host -t A thief.one
```
#### 参数
* -a：显示详细的DNS信息； 
* -c<类型>：指定查询类型，默认值为“IN“； 
* -C：查询指定主机的完整的SOA记录； 
* -r：在查询域名时，不使用递归的查询方式； 
* -t<类型>：指定查询的域名信息类型； 
* -v：显示指令执行的详细信息； 
* -w：如果域名服务器没有给出应答信息，则总是等待，直到域名服务器给出应答； 
* -W<时间>：指定域名查询的最长时间，如果在指定时间内域名服务器没有给出应答信息，则退出指令； 
* -4：使用IPv4； host 
* -6：使用IPv6.

### dig
#### Usage
```bash
dig thief.one mx
dig thief.one ns
dig @202.106.0.20 thief.one a  指定dns服务器
dig thief.one a +tcp  设置为tcp协议，默认为udp
dig thief.one a +trace 这个参数之后将显示从根域逐级查询的过程
```
若*http://thief.one*的DNS服务器为10.0.0.1，且存在域传送漏洞，则使用dig @10.0.0.1 http://thief.one axfr即可查看所有域名了。

#### 参数
* @<服务器地址>：指定进行域名解析的域名服务器； 
* -b：当主机具有多个IP地址，指定使用本机的哪个IP地址向域名服务器发送域名查询请求；
* -f<文件名称>：指定dig以批处理的方式运行，指定的文件中保存着需要批处理查询的DNS任务信息； 
* -P：指定域名服务器所使用端口号； 
* -t<类型>：指定要查询的DNS数据类型； 
* -x：执行逆向域名查询； 
* -4：使用IPv4； 
* -6：使用IPv6； 
* -h：显示指令帮助信息。

### whois
whois用来查询域名相关信息，比如注册人信息，电子邮件，域名提供商，ip信息等等。
#### Usage
```bash
whois -p port thief.one
```
更多用法可以使用*man whois*查看。

### 传送门
[【渗透神器系列】nc](http://thief.one/2017/04/10/1/)
[【渗透神器系列】nmap](http://thief.one/2017/05/02/1/)
[【渗透神器系列】Fiddler](http://thief.one/2017/04/27/1)
[【渗透神器系列】搜索引擎](http://thief.one/2017/05/19/1)
[【渗透神器系列】WireShark](http://thief.one/2017/02/09/WireShark%E8%BF%87%E6%BB%A4%E8%A7%84%E5%88%99/)

DNS信息在线查询的网站很多，可以参考下：[SecWeb安全导航](https://thief.one/SecWeb)另外网上类似的文章很多很多啦，大家可以全去搜索下，这里只是列举了一些常见的工具，若有好的后面会持续补充。