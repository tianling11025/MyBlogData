---
title: Selenium+Phantomjs爬过的那些坑
date: 2017-03-01 16:37:38
comments: true
tags: Phantomjs
categories: 编程之道
---
<blockquote class="blockquote-center">技术的探索就是不断提出假设，然后不断去推翻它</blockquote>
最近在跟同事使用phantomjs编写爬虫时，遇到了很多有意思的坑，我们在分析了一番后得出了一些结论以及解决方案，此分享一下。
	<!--more -->
　　事情的起因，是因为我们要利用phantomjs访问一批网站获取源码以及url，然后当我们查看输出结果时却发现请求的url与访问后获取的url并不对应，比如我用phantomjs访问baidu，返回的结果却显示当前url是bing。由此引发了我们一系列的猜想，由于这方面互联网上的资源比较少，因此也只能自己猜测并动手验证了。
　　对于结果值不对应问题，我暂时定义为，phantomjs状态被污染或者覆盖。简单来说，我们先去访问a网站，获取结果后，我们又访问了b网站，然后获取b网站的结果，然而我们发现b网站的结果却是a网站。那么我们首先认为，phantomjs再处理b网站时，本身的状态没有被更新，导致获取b网站的结果仍然为a网站。
　　那么是什么原因导致phantomjs状态未更新呢？
　　我同事的博客中详细介绍了2种原因，详情请看：[https://eth.space/phantomjs-debug/](https://eth.space/phantomjs-debug/)，这里便不再重复。

作为补充说明，我这边贴出测试代码，以供参考

### phantomjs状态污染测试

#### 测试代码
```bash
d=webdriver.PhantomJS("D:\python27\Scripts\phantomjs.exe",service_args=['--load-images=no','--disk-cache=yes'])
d.implicitly_wait(10)        ##设置超时时间
d.set_page_load_timeout(10)  ##设置超时时间

def gethttp(url):
    try:
        d.get(url)
    except Exception,e:
        print e

    print d.current_url

```
#### 测试（一）
当我们先用phantomjs运行了cn.bing.com，然后运行123.114.com网站，注意123.114.com是访问不了的.
```bash
gethttp("http://cn.bing.com") #网站能正常打开
gethttp("http://123.114.com") #DNS解析失败，网站打不开
```
执行结果：
```bash
http://cn.bing.com/
http://cn.bing.com/
```
可以看到我们获取123.114.com网站的信息时竟然返回了cn.bing.com。

#### 测试（二）
当我们访问一个网页源码里面带有onbeforeunload元素的网页时。
```bash
gethttp("http://www.zzxzxyey.com") #网页内存在onbeforeunload元素
gethttp("http://cn.bing.com") #网站能正常打开
```
执行结果：
```bash
http://www.zzxzxyey.com/
http://www.zzxzxyey.com/
```
可以看到以上2种情况，都会导致phantomjs状态污染，至于其他情况还待后期观察测试。

### 解决方案

#### 彻底法
每次d.get()请求完就d.quit()关闭phantomjs进程，待到新的请求再开启。（非常耗资源）

#### 普通法
每次get前去判断url是否能被dns解析，url是否能打开。（也有点耗资源）

#### 优雅法
每次get后，保存current_url的值，待下一次请求后与此值相比较，如果一样，则说明状态没有被改变。
（当然，有些特殊情况除外，比如每次get的网站都是同一个，或者批量get的网站中有相同地址的。）

如遇到Phantomjs性能优化问题，请移步[Phantomjs性能优化](http://thief.one/2017/03/01/Phantomjs%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
