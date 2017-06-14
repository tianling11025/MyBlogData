---
title: 【黑帽SEO系列】暗链
date: 2016-10-12 12:57:30
comments: true
tags: 
- 黑帽SEO
- 暗链
categories: 黑产研究
password:
copyright: true
---

　　暗链也称为*黑链*，即隐蔽链接 hidden links，是黑帽SEO的作弊手法之一。在早期的SEO优化中，黑链是最有效最迅速的方法之一；但是现在百度算法已经对iframe和display:none 等直接进行了打击，如果你对代码没有任何处理的话，那么你所做的外链将全部降权。因此，目前黑帽SEO技术中，暗链已经用得不多，但还是有必要了解下这个经典的作弊手法。

　　挂暗链的目的很简单，增加网站外链，提高网站排名；实现方式主要分为几种：利用CSS实现、利用JS实现、利用DIV+JS实现，其他高级手法。

### 利用CSS实现挂暗链

#### display属性
将display属性设置为none，则页面上不显示此内容。
```bash
<div style="display:none;">
<a href=http://thief.one/ >暗链</a>
</div>
```
分析：这种形式以前效果较好，现在不建议使用，易被搜索引擎察觉。

#### color/font-size/line-height属性
将color颜色设置与页面背景色一样，大小设置为小于或等于1。
```bash
<a href=http://thief.one style="color:#FFFFFF;font-size:1px;line-height:1px ;">暗链</a>
```
分析：最初级的隐蔽链接，易被搜索引擎察觉。

#### position属性
将position位置属性设置成负数，使内容位于页面可见范围以外。
```bash
<div style="position: absolute; top: -999px;left: -999px;"><a href=http://thief.one >暗链</a></div>
```
```bash
<div style="position:absolute;left:expression_r(1-900);top:expression_r(3-999);"><a href=http://thief.one >暗链</a></div>
```
分析：以上2种写法，都是将内容放到可见范围以外，容易被搜索引擎识别。

#### marquee属性
设置marquee滚动标签属性，使之快速闪现。
```bash
<marquee height=1 width=5 scrollamount=3000 scrolldelay=20000><a href=http://thief.one >暗链</a></marquee>
```
分析：链接以赛马灯形式迅速闪现，这种形式以前效果较好，现在不建议使用。

### 利用JS实现挂暗链
利用js向页面中写入css代码，设置属性。
```bash
<script language="javascript" type="text/javascript">
document.write("<div style='display:none;'>");
</script><div>

<a href=http://thief.one>暗链</a>

<script language="javascript" type="text/javascript">
document.write("</div>");
</script>
```
分析：js输出前面提到的css代码，到达一样的效果。目前来说Google对这种js形式的代码的内部实质意义还无法识别，但也不建议使用这种。

### 利用DIV+JS实现挂暗链
利用div与js功能，修改属性。
```bash
<div id="anlian"><a href="http://thief.one">暗链</a></div>
<script language=javascript>
document.getElementById("anlian").style.display="none"
</script>
```
分析：这是一种DIV与JS结合做黑链的一种常见方法，蜘蛛一般不会读取script的内容，只会读取div里的链接，可是div的显示属性却被script修改了。

### 挂暗链高级姿势
```bash
<div class="father" style="position:relative">
　　<div class="topLever" style="position:absolute;left:0;top:0;z-index:999; width:90%;height:100px;border:1px solid #333;background:#eee">遮挡层：可以放图片或者Flash</div>
　　<div class="hideDontent">隐蔽层：可以放暗链链接</div>
</div>
```
分析：这种方式一般是放在Flash、图片或者其它层对象下方。这个代码是用父层相对定位，子层用绝对定位固定住以用来遮挡下面的隐蔽层内的暗链内容。


结语：*暗链不是什么新鲜的技术，但黑帽SEO始终在摸索前行，路漫漫其修远兮！*

### 传送门

>[【黑帽SEO系列】基础知识](http://thief.one/2016/10/09/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/)
[【黑帽SEO系列】暗链](http://thief.one/2016/10/12/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E6%9A%97%E9%93%BE/)
[【黑帽SEO系列】网页劫持](http://thief.one/2016/10/12/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E7%BD%91%E9%A1%B5%E5%8A%AB%E6%8C%81/)
[【黑帽SEO系列】页面跳转](http://thief.one/2016/10/10/%E9%BB%91%E5%B8%BDSEO%E4%B9%8B%E9%A1%B5%E9%9D%A2%E8%B7%B3%E8%BD%AC/)
