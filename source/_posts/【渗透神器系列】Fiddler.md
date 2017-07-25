---
title: 【渗透神器系列】Fiddler
date: 2017-04-27 09:41:36
comments: true
tags:
- 渗透神器
- Fiddler
categories: 安全工具
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">人世起起落落 左手边上演的华灯初上 右手边是繁华落幕的星点余光</blockquote>
　　本篇作为渗透神器系列第二篇，将介绍一款渗透界web测试开发界比较流行的一款web流量抓包分析工具，Fiddler。Fiddler的功能这里不多说，简单概括就是抓包、改包、重放。本篇的重点不是介绍Fiddler的基础用法，而是介绍如何通过编程打造属于自己的定制化Fiddler。本篇所记内容大部分来自互联网，如觉内容老套可自行绕道，全当个人查询之用，轻喷即可。
<!--more -->

### 修改规则文件CustomRules.js
CustomRules.js是用Jscript.NET语言写的，语法类似C#。通过修改CustomRules.js可以修改http的请求和应答，不用中断程序，还可以针对不同的url做特殊的处理。
#### CustomRules.js文件位置
Fiddler工具菜单栏：
```bash
rules->CustomRules 
```
本地电脑磁盘存放地址：
```bash         
C:\Documents and Settings\[your user]\MyDocuments\Fiddler2\Scripts\CustomRules.js
```
#### 常用内容
先分享一个常用的内容：
```bash
static function OnBeforeRequest(oSession: Session) {

        // oSession.oRequest.headers.Remove("Cookie");   //移除请求包的cookies
        // oSession.oRequest.headers.Add("Cookie", "username=admin;");  //新建cookies
        // oSession.oRequest["Referer"]="http://www.baidu.com"; //设置referer为baidu

        // if (oSession.HTTPMethodIs("POST")){   //POST修改为GET
        //     oSession.RequestMethod="GET";
        // }   

        // var strBody=oSession.GetRequestBodyAsString();   //获取请求包中的body内容，修改其内容。
        // // // strBody=strBody.replace("111","222");   //替换字符串
        // strBody="11111111111111111111111111111111111"+strBody;  //在发送的数据包前面加上垃圾数据
        // // // strBody=strBody.ToUpper(); //全部转化为大写
        // // // strBody=strBody.ToLower(); //全部转化为小写
        // oSession.utilSetRequestBody(strBody);
}

```
如上所示，修改OnBeforeRequest函数下的代码，可以起到在发送请求之前，自动修改请求包中的一些参数。如可以增删改cookie，headers头参数，可以修改请求包类型等，主要作用就是为了达到渗透测试时某种特殊的作用，比如绕过防火墙。

#### 常用函数
http请求函数：即修改该函数内容，可以在发送http请求包之前修改某些参数。
```bash
static function OnBeforeRequest(oSession: Session)
```
http应答函数：即修改该函数内容，可以在接收http应答包之前修改某些参数
```bash
static function OnBeforeResponse(oSession: Session)
```
#### 函数中的方法属性
##### 筛选某个url
```bash
if (oSession.host.indexOf("thief.one") > -1) {}
```
##### 修改session中的显示样式
```bash
oSession["ui-color"] = "orange"; #即该记录显示的颜色
```
##### 移除http头部中的某字段
```bash
oSession.oRequest.headers.Remove("");
```
##### 修改http头部中的某字段内容
```bash
oSession.oRequest["Referer"] = "http://thief.one";
```
##### 修改host
```bash
oSession.host = "thief.one";
```
##### 修改Origin字段
```bash
oSession.oRequest["Origin"] = "http://thief.one";
```
##### 删除所有的cookie
```bash
oSession.oRequest.headers.Remove("Cookie");
```
##### 新建cookie
```bash
oSession.oRequest.headers.Add("Cookie", "username=nMask;");
```
##### 获取Request中的body字符串
```bash
var strBody=oSession.GetRequestBodyAsString();
```
##### 用正则表达式或者replace方法去修改string
```bash
strBody=strBody.replace("thief","nmask");
```
##### 弹个对话框检查下修改后的body
```bash             
FiddlerObject.alert(strBody);
```
##### 将修改后的body，重新写回Request中
```bash
oSession.utilSetRequestBody(strBody);
```
##### 修改请求url
例如：将请求URI中http协议替换成https协议。
```bash
oSession.fullUrl = "https" + oSession.fullUrl.Substring(oSession.fullUrl.IndexOf(':'));
```
##### 网络限速
1000/下载速度 = 需要delay的时间(毫秒)，比如20kB/s 需要delay50毫秒来接收数据。
```bash
if (m_SimulateModem) {
    // Delay sends by 300ms per KB uploaded.
     oSession["request-trickle-delay"] = "300";
     // Delay receives by 150ms per KB downloaded.
     oSession["response-trickle-delay"] = "150";
 }
```
Fiddler可以定制化很多功能，以上是我平时常用的一些内容，如想要了解更多用法请参考官方文档：[Fiddler文档](http://docs.telerik.com/fiddler/Configure-Fiddler/Tasks/ConfigureFiddler)

### 传送门
[【渗透神器系列】DNS信息查询](http://thief.one/2017/07/12/1/)
[【渗透神器系列】nc](http://thief.one/2017/04/10/1/)
[【渗透神器系列】nmap](http://thief.one/2017/05/02/1/)
[【渗透神器系列】搜索引擎](http://thief.one/2017/05/19/1)
[【渗透神器系列】WireShark](http://thief.one/2017/02/09/WireShark%E8%BF%87%E6%BB%A4%E8%A7%84%E5%88%99/)

参考：http://www.open-open.com/lib/view/open1429059806736.html
