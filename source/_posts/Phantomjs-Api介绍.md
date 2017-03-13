---
title: Phantomjs Api介绍
date: 2017-03-13 19:56:20
comments: true
tags: Phantomjs
categories: 编程之道
---

<blockquote class="blockquote-center">晋书云：“生犀不敢烧，燃之有异香，沾衣带，人能与鬼通”</blockquote>
	
　　之前几篇文章介绍了Selenium+Phantomjs用法，也探讨过性能优化问题。然而利用selenium或者说python去运行phantomjs本质上并不是高效的方法，再者selenium对于phantomjs的封装并不是特别完善（长久没有更新过），因此很有必要研究下原生态的phantomjs。于是我参考[官网](http://phantomjs.org)介绍，学习总结成文，在此记录分享。
<!--more -->
　　phantomjs全面支持web而不需要浏览器，又称为无头浏览器，它是一个基于webkit的服务端javascript API，可以用于页面自动化，网络监测，网页截图，爬虫抓取等。phantomjs有很多api接口，接口语法用的就是js的语法，phantom提供了类，实例化以后可以调用对象的方法，通过回调函数可以实现自己想要的功能，其APi主要有web服务端Api、webPage APi、System APi等，这里主要介绍几种常用的api的用法。

### phantomjs-Command Line Interface
描述：phantomjs命令行用法以及参数设置
首先我们看下如何调用phantomjs运行js脚本
```bash
phantomjs [options] somescript.js [arg1 [arg2 [...]]]
```
可选参数：（只列举常用的）

* --disk-cache=[true|false] 缓存设置
* --ignore-ssl-errors=[true|false] 忽略ssl错误
* --load-images=[true|false] 加载图片
* --proxy=address:port  设置代理

有很多参数，不一一列举，详细参考：[phantomjs-Command Line Interface](http://phantomjs.org/api/command-line.html)

### phantomjs-system module
描述：phantomjs系统操作APi
文档地址：[phantomjs-system module](http://phantomjs.org/api/system/)
作用：用于system系统操作

#### args（获取程序输入参数）
代码（test.js）
```bash
var system = require('system');
var args = system.args;

if (args.length === 1) {
  console.log('Try to pass some arguments when invoking this script!');
} else {
  args.forEach(function(arg, i) {
    console.log(i + ': ' + arg);
  });
}
```
运行：
phantomjs test.js hello
结果：
0 test.js
1 hello
功能：接受控制台输入参数。

#### env（系统环境变量）

代码（test.js）:
```bash
var system = require('system');
var env = system.env;

Object.keys(env).forEach(function(key) {
  console.log(key + '=' + env[key]);
});
```
运行：phantomjs test.js
功能：列出系统环境变量

#### os（平台类型）

代码（test.js）：
```bash
var system = require('system');
var os = system.os;
console.log(os.architecture);  // '32bit'
console.log(os.name);  // 'windows'
console.log(os.version);  // '7'
```
运行：phantomjs test.js
结果：
32bit
windows
7
功能：输出运行平台类型

#### pid （进程id）

代码（test.js）:
```bash
var system = require('system');
var pid = system.pid;

console.log(pid);
```
输出进程pid

#### platgform（平台信息）

代码（test.js）:
```bash
var system = require('system');
console.log(system.platform); // 'phantomjs'
```
运行结果:phantomjs

### Phantomjs-web server module
描述：phantomjs web server module APi
文档地址：[Phantomjs-web server module](http://phantomjs.org/api/webserver/method/listen.html)
作用：作为webserver服务端，提供http服务。
代码（test.js）：
```bash
var webserver = require('webserver');
var server = webserver.create();
var service = server.listen(8080, function(request, response) {
  response.statusCode = 200;
  response.setHeader("Cookie","1adaa2121");
  response.setEncoding("binary");
  response.write('<html><body>Hello!</body></html>');
  console.log(request.method);
  console.log(request.url);
  console.log(request.httpVersion);
  console.log(request.headers);
  console.log(request.post);
  console.log(request.postRaw);
  response.close();
});
```
运行：phantomjs test.js
访问：http://localhost:8080

如果要指定ip与端口，则8080可以这样写：'127.0.0.1:9999'。

其中有2个参数，request与response。

request参数方法：
* request.method
* request.url
* request.httpVersion
* request.headers
* request.post
* request.postRaw

用来获取请求内容。

response参数方法：
* response.headers
* response.setheader(name,value)
* response.header(name)
* response.statusCode()
* response.setEncoding("binary")
* response.write(html_data)
* response.writeHead(statusCode,headers)
* reponse.close()
* reponse.closeGracefully()

### Phantomjs-web page module
描述：phantomjs web page module APi
文档地址：[Phantomjs-web page module](http://phantomjs.org/api/webpage/)
作用：用来发送http请求，获取网络资源，或者页面操作。

#### 实例化api类

```bash
var webPage = require('webpage');
var page = webPage.create();
```
#### page方法
* page.content  源码
* page.title    标题
* page.cookie    cookie
* page.plainText  网页内容（去除html）
* page.setting 参数设置
* page.url 当前url

#### clipRect剪切页面
```bash
page.clipRect = {
    top: 14,
    left: 3,
    width: 400,
    height: 300
};
```

#### content获取网页源码
```bash
var webPage = require('webpage');
var page = webPage.create();

page.open('http://thief.one', function (status) {
  var content = page.content;
  console.log('Content: ' + content);
  phantom.exit();
});
```
#### cookie获取页面cookie
```bash
page.open('http://thief.one', function (status) {
  var cookies = page.cookies;

  console.log('Listing cookies:');
  for(var i in cookies) {
    console.log(cookies[i].name + '=' + cookies[i].value);
  }

  phantom.exit();
});
```
#### 设置customHeaders内容：
```bash
page.customHeaders = {
  "X-Test": "foo",
  "DNT": "1"
};
```
#### plainText获取网页内容（去除html只留内容）
```bash
page.open('http://thief.one', function (status) {
  console.log('Stripped down page text:\n' + page.plainText);
  phantom.exit();
});
```
#### setting 请求头设置
```bash
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
```
#### zoomFactor缩略图创建
```bash
var webPage = require('webpage');
var page = webPage.create();

page.zoomFactor = 0.25;
page.render('capture.png');
```
#### addcookie添加cookie
```bash
phantom.addCookie({
  'name'     : 'Valid-Cookie-Name',   /* required property */
  'value'    : 'Valid-Cookie-Value',  /* required property */
  'domain'   : 'localhost',
  'path'     : '/foo',                /* required property */
  'httponly' : true,
  'secure'   : false,
  'expires'  : (new Date()).getTime() + (1000 * 60 * 60)   /* <-- expires in 1 hour */
});
```
#### 上传文件
```bash
var webPage = require('webpage');
var page = webPage.create();

page.uploadFile('input[name=image]', '/path/to/some/photo.jpg');
```
#### render页面截图
```bash
page.viewportSize = { width: 1920, height: 1080 };
page.open("http://www.google.com", function start(status) {
  page.render('google_home.jpeg', {format: 'jpeg', quality: '100'});
  phantom.exit();
});
```

更多例子请参考：[examples](http://phantomjs.org/examples/index.html)