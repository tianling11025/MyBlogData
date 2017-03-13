---
title: SearchWebPath
date: 2017-03-10 12:33:21
comments: true
tags: Web路径问题
categories: 安全工具
---
<blockquote class="blockquote-center">真的猛士，敢于直面惨淡的人生，敢于正视淋漓的鲜血。
—— 鲁迅</blockquote>

　　近日爆出的struts2-045漏洞可谓掀起了一波新的信息安全危机，基于该漏洞利用较为简单，适用范围广，因此受灾面积可想而知。然而在对某些站点进行安全检测时，难免会遇到一些问题，比如：如何写shell，如何提权等等。这里我针对如何寻找网站物理路径的问题，开发了一个小工具，可自动化的快速定位的网站物理路径，在此分享。
	<!--more -->
　　若需Struts2-045 POC或者检测工具，请前往：[Struts2-045漏洞](http://thief.one/2017/03/07/Struts2-045%E6%BC%8F%E6%B4%9E/)

　　免责申明：*本文不在于教唆如何利用struts2漏洞进行网站入侵，只用作技术探讨研究，本文涉及的工具请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负*

### 工具应用场景
利用某些特定漏洞，可远程执行命令，希望可以寻找到网站物理路径，写入一句话木马。

### 前提条件
* 网站URL是静态的，而不是动态随机生成（即url路径必须与磁盘目录结构一致）
* 服务器支持上传文件

### Function
根据网站URL，如：www.xxx.com/a/b/c?id=1，判断出URL所在的网站物理路径地址，如：c:/web/cms/a/b/c。

### Usage
#### python源码文件
```bash
python searchweburl.py -p "./" -u "http://www.xxx.com/a/b/c/d?id=1"
```
#### windows绿色版
```bash
searchweburl.exe -p "./" -u "http://www.xxx.com/a/b/c/d?id=1"
```
#### linux绿色版
```bash
./searchweburl -p "./" -u "http://www.xxx.com/a/b/c/d?id=1"
```
### Parameter

* -p --path　　　　待检测的磁盘路径
* -u --url　　　　 待检测的网站url
* -h --help　　　　帮助信息

### Example
针对于windows与linux操作系统，我分别搭建了2套网站，以便测试。
#### Windows
在一台windows服务器上搭建了一个简单的web服务,访问如下：
![](/upload_image/20170310/1.png)
　　假设此时我们已经拥有此服务器的shell，但需要在网站路径下写入一句话木马，然而手动寻找网站路径比较费时。将此searchweburl.py上传到服务器任意目录下（没有python环境可上传exe版本），windows下载远程文件命令可参考：[windows常用命令](http://thief.one/2017/03/08/Windows%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/)。
运行如下命令：
```bash
searchweburl.exe -p "e:/" -u "http://localhost:8080/m_1_8/user/html/1.html"
```
运行截图：
![](/upload_image/20170310/2.png)
已经定位出此url所在的物理路径地址。

#### Linux
在一台Linux服务器上搭建了一个简单的web服务,访问如下：
![](/upload_image/20170310/3.png)
　　同样的，我们上传searchweburl.py或者seachweburl（linux免环境版），linux下载远程文件命令可参考：[Linux常用命令](http://thief.one/2017/03/08/Linux%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/)。
运行如下命令：
```bash
./searchweburl -p "/home" -u "http://172.16.1.2:9990/b/a/b/c/d/1.html"
```
运行截图：
![](/upload_image/20170310/4.png)

### 使用技巧
　　我们需要注意到的时，再选择url时尽量去挑选目录结构较多的，因为这样定位出来的结果就越准确。继续以上linux的例子，我们选择另外一个url，如：http://172.16.1.2:9990/b/a/1.html。
![](/upload_image/20170310/5.png)
可以看到URL的目录结构少了好几层，那么运行程序看看结果。
![](/upload_image/20170310/6.png)
　　出现了2条结果，因为这2条结果都符合url目录结构，一般网站服务器上文件较多，因此选择目录层次较深的网站，可越精准得定位出结果。


### 鸡肋问题
　　在我开发这个工具之前，曾用了5分钟的时间思考过此工具的应用场景是否广泛，以及其本身是否鸡肋。无论如何，我最终还是将其开发完成，因为我知道会有人需要它，即使它很鸡肋。

### SearchWebPath下载

windows免环境版：[Searchweburl.exe](https://github.com/tengzhangchao/SearchWebPath/raw/master/windows/searchweburl.exe)
linux免环境版：[Searchweburl](https://github.com/tengzhangchao/SearchWebPath/raw/master/linux/searchweburl)

Github项目地址：[https://github.com/tengzhangchao/SearchWebPath](https://github.com/tengzhangchao/SearchWebPath)

