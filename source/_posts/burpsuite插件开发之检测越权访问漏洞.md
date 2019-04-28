---
title: burpsuite插件开发之检测越权访问漏洞
copyright: true
permalink: 1
top: 0
date: 2018-05-04 15:09:07
tags:
- burpsuite
categories: 编程之道
password:
---
<blockquote class="blockquote-center">那个喝醉的夜晚，挡不住我们的步伐</blockquote>

　　前些天公司买了些BurpSuite的License，终于可以用上正版了，先给公司来波赞！好啦，言归正传，BurpSuite作为Web安全测试的一大神器，其中一个优势就是其扩展性好。BurpSuite支持Java、Python、Ruby作为其插件的扩展语言，而在其内置的Bapp_Store中也有很多很强大的插件。作为一名程序猿，心想是时候自己动手开发一款专属插件了，抱着此心态我便开始尝试学习摸索着Coding，于是便有了此文。
<!-- more -->

### 插件语言的选择
　　以上所述Burp支持Java、Python、Ruby语言的扩展，相对来说我更熟悉Python，因此就用Python开始学习写插件，对于速度要求高的朋友可以用Java写。熟悉Python的朋友肯定知道，Python分为Cython、Jython等。前者就是我们通常所说的Python，后者是Java版本的Python，简单理解就是用Jython可以调用Java的库。

### burpsuite jython开发环境
　　想要开发使用一款属于自己的BurpSuite插件，必须要部署好Jython开发环境以及Jython运行环境。前者需要在开发jython程序的平台上搭建环境，后者需要在运行burpsuite的平台搭建环境。鉴于一般开发以及使用插件都在用一个平台上，比如mac，因此本文介绍一下如何在mac上安装jython环境。

#### install jython for Mac
首先我们需要在mac上安装jython的环境以便开发jython程序，就像安装python环境一样，mac上安装jython命令：
```bash
brew install jython
```
安装完以后，jython安装在/usr/local/Cellar/jython/目录下，需要设置环境变量，将/usr/local/Cellar/jython/2.7.1/libexec/bin添加到环境变量，然后在shell中输入：

```bash
$jython
Jython 2.7.1 (default:0df7adb1b397, Jun 30 2017, 19:02:43)
[Java HotSpot(TM) 64-Bit Server VM (Oracle Corporation)] on java1.8.0_111
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
说明：其他平台（windows，linux）安装jython方式请自行google，应该比较类似。

#### Load Jython to Burpsuite
mac上安装完jython环境后，需要在burpsuite中加载jython环境，注意这里选择的是jar文件。
![](/upload_image/20180504/1.png)

### 开发jython程序
本篇以开发一款检测未授权访问漏洞的插件为例介绍一下插件的开发过程，由于本文重点在于介绍如何开发一款bp插件，以及一些不可抗因素，本文介绍的插件均为简化后的版本。

#### 创建main.py文件
``` bash
#! -*- coding:utf-8 -*-

import re
from burp import IBurpExtender # 定义插件的基本信息类
from burp import IHttpListener # http流量监听类
from noauth import noauth_request

# 敏感接口检测，并输出敏感接口信息
res_host = re.compile(r'Host: ([^,]*)')
res_path = re.compile(r'(GET|POST) ([^ ]*) HTTP/')


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers() # 通用函数
        self._callbacks.setExtensionName("sensitive_interface_scan")

        print "load sensitive_interface_scan plugin success!"
        print "============================================="
        print ""

        # register ourselves as an HTTP listener
        callbacks.registerHttpListener(self)
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if toolFlag == 4:
            if not messageIsRequest:
                response = messageInfo.getResponse() # get response
                analyzedResponse = self._helpers.analyzeResponse(response)
                body = response[analyzedResponse.getBodyOffset():] 
                body_string = body.tostring() # get response_body

                request = messageInfo.getRequest()
                analyzedRequest = self._helpers.analyzeResponse(request)
                request_header = analyzedRequest.getHeaders() 
                try:
                    method,path = res_path.findall(request_header[0])[0]
                    host = res_host.findall(request_header[1])[0]
                    url = method+" "+host+path
                except:
                    url = ""

                if method=="GET":
                    # 检测GET请求的接口

                    print "[Info]Check url is ",url

                    cur = noauth_request(host,path,body_string)
                    noauth_result = cur.run()

                    if noauth_result: 
                        print "[Info]Found it is a noauth Interface %s" % noauth_result[0][0]
                        print "[Info]remove param is ",noauth_result[0][1]

                    print "======================================================================================"
                    print ""

```
说明：此文件为插件入口文件，其中导入的burp内置类IBurpExtender为基类，即所有插件都需要使用继承此类，IHttpListener类用来获取http请求以及响应内容。

#### 创建noauth.py文件
```bash
#! -*- coding:utf-8 -*-

'''未授权访问poc(GET)'''

import requests
from furl import furl

auth_params=["token","sign","ticket"]

# headers 里面除去cookie

headers={
    
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,mt;q=0.7,zh-TW;q=0.6",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cookie":"test",

}


