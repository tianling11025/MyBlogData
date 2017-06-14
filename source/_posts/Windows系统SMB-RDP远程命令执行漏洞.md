---
title: Windows系统SMB/RDP远程命令执行漏洞
date: 2017-04-15 14:22:36
comments: true
tags: 
- 系统漏洞
- windows
categories: 系统安全
password:
copyright: true
---
<blockquote class="blockquote-center">黑客无所不能</blockquote>

　　介于此次爆发的漏洞事件危害太过严重，本文当回搬运工，分享此次NSA方程式组织泄露的0day事件。由于信息量太过庞大，没有对其中的技术细节进行研究，不过请相信我，赶紧拔电源吧。
<!--more -->
事件具体细节请参考：[长亭科技专栏](https://zhuanlan.zhihu.com/p/26375989)
exploit地址：https://github.com/x0rz/EQGRP_Lost_in_Translation

### 事件起因
　　2016 年 8 月有一个 “Shadow Brokers” 的黑客组织号称入侵了方程式组织窃取了大量机密文件，并将部分文件公开到了互联网上，方程式（Equation Group）据称是 NSA（美国国家安全局）下属的黑客组织，有着极高的技术手段。这部分被公开的文件包括不少隐蔽的地下的黑客工具。另外 “Shadow Brokers” 还保留了部分文件，打算以公开拍卖的形式出售给出价最高的竞价者，“Shadow Brokers” 预期的价格是 100 万比特币（价值接近5亿美金）。这一切听起来难以置信，以至于当时有不少安全专家对此事件保持怀疑态度，“Shadow Brokers” 的拍卖也因此一直没有成功。
　　北京时间 2017 年 4 月 14 日晚，“Shadow Brokers” 终于忍不住了，在推特上放出了他们当时保留的部分文件，解压密码是 “Reeeeeeeeeeeeeee”。
　　这次的文件有三个目录，分别为“Windows”、“Swift” 和 “OddJob”，包含一堆令人震撼的黑客工具（我们挑几个重要的列举如下）：

* EXPLODINGCAN 是 IIS 6.0 远程漏洞利用工具
* ETERNALROMANCE 是 SMB1 的重量级利用，可以攻击开放了 445 端口的 Windows XP, 2003, Vista, 7, Windows 8, 2008, 2008 R2 并提升至系统权限。
* 除此之外 ERRATICGOPHER 、ETERNALBLUE 、ETERNALSYNERGY 、ETERNALCHAMPION 、EDUCATEDSCHOLAR、 EMERALDTHREAD 等都是 SMB 漏洞利用程序，可以攻击开放了 445 端口的 Windows 机器。
* ESTEEMAUDIT 是 RDP 服务的远程漏洞利用工具，可以攻击开放了3389 端口且开启了智能卡登陆的 Windows XP 和 Windows 2003 机器。
* FUZZBUNCH 是一个类似 MetaSploit 的漏洞利用平台。
* ODDJOB 是无法被杀毒软件检测的 Rootkit 利用工具。
* ECLIPSEDWING 是 Windows 服务器的远程漏洞利用工具。
* ESKIMOROLL 是 Kerberos 的漏洞利用攻击，可以攻击 Windows 2000/2003/2008/2008 R2 的域控制器。

### 漏洞影响

据说影响全球70%的windows服务器，想想都恐怖，不说了，我拔电源了。

### 漏洞对应的补丁
![](/upload_image/20170415/1.png)

### 临时修复方案

* 关闭445,137,139,3389端口，或者上防护设备限制特定ip访问。
* 坐等微软补丁