---
title: 利用chrome_remote_interface实现程序化、自动化Web安全测试
copyright: true
permalink: 1
top: 0
date: 2018-06-07 15:22:18
tags:
- chrome_remote_interface
- headless chrome
categories: 爬虫技术
password:
---
<blockquote class="blockquote-center">高考加油！</blockquote>

　　如果要问有哪些抓包神器或者流量分析工具？以下几款工具是必须要提的，burpsuite（跨平台）、[fiddler](https://thief.one/2017/04/27/1/)（windows下抓包神器）、[wireshark](https://thief.one/2017/02/09/WireShark%E8%BF%87%E6%BB%A4%E8%A7%84%E5%88%99/)（经典网络抓包工具）、[justniffer](https://thief.one/2017/09/27/1/)（与前面几个使用代理获取流量不一样的是，justniffer是基于网卡获取流量）等。以上这几款工具之前我有单独成文介绍过，如有需要可点击蓝色链接移步。
　　那么如果问有哪些程序化的抓包工具？（注明一下这里的程序化指的是可编程）首先burpsuite算一个，因为我们可以开发扩展工具（[burpsuite插件开发之检测越权访问漏洞](https://thief.one/2018/05/04/1/)）；另外fiddle也算一个，可以编辑配置文件，达到扩展功能，之前也介绍过。
　　那么如果问有哪些即可以实现程序化又可以实现自动化的抓包工具？（注明一下这里的自动化是指自动产生流量）这个问题有点拗口，你可能会想为什么一个抓包工具要负责产生流量，流量交给爬虫岂不是更好？这个问题暂且放一放，继续往下看。
<!-- more -->
### 自动化安全测试
　　平常我们经常会使用burpsuite等工具检测一个网站的安全性，检测方法不外乎使用浏览器访问网站且把流量代理到burpsuite上，然后在burpsuite上通过拦截、修改、重放流量等方式测试网站安全性。然而当要测试的网站非常多时，有没有一个更自动化、更省力的方式去测试呢？方案肯定是有的，简单来说要实现自动化web安全测试无非要解决几个问题，首先是流量怎么产生？然后是怎么从流量中分析出漏洞？

#### 自动化测试方案：主动扫描器
　　市面上基于爬虫的主动扫描器就是一种自动化安全测试工具，首先它的流量是通过爬虫爬取url主动产生的，然后利用一些漏洞插件去构造不同的访问请求。短板：目前市面上扫描器爬虫大多基于web1.0，无法加载js渲染网页，而现在越来越多的网站使用web2.0技术实现前后端数据交互。

#### 自动化测试方案：被动扫描器
　　一些大厂内部自研的被动扫描器，首先它的流量不是通过爬虫主动获取的，而是通过监听交换机等网络设备的网卡流量，然后利用一些漏洞插件去分析流量中存在漏洞的点。短板：适合大厂各业务线安全检查不适合测试某个特定的网站，因为需要人为访问网站产生流量。

#### 自动化测试方案：selenium+流量获取工具+漏洞插件
　　selenium是一款网站自动化测试工具，可以程序化的操作浏览器，实现自动化产生流量。再结合抓包工具以及漏洞检测插件，应该就可以解决流量获取以及漏洞检测的问题。短板：用selenium只能实现一些简单的浏览器操作，对于检测复杂的网站系统，似乎不够用，而且速度很慢，性能很差。

#### 自动化测试方案：chrome_remote_interface+漏洞插件
　　之前我介绍过[headless chrome](https://thief.one/2018/03/06/1/)，也介绍过[phantomjs](https://thief.one/2017/03/31/Phantomjs%E6%AD%A3%E7%A1%AE%E6%89%93%E5%BC%80%E6%96%B9%E5%BC%8F/)等web2.0爬虫工具，目前推荐去学习使用headless-chrome。headless chrome工具是用来自动加载js，获取渲染后的页面源码，解决web2.0爬虫之困。而chrome_remote_interface是一个更底层的工具，可以用来分析协议，简单说就是可以分析整个渲染过程，以及截取分析过程中的流量。就类似您打开了chrome浏览器的审查元素功能，然后刷新一下页面，查看一下network信息。
![](/upload_image/20180607/1.png)

### chrome_remote_interface介绍
chrome_remote_interface是一个开源项目，[项目地址](https://github.com/cyrus-and/chrome-remote-interface)，并且支持命令行、编码两种方式，且使用node.js开发。

#### 安装使用
因为chrome_remote_interface是基于nodejs的，因此需要安装npm包管理工具。
```bash
yum install npm -y
```
然后创建一个目录，初始化一个项目
```bash
npm init
```
在目录下安装chrome_remote_interface
```bash
npm install chrome-remote-interface
```
创建一个简单的nodejs程序(nmask.js)：
```bash
const CDP = require('chrome-remote-interface');

// node nmask.js https://nmask.cn

var options = process.argv;
var target_url = options[2];

CDP((client) => {
    // extract domains
    const {Network, Page} = client;
    
    // setup handlers
    Network.requestWillBeSent((params) => {
        console.log(params.request.url);
    });
    Page.loadEventFired(() => {
        client.close();
    });
    
    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        return Page.navigate({url: target_url});//输出请求的url
    }).catch((err) => {
        console.error(err);
        client.close();
    });
}).on('error', (err) => {
    console.error(err);
});

```
说明：在运行这段程序前，必须要在系统上安装chrome以及启动chrome headless监听模式，具体怎么安装chrome headless可以移步：[headless chrome and api](https://thief.one/2018/03/06/1/)
启动chrome headless监听模式：
```bash
chrome --headless --remote-debugging-port=9222
或者
google-chrome --headless --remote-debugging-port=9222
```
然后另外开启一个窗口，运行nodejs：
```bash
node nmask.js https://thief.one
```
运行结果如下：(输出渲染过程中请求的所有url)
![](/upload_image/20180607/2.png)

### chrome_remote_interface for python
　　由于chrome_remote_interface是nodejs实现的，因此对于不熟悉nodejs的朋友来说coding成本比较高。然而好在已经有外国友人用python封装了一个工具，[项目地址](https://github.com/wasiher/chrome_remote_interface_python)，虽然目前此项目尚处于初级阶段，但实实在在地解决了我的问题。

#### 安装使用
基于是用python3.5开发的，那么就clone一下项目，直接安装吧：
```bash
git clone https://github.com/wasiher/chrome-remote-interface-python.git
python3 setup.py install
```
编写一个python版的程序(nmask.py)：
```bash
#! -*- coding:utf-8 -*-

'''
__author__="nMask"
__Date__="7 Jun 2018"
__Blog__="https://thief.one"
__version__="1.0"
__py_version__="3.5"

'''

import asyncio
import chrome_remote_interface


class callbacks(object):
    ''' callback class '''

    target_url = ''
    result = []

    async def start(tabs):
        await tabs.add()

    async def tab_start(tabs, tab):
        await tab.Page.enable()
        await tab.Network.enable()
        await tab.Page.navigate(url=callbacks.target_url)

    async def network__response_received(tabs, tab, requestId, loaderId, timestamp, type, response, **kwargs):
        '''
        print(response.requestHeaders)
        print(dir(response))
        more response attribute https://chromedevtools.github.io/devtools-protocol/tot/Network#type-Response
        '''
        try:
            body = tabs.helpers.old_helpers.unpack_response_body(await tab.Network.get_response_body(requestId=requestId))
        except tabs.FailResponse as e:
            print('[Error]', e)
        else:
            print(response.url,response.status,len(body))
            callbacks.result.append((response.url,response.status,len(body)))

    async def page__frame_stopped_loading(tabs, tab, **kwargs):
        print("[Info]Finish")
        tabs.terminate()

    async def any(tabs, tab, callback_name, parameters):
        pass


if __name__=="__main__":
    callbacks.target_url = "http://www.baidu.com"
    asyncio.get_event_loop().run_until_complete(chrome_remote_interface.Tabs.run('localhost', 9222, callbacks))
    print(callbacks.result)
```
说明：同样的在运行这段代码前，先运行chrome headless监听程序。

然后运行该程序：
```bash
python nmask.py
```
![](/upload_image/20180607/3.png)

说明：运行程序，最终得到渲染过程中请求的url、响应码、响应内容长度。

### Chrome Debugging Protocol 
　　无论是nodejs版本的chrome-remote-interface还是python版本的，实现的底层都是基于Chrome Debugging Protocol接口，[官方文档](https://chromedevtools.github.io/devtools-protocol/)，因此在使用chrome-remote-interface过程中，可以查询一下这个文档。比如python版本中network__response_received函数，是封装了Chrome Debugging Protocol接口Network.ResponseReceived函数，而此函数接受的参数，以及一些属性方法等都可以在该文档中查询。

### 解决文章开头的问题
　　文章开头还留了一个问题，有哪些即可以实现程序化又可以实现自动化的抓包工具？想想chrome-remote-interface能干啥？其一可以使用nodejs、python（可能还有其他语言封装的项目）编程，底层接口文档比较完善；其二用它来写web2.0爬虫，访问页面产生流量，当然区别web1.0爬虫，这里的流量是完整的流量，相当于人工打开浏览器访问网页；其三可以获取流量，并且进行分析。第一点功能实现了程序化，第二三点功能实现了自动化。
　　最后让我们回过头看一下前文提到的自动化测试方案--主动扫描器，其短板就是没法解决web2.0爬虫的困境，而chrome-remote-interface恰恰可以解决，发挥下想象力，其前途应该无限！
























