---
title: bootstrap前端框架
copyright: true
permalink: 1
top: 0
date: 2017-08-23 16:47:34
tags:
- bootstrap
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Let bygones be bygones
过去的就让它过去吧</blockquote>
　　现在Web前端的技术发展得很快，web页面做得越来越炫目。然而作为一名"后端程序员"，不会写css，写不好javascript，不懂jquery怎么办？没关系，本篇将介绍前端开发神器--bootstrap，学会它立马变身前端达人。（题外话：我也是被前端开发搞得心力憔悴后，才发现有这个框架，用起来简直爽！）
<!-- more -->

### Who is bootstrap?
　　Bootstrap是由Twitter的Mark Otto和Jacob Thornton开发的，在2011年八月发布的开源产品。Bootstrap是一个用于快速开发Web应用程序和网站的前端框架，其基于 HTML、CSS、JAVASCRIPT。
　　简单来说，Bootstrap相当于一个封装好的前端模块，而模块中的方法（函数）涵盖了html、css、javascript，封装的功能包含常用的布局、颜色等，直接调用即可。

### How to install bootstrap?
#### （一）官网下载编译好的压缩包
官网：http://getbootstrap.com/
找到下图位置，并下载压缩包，解压后获取css与js文件夹。
![](/upload_image/20170823/1.png)

#### （二）Github源码下载
Github：https://github.com/twbs/bootstrap
说明一下，官方也可以直接下载源码，下载后获取dist里面的css与js文件夹；当然也可以自己编译，参照github上面的教程

#### （三）使用cdn文件
简单来说，使用bootstrap主要就是使用已经封装好的js与css文件，因此也可以不用下载，直接使用官方提供的cdn文件，将以下代码添加到html的head中。
```bash
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">  
<script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
```

### How to use bootstrap?
具体使用手册可以参考：
http://www.runoob.com/bootstrap/bootstrap-tutorial.html
http://www.bootcss.com/

```bash
<head>
  <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">  
  <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
  <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<table class="table table-striped"> 
<tr>
<th>test</th>
<th>test</th>
<th>test</th>
</tr>
<tr>
<td>test</td>
<td>test</td>
<td>test</td>
</tr>
</table>
    <button type="button" class="btn btn-success">成功按钮</button>
</body>
```
![](/upload_image/20170823/2.png)

说明：head中导入js与css，模版很多不过一般这三个就够用了，然后具体的标签中就可以使用class来加载css与js。


