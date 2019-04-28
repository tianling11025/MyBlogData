---
title: Headless Chrome and API
copyright: true
permalink: 1
top: 0
date: 2018-03-06 13:56:54
tags:
- Headless Chrome
- Puppeteer
- pychrome
- chromeless
categories: 爬虫技术
password:
---
<blockquote class="blockquote-center">我已爬遍了全世界，而你却迟迟不见</blockquote>

　　自从Google在chrome59版本后加入了 [Headless Chrome](https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md)，类似phantomjs、selenium等工具作者都放弃了维护自身的产品（原因可参考文章 [QtWebkit or Headless Chrome](https://paper.seebug.org/537/?from=timeline&isappinstalled=0)）。因此作为使用者的我们也是时候放弃phantomjs，转而研究Headless Chrome了。由于网上对于Headless Chrome的资料还很少，因此我先收集整理一波，随后慢慢学习研究，渐渐将本篇内容补充完善。
<!-- more -->

### Headless Chrome 介绍
headless chrome意思是无头chrome浏览器，相对于传统的chrome浏览器，这是一个可以在后台用命令行操作浏览器的工具，对于爬虫编写以及web自动化测试都有很大的作用。相比较同类工具Phantomjs，其更加强大（主要因为其依赖的webkit更新）。

### Headless Chrome 安装
目前只支持mac与linux系统，需要下载chrome浏览器并安装。

#### mac install headless chrome
mac下直接去官网下载安装包即可，mac下chrome浏览器位置，为了方便使用，用alias别名启动。
```bash
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
alias chrome-canary="/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary"
alias chromium="/Applications/Chromium.app/Contents/MacOS/Chromium"
```
下载[chrome-canary](https://www.google.com/chrome/browser/canary.html)版

说明：`Mac 和 Linux 上的 Chrome 59 都可以运行无需显示模式。对 Windows 的支持将在 Chrome 60 中提供。要检查你使用的 Chrome 版本，请在浏览器中打开 chrome://version。`

#### linux install headless chrome
添加源：
```bash
vim /etc/yum.repos.d/chrome.repo
写入以下内容：

[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=0
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
```
安装：
```bash
yum install -y google-chrome-stable
```
测试运行：
```bash
google-chrome --headless --print-to-pdf https://thief.one
```
报错处理：
```bash
Running as root without --no-sandbox is not supported # 错误信息
```
解析方案：
```bash
vim /opt/google/chrome/google-chrome
找到 exec -a "$0" "$HERE/chrome" "$@"
改为 exec -a "$0" "$HERE/chrome" "$@" --user-data-dir --no-sandbox
```

`说明：若在安装过程中报错，则将源文件中的gpgcheck改为0`

linux安装headless chrome参考：http://akai-tsuki.hatenablog.com/entry/2017/06/18/000000

### Headless Chrome 基础用法
HELP信息：
```bash
chrome \
--headless \                   # Runs Chrome in headless mode.
--disable-gpu \                # Temporarily needed for now.
--remote-debugging-address=127.0.0.1
--remote-debugging-port=9222 \
 https://thief.one   # URL to open. Defaults to about:blank.
```

#### 访问一个网页获取源码
--dump-dom 标志将打印 document.body.innerHTML 到标准输出：
```bash
chrome --headless --disable-gpu --dump-dom https://thief.one/
```

#### 访问一个网页将源码创建成一个PDF
--print-to-pdf 标志将页面转出为 PDF 文件：
```bash
chrome --headless --disable-gpu --print-to-pdf https://thief.one/
```

#### 访问一个网页并截图
使用--screenshot标志运行 Headless Chrome 将在当前工作目录中生成一个名为 screenshot.png的文件：
```bash
chrome --headless --disable-gpu --screenshot https://thief.one/

# 设置图片大小
chrome --headless --disable-gpu --screenshot --window-size=1280,1696 https://thief.one/
```

#### 访问一个网页并进行js交互（REPL模式）
--repl 标志可以使 Headless Chrome 运行在一个你可以使用浏览器评估 JS 表达式的模式下。执行下面的命令：
```bash
chrome --headless --disable-gpu --repl https://thief.one
>>> location.href
{"result":{"type":"string","value":"https://thief.one"}}
>>> quit
```

#### 启动一个监听端口
```bash
chrome --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0
```
可以通过浏览器打开：http://0.0.0.0:9222 

### Headless Chrome API
以上演示了使用命令行的方式操作headless chrome，那么怎么在代码中使用它呢？
api工具如下：
官方：[puppeteer](https://github.com/GoogleChrome/puppeteer)
底层：[chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface/)
活跃：[chromeless](https://github.com/graphcool/chromeless)
非官方：[headless-chrome-crawler](https://github.com/yujiosaka/headless-chrome-crawler)

Python相关的API：
[pychrome](https://github.com/fate0/pychrome)
[Pyppeteer 推荐](https://github.com/miyakogi/pyppeteer)
[chromote](https://github.com/iiSeymour/chromote)
[chrome_remote_interface_python](https://github.com/wasiher/chrome_remote_interface_python)

#### puppeteer 介绍
Puppeteer 是一个由 Chrome 团队开发的 Node 库。它提供了一个高层次的 API 来控制无需显示版（或 完全版）的 Chrome。它与其他自动化测试库，如 Phantom 和 NightmareJS 相类似，但是只适用于最新版本的 Chrome。

#### puppeteer 安装
```bash
mkdir puppeteer_test # 创建一个项目目录
cd puppeteer_test
npm init
npm i --save puppeteer
```
安装puppeteer前需要在系统上安装nodejs与npm；安装完puppeteer，默认会自动安装最新版本的chromium。
注意：`系统默认安装的npm与nodejs版本都很低，而使用puppeteer需要node6.4.0+，async/await需要node7.6.0+，因此建议安装node7.6.0版本，否则会导致无法使用。`

##### 安装升级nodejs与npm
要安装puppeteer，需要先安装npm与nodejs，而puppeteer对nodejs版本有要求，因此不能用系统默认安装的nodejs版本。
```bash
wget http://nodejs.org/dist/v7.6.0/node-v7.6.0-linux-x64.tar.gz
tar -zvxf node-v7.6.0-linux-x64.tar.gz
```
共享至全局
```bash
rm -rf /usr/bin/node /usr/bin/npm
ln -s /path/node-v7.6.0-linux-x64/bin/node /usr/bin/node  
ln -s /path/node-v7.6.0-linux-x64/bin/npm /usr/bin/npm
```
若用yum安装过nodejs，需要移除其他版本:
```bash
yum remove npm
yum remove nodejs
```
查看nodejs与npm版本：
```bash
node -v
npm -v
```
安装升级nodejs过程参考：http://jeeinn.com/2017/02/236/

#### puppeteer 使用
在使用puppeteer前，先要确定puppeteer、nodejs、npm安装成功（版本正确），且headless chrome安装成功。
官方API文档：https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md

##### 打印用户代理：
在puppeteer_test目录下创建一个example1.js文件，写入：
```bash
const puppeteer = require('puppeteer');

(async() => {
 const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
 console.log(await browser.version());
 browser.close();
})();
```
运行代码:
```bash
node example1.js
```
##### 获取页面的屏幕截图：
创建一个example2.js文件，写入：
```bash
const puppeteer = require('puppeteer');

(async() => {

const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();
await page.goto('https://thief.one', {waitUntil: 'networkidle2'});
await page.pdf({path: 'screen.pdf', format: 'A4'});

browser.close();
})();
```
运行代码：
```bash
node example2.js
```
说明：在运行puppeteer之前不需要额外开启一个headless-chrome进程，因为其本身就会去开启。

##### 发送POST请求获取源码
```bash
const puppeteer = require('puppeteer');

puppeteer.launch({headless: true,args: ['--no-sandbox', '--disable-setuid-sandbox'],}).then(async browser => {

  const page = await browser.newPage();
  await page.setRequestInterception(true); // 开启请求捕捉
  page.on('request', interceptedRequest => {
    const overrides = {};
    //console.log(interceptedRequest.url()); // 输出捕捉到的请求URL
    if (interceptedRequest.url()=='http://127.0.0.1:8000/'){
       overrides.method = 'POST';
       overrides.postData = '{"id":"2"}';
    }
    interceptedRequest.continue(overrides); // 重放
   });
  await page.goto('http://127.0.0.1:8000/');
  await console.log(await page.content()); // 输出源码
  await browser.close();
});
```

##### 安装puppeteer报错
在linux下安装puppeteer报错，即:
```bash
npm i --save puppeteer 命令没有运行成功
```
失败原因可能是linux版本不支持，centos7下成功，centos6下测试失败。

##### 运行puppeteer报错处理
报错如下，说明代码语法有问题，或者node版本太低，不符合要求：
```bash
SyntaxError: Unexpected token function
```
报错如下，说明代码中需要设置headless状态为true
```bash
Failed to launch chrome
```
解决方案，修改代码为如下：
```bash
const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

```
报错如下，与上面解决方案一致：
```bash
1025/084740.006078:ERROR:zygote_host_impl_linux.cc(88)] Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
```
#### pyppeteer
pyppeteer模版是对puppeteer的python封装，因为puppeteer是用nodejs写的，所以要在python中使用得用pyppeteer模块。
##### pyppeteer安装
pyppeteer模版只支持python3.5以上版本。
```bash
python3 -m pip install pyppeteer
```
##### pyppeteer简单的例子
截图：
```bash
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```
说明：在使用pyppeteer时，不需要额外开启headless-chrome进程（与puppeteer一样）。更多pyppeteer模版使用方法，参考：https://miyakogi.github.io/pyppeteer/reference.html#page-class

##### pyppeteer报错处理
错误类似如下：
```bash
pyppeteer.errors.BrowserError: Failed to connect to browser port: http://127.0.0.1:58871/json/version
```
解决方案：
```bash
加上：args=['--no-sandbox']，同puppeteer类似。

browser = await launch(args=['--no-sandbox'])
```

#### chrome-remote-interface工具
可以用来分析渲染一个页面过程中所有的请求过程，包括获取所有的请求接口以及响应内容等。再运行chrome-remote-interface代码前，需要先启动headless chrome进程，即：
```bash
chrome --headless --remote-debugging-port=9222
```
安装chrome-remote-interface：
```bash
npm install chrome-remote-interface 
```
然后编写代码：(以获取所有请求url为例)
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
运行这段代码：
```bash
node nmask.js https://thief.one
```


#### chromeless介绍
chromeless社区比较火热，代码更新也非常频繁，个人比较看好。

#### chromeless安装
chromeless对nodejs版本要求是>8.2(centos7下node7.6测试可以)，因此需要先升级nodejs，升级方法参考前文；升级完以后，再安装chromeless项目环境。
```bash
mkdir chromeless_test
cd chromeless_test
npm init
npm install chromeless
```
#### chromeless使用
官方API文档：https://github.com/graphcool/chromeless/blob/master/docs/api.md#api-goto
在线代码运行环境：[https://chromeless.netlify.com](https://chromeless.netlify.com/#src=)

创建chromeless_test.js,写入：
```bash
const { Chromeless } = require('chromeless')

async function run() {
  const chromeless = new Chromeless()

  const screenshot = await chromeless
    .goto('https://www.baidu.com')
    //.type('chromeless', 'input[name="q"]')
    //.press(13)
    //.wait('#resultStats')
    .screenshot()

  console.log(screenshot) // prints local file path or S3 url

  await chromeless.end()
}

run().catch(console.error.bind(console))
```
运行代码：
```bash
nohup google-chrome --headless --remote-debugging-port=9222 & #开启本地headless chrome
node chromeless_test.js
```
`注意：在运行chromeless前，需要先安装headless chrome，并且需要在本地开启--remote-debugging-port=9222，监听本地9222端口；chromeless也支持使用远程的headless chrome`

#### pychrome工具
`暂没有研究，尽情期待！`

### 常见问题

#### Linux截图中文字体变方块如何解决？
出现这类问题主要是因为linux服务器字体缺失的问题，解决方案是将字体文件copy到linux服务器/usr/share/fonts/zh_CN目录下。

第一步：从windows或者mac上获取字体文件，mac上的字体文件地址为：/Library/Fonts，windows字体地址为：c盘下的Windows/Fonts。将Fonts目录打包上传到linux服务器/usr/share/fonts/zh_CN目录下，然后解压。

第二步：设置权限
```bash
chmod -R 755 /usr/share/fonts/zh_CN
```
第三步：生成fonts.scale
```bash
yum -y install ttmkfdir
ttmkfdir -e /usr/share/X11/fonts/encodings/encodings.dir
```
第四步：修改字体配置文件
```bash
vim /etc/fonts/fonts.conf


在<dir>....</dir>列表中添加字体

如：<dir>/usr/share/fonts/zh_CN/Fonts</dir>
```
第五步：刷新字体缓存
```bash
fc-cache
```
#### 命令行运行headless chrome需要使用--disable-gpu参数吗？
```bash
目前--disable-gpu 标志在处理一些bug时是需要的，在未来版本的 Chrome 中就不需要了。
```
#### 系统仍然需要安装Xvfb吗？
```bash
不需要，Headless Chrome 不使用窗口，所以不需要像 Xvfb 这样的显示服务器。

你问什么是 Xvfb？
Xvfb 是一个用于类 Unix 系统的运行于内存之内的显示服务器，可以让你运行图形应用程序（如 Chrome），而无需附加的物理显示器。许多人使用 Xvfb 运行早期版本的 Chrome 进行 “headless” 测试。
```
#### 如何创建一个运行 Headless Chrome 的 Docker 容器？
```bash
查看 lighthouse-ci。它有一个使用 Ubuntu 作为基础镜像的 Dockerfile 示例，并且在 App Engine Flexible 容器中安装和运行了 Lighthouse。
```

#### headless chrome和 PhantomJS 有什么关系？
```bash
Headless Chrome 和 PhantomJS 是类似的工具。它们都可以用来在无需显示的环境中进行自动化测试。两者的主要不同在于 Phantom 使用了一个较老版本的 WebKit 作为它的渲染引擎，而 Headless Chrome 使用了最新版本的 Blink。
```

`下篇将介绍分布式漏扫爬虫框架的设计与实现，以及写爬虫过程中需要注意的点`

### 参考文章
https://zhuanlan.zhihu.com/p/29207391
https://developers.google.com/web/updates/2017/04/headless-chrome
https://juejin.im/entry/58fd5e645c497d005803b6a4
http://csbun.github.io/blog/2017/09/puppeteer/