class noauth_request(object):
    # 未授权访问漏洞检测

    def __init__(self,host,path,body_string):

        self.url = "http://"+host+path
        self.uri = str(furl(self.url).remove(args=True))
        self.body_string = body_string
        self.param = dict(furl(self.url).args)
        self.remove_param = []

    def run(self):
        
        result_list=[]

        self.remove_auth() # remove params,example:auth,token,sign......

        response_body,current_url = self.get_response()

        if response_body == self.body_string:

            result_list.append((current_url,self.remove_param,response_body))
        
        return result_list

    def remove_auth(self):
        # 删除用户认证的参数

        for i in auth_params:
            if self.param.has_key(i):
                self.remove_param.append(i)
                self.param.pop(i)

    def get_response(self):
        # 重放接口获取返回值

        current_url = ""
        response_body = ""

        try:
            res=requests.get(url=self.uri, params=self.param, timeout=20, headers=headers)
        except Exception,e:
            print "[noauth_request:get_response]"+str(e)

            if "HTTPSConnectionPool" in str(e):
                try:
                    res=requests.get(url=self.uri.replace("http://","https://"), params=self.param, timeout=20, headers=headers)
                except Exception,e:
                    print "[noauth_request:get_response]"+str(e)
                else:
                    current_url = res.url
                    response_body = res.text
        else:
            current_url = res.url
            response_body = res.text

        return response_body,current_url

```
说明：此文件为检测未授权访问类，功能比较简单，获取原始请求以及响应包，去除请求接口的cookie以及token等认证后重放，查看返回结果有没有变化。一般情况下还会检测响应包是否包含敏感信息，这里为了方便演示，简化了插件功能。

### 将jython程序添加到burpsuite中
选择添加一个插件：
![](/upload_image/20180504/2.png)
注意下图中的标记部分：
![](/upload_image/20180504/3.png)
说明：类型选择python，文件选择入口文件，burpsuite会自动获取本地的依赖文件；输出这里选择在控制台输出，因为此插件没有写ui界面。

加载成功后，会在控制台输出：
![](/upload_image/20180504/4.png)

然后我们就去开启浏览器代理，关闭bp拦截，愉快的进行web系统测试吧，若插件检测到了未授权访问的接口，则会输出类似如下：

![](/upload_image/20180504/6.png)

### 增加UI界面代码
在控制台输出的方式总归没有那么优雅，因此如果能像其内置的功能那样在界面上输出就更好了。以下是一段简单的ui界面开发代码：

```bash
# -*- coding:utf-8 -*-

# 导入 burp 接口
from burp import IBurpExtender, ITab

# 导入 Java 库
from javax.swing import JPanel
from javax.swing import JButton

class BurpExtender(IBurpExtender, ITab):
    ''' 继承burp java父类 '''

    def registerExtenderCallbacks(self, callbacks):
        # 注册插件信息

        self._cb = callbacks # 回调
        self._hp = callbacks.getHelpers() # 帮助信息

        self._cb.setExtensionName('python_test_plugin') # 插件名称

        print 'load python_test_plugin success!'

        self.mainPanel = JPanel() # 面板
        
        self.testBtn = JButton(u'一个按钮', actionPerformed=self.testBtn_onClick) # 初始化一个 JButton 并绑定单击事件

        self.mainPanel.add(self.testBtn) # 面板中添加这个按钮

        self._cb.customizeUiComponent(self.mainPanel) 
        self._cb.addSuiteTab(self)

    def testBtn_onClick(self, event):
        # 点击按钮事件

        print "click button"

    def getTabCaption(self):
        # 获取tab按钮名称

        return 'python_test_plugin'

    def getUiComponent(self):
        # 获取面板内容·

        return self.mainPanel
```
说明：这只是一个ui界面开发的demo，效果如下：

![](/upload_image/20180504/5.png)

### burp插件开发文档
这里介绍几个常用的burp类：
```bash
1. 插件入口和帮助接口类：IBurpExtender、IBurpExtenderCallbacks、IExtensionHelpers、IExtensionStateListener
IBurpExtender接口类是Burp插件的入口，所有Burp的插件均需要实现此接口，并且类命名为BurpExtender。 IBurpExtenderCallbacks接口类是IBurpExtender接口的实现类与Burp其他各个组件（Scanner、Intruder、Spider......）、各个通信对象（HttpRequestResponse、HttpService、SessionHandlingAction）之间的纽带。 IExtensionHelpers、IExtensionStateListener这两个接口类是插件的帮助和管理操作的接口定义。

2. UI相关接口类：IContextMenuFactory、IContextMenuInvocation、ITab、ITextEditor、IMessageEditor、IMenuItemHandler
这类接口类主要是定义Burp插件的UI显示和动作的处理事件，主要是软件交互中使用。

3. Burp工具组件接口类：IInterceptedProxyMessage、IIntruderAttack、IIntruderPayloadGenerator、IIntruderPayloadGeneratorFactory、IIntruderPayloadProcessor、IProxyListener、IScanIssue、IScannerCheck、IScannerInsertionPoint、IScannerInsertionPointProvider、IScannerListener、IScanQueueItem、IScopeChangeListener
这些接口类的功能非常好理解，Burp在接口定义的命名中使用了的见名知意的规范，看到接口类的名称，基本就能猜测出来这个接口是适用于哪个工具组件。

4. HTTP消息处理接口类：ICookie、IHttpListener、IHttpRequestResponse、IHttpRequestResponsePersisted、IHttpRequestResponseWithMarkers、IHttpService、IRequestInfo、IParameter、IResponseInfo

这些接口的定义主要是围绕HTTP消息通信过程中涉及的Cookie、Request、Response、Parameter几大消息对象，通过对通信消息头、消息体的数据处理，来达到控制HTTP消息传递的目的。
```
关于更多关于burp开发相关的文档，可以参考下：https://portswigger.net/burp/extender/

### 本文参考
http://xdxd.love/2015/04/20/burpsuite%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91%E4%B9%8Bpython%E7%AF%87/


写不动了~~~~~






