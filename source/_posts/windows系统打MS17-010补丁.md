---
title: windows系统打MS17-010补丁
date: 2017-05-15 19:45:31
comments: true
tags:
- ms17-010
- windows补丁
categories: 系统安全
permalink: 01
---
<blockquote class="blockquote-center">你转身的一瞬，我萧条的一生</blockquote>
　　周一大早全民开始打补丁，由此可见此次蠕虫病毒影响空前绝后。而我在给自己电脑打补丁的时候，发现了一些问题，在此分享以帮助还未及时打补丁的朋友。
<!--more -->

### 传送门
需要关闭445端口的朋友可以参考教程:　[windows关闭445端口](http://thief.one/2017/05/13/2)

### 微软漏洞信息官网挂了？
　　今早我在访问　[微软漏洞信息官方网站](https://technet.microsoft.com/en-us/library/security/MS17-010)　准备下载补丁时，发现其网站出现502错误，不知道是不是由于访问量太高的缘由。我猜想此时微软高层的心情肯定是苦笑不得，从来没有被民众重视过的微软补丁在今日达到了一个下载高潮。由于官方渠道下载受阻，很多人无法得到补丁文件，从而没能顺利得安装好补丁，在此我给出网盘链接，里面是各个操作系统对应的补丁程序。

百度网盘链接：http://pan.baidu.com/s/1slfitD7 密码：dkoe

说明：网盘内每个操作系统对应一个压缩包，请下载后自行解压安装即可，如失效请留言告知！

### 开启windows自动更新就ok了？
　　起初我在处理ms17-010补丁的时候，是选择开启windows自动更新功能，并且安装了最新的一些补丁。然而当我安装完后进行查看时，并没有发现KB4012212(windows7)补丁信息。无奈，只能自行下载ms17-010补丁安装包进行单独安装，安装完以后可以看到已安装的补丁中存在了KB4012212，所以我猜想自动更新是不包含ms17-010漏洞补丁的。

#### 如何查看已安装补丁信息？
查看已安装的补丁信息(cmd下输入以下命令)：
```bash
systeminfo > systeminfo.txt
```
打开生成的systeminfo.txt文件查看，里面包含了已安装补丁的KB编号信息。
![](/upload_image/2017051501/1.png)

### ms17-010对应的KB编号
各版本操作系统对应的KB号：
* windows Vista （KB4012598）
* windows xp（KB4012598）
* Windows Server 2008（KB4012598）
* Windows 7（KB4012212、KB4012215）
* Windows Server 2008 R2（KB4012212、KB4012215）
* Windows 8.1（KB4012213、KB4012216）
* Windows Server 2012 and Windows Server 2012 R2（KB4012213、KB4012214、KB4012216、KB4012217）
* Windows RT 8.1（KB4012216）
* Windows 10（KB4012216、KB4013198）
* Windows Server 2016（KB4013198）

安装完补丁后，请查看校验系统是否存在对应的KB号。

### MS对应的KB号
请移步项目：https://github.com/tengzhangchao/microsoftSpider


>转载请说明出处：[windows系统打MS17-010补丁|nMask'Blog](http://thief.one/2017/05/15/1)
本文地址：http://thief.one/2017/05/15/1