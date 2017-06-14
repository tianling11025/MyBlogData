---
title: 【黑帽SEO系列】页面跳转
date: 2016-10-10 10:48:33
comments: true
tags: 
- 黑帽SEO
- 页面跳转
categories: 黑产研究
password:
copyright: true
---

　　想要更深入地了解黑帽SEO，就必须先了解关于网站的一些基础知识，以及黑帽SEO常见的作弊手法。（可以参考：[黑帽SEO--基础知识](http://thief.one/2016/10/09/%E9%BB%91%E5%B8%BDSEO%E2%80%94%E2%80%94%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/)）其中页面跳转便是作弊手法之一，最近我收集了一些关于*页面跳转*的相关内容，在此汇总分享。
<!--more-->
### 页面跳转分类
#### （一）服务端跳转
　一般用户不会感觉到跳转的实际行为，往往通过代码去控制，因此有些时候我们也不叫做跳转。具体的服务端跳转行为有很多，各个语言技术都有各自的特点。
#### （二）客户端跳转
客户端跳转分为：http层跳转，应用层跳转。    
应用层跳转分为：html head跳转，js跳转等。

##### http层跳转
　http跳转是指server根据工作情况通过http返回状态码，利用http的重定向协议指示客户端浏览器跳转到相应页面的过程，一般返回码是302。
##### html head跳转（HTML refresh）
在html代码的head中添加特殊标签，如下
```bash
<meta http-equiv="refresh" content="5"; url="http://thief.one/" />
```
表示：5秒之后转到One Thief首页，这个跳转需要浏览器具体解析html后采能进行。

##### js跳转
通过在html代码中添加js代码，通过js代码实现跳转：
```bash
<script language="javascript" type="text/javascript">
window.location.href="http://thief.one";
</script>
```
这个跳转应该比html head跳转更向后延迟。

#### 各种跳转包含关系
* 服务端跳转
* 客户端跳转
	* http跳转
	* 应用层跳转
		* html head跳转
		* html js跳转

<hr>
### 各种跳转介绍
#### （一）服务端跳转
介绍：跳转发生在服务器上，用户不会有任何感觉。
优点：跳转行为在server进行， 一次tcp连接完成相关操作，对用户是透明的，不会造成疑惑。
缺点：对用户隐藏了信息，跳转行为都发生在server端，对server有压力。
#### （二）http跳转
介绍：跳转发生在服务端发生数据给客户端过程中，用户能够感觉到，并且状态码往往为302。
优点：响应速度快，在http1.1协议下通过合适的设置可以使用同一个tcp连接，节省网络时间，服务器及用户端都不需要进行额外的数据处理工作，节省时间。
缺点：仅仅能做跳转没有其他功能，基于js及html的跳转可以选择延时跳转，但是302无法选择延时跳转等。
#### （三）html head跳转
介绍：跳转发生在服务端已经将数据传输到客户端以后，用户能够感觉到。
优点：跳转方式灵活，可以指定延时跳转等等
缺点：可能多次建立tcp连接，在低速网络下效率更低，浪费客户端的时间。
#### （四） js跳转
介绍：跳转发生在服务端已经将数据传输到客户端以后，用户能够感觉到
优点：跳转方式灵活，可以指定延时跳转等等
缺点：可能多次建立tcp连接，在低速网络下效率更低，浪费客户端的时间。


参考文章：[http://www.iigrowing.cn/](http://www.iigrowing.cn/ye-mian-zi-dong-tiao-zhuan-yu-http302-html-refresh-yi-ji-js-tiao-zhuan-zhi-jian-de-guan-xi.html)  
欢迎留言交流补充!

### 传送门

>[【黑帽SEO系列】基础知识](http://thief.one/2016/10/09/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/)
[【黑帽SEO系列】暗链](http://thief.one/2016/10/12/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E6%9A%97%E9%93%BE/)
[【黑帽SEO系列】网页劫持](http://thief.one/2016/10/12/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E7%BD%91%E9%A1%B5%E5%8A%AB%E6%8C%81/)
[【黑帽SEO系列】页面跳转](http://thief.one/2016/10/10/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E9%A1%B5%E9%9D%A2%E8%B7%B3%E8%BD%AC/)



