---
title: 安卓版Kali-linux
date: 2017-02-10 11:36:30
comments: true
tags: kali
categories: 技术交流
---
　　据说OPPO拍照神器最近很火，于是便凑热闹买了一款（R9s），外形不错，性能说得过去。尤其是自拍功能爱不释手（......），于是手头原本的小米便闲置了出来。作为一名崇尚节俭持家的技术男，当然是要废物利用一番，于是便有了以下的一番折腾。
　　我的目的是打造一款渗透测试专用手机，最先想到的方案是在手机上安装kali-linx系统，因为该系统集成了很多渗透测试工具，解决了很多依赖问题，省去不少麻烦。那么问题来了，怎么在手机上安装kali-linux系统呢？在查找了一些资料之后，我理了理思路：
（1）手机需要root
（2）手机上安装linux-deploy
（3）在linux-deploy上安装kali
（4）在kali里面安装渗透测试工具
思路有了，那么让我们撸起袖子干起来吧！(以下提到的安装包会在文章最后提供下载！)

### Root
　　起初看到网上的一些教程，介绍root手机非常简单，下载第三方软件，便可一键root。于是抱着轻松地态度在电脑上下载了一款软件（root精灵），接着将手机连上电脑，便开始点击一键root了。过了几分钟提示root成功，心想，原来破解手机这么简单，刚想吐槽小米，打开手机便发现根本没有root成功，NM坑爹。然后卸载了此软件，又重新找了一款（root大师），结果同样如此。
　　心中默默骂了几条街后，喝口水冷静了会，重新上网搜索资料，竟然无意看到了小米官方提供开发者版本的安装包（晕倒，所以不能盲目使用第三方软件，一般厂商会给出相应的软件或者安装包）。
　　官方下载地址：[http://www.miui.com/download-241.html](http://www.miui.com/download-241.html)
　　根据官方提供的教程安装即可（我选择了第二种安装方式），安装完以后在安全中心授予应用程序root权限，其他品牌的手机请自行百度，方法大同小异。

### 安装linux-deploy
　　Linux deploy是一个可以快速在Android设备上安装运行Linux操作系统的App,遵循GPLv3协议，运行需要root权限。linux-deploy软件介绍：[http://www.cnblogs.com/mzlw/p/4841707.html](http://www.cnblogs.com/mzlw/p/4841707.html)
在手机上安装完linux-deploy，运行后进行配置：
![](/upload_image/20170210/3.png)
运行界面如上图所示，点击右下角进行配置：
![](/upload_image/20170210/1.png)
发行版选择：kali-linux；源地址选择国内镜像：http://202.141.160.110/kali/
![](/upload_image/20170210/2.png)
勾选上ssh,vnc，在启动系统后会自动开启ssh以及vnc服务，方便远程管理。
配置完成后点击安装，等待一会。
![](/upload_image/20170210/4.png)
安装完以后点击启动，如若成功，便可以用ssh工具连接此系统。
![](/upload_image/20170210/6.png)

注：linux-deploy只是一款软件，安装它对应手机本身不会造成什么影响（除了占用存储空间），也不会清空数据（不是刷机）

linux-deploy安装kali参考：
[http://www.freebuf.com/articles/terminal/13209.html](http://www.freebuf.com/articles/terminal/13209.html)
[http://www.freebuf.com/articles/terminal/47817.html](http://www.freebuf.com/articles/terminal/47817.html)

### kali上安装渗透工具
　　虽然手机上安装kali成功了，但是此kali系统上并没有任何工具，需要自己安装。因为kali官方的源太慢了，因此建议更换国内的源。手机上安装一个ssh远程连接工具，连接上kali系统，并输入以下命令：
```bash
vim /etc/apt/sources.list
```
清空文件内容并添加以下内容：
```bash
deb http://202.141.160.110/kali/ kali-rolling main contrib non-free
deb-src http://202.141.160.110/kali kali-rolling main contrib non-free
```
更换完以后，更新源：
```bash
sudo su       #切换到root用户
apt-get update
apt-get upgrade
```
安装工具：
```bash
apt-get install nmap
apt-get install sqlmap
apt-get install metasploit-framework
......
```
运行截图：
![](/upload_image/20170210/5.png)
*运行速度还行，方便携带，居家旅行必备神器！*

### 其他安全工具
　　除了在安卓手机上安装kali系统以外，很多安全软件也支持安卓系统，比如dsploit、busybox、nmap for android等。首先在手机上安装busybox软件（授予root权限），运行软件以后勾选上智能安装选项，然后点击安装busybox。安装完busybox后，才可以使用dsploit等软件，当然这些软件也都是需要root权限的。至于这些安全软件的用法，网上一搜一大推，这里便不再介绍了。

### 软件工具下载
链接: [https://pan.baidu.com/s/1miqcGjQ](https://pan.baidu.com/s/1miqcGjQ)  密码: ch5f


<center>*有时候折腾仅仅只是为了折腾，仅此而已！*</center>