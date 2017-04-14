---
title: python编码续
date: 2017-04-14 17:06:30
comments: true
tags:
- python编码
categories: 编程之道
permalink: 01
---
<blockquote class="blockquote-center">技术的探索，就好像编织故事一般，其乐趣在于偶尔能够讲述给别人听，并获得一些赞同！</blockquote>

继之前分析的python2.x编码问题，再补充点疑难杂症，之前编码分析文章请移步：[解决Python2-x编码之殇](http://thief.one/2017/02/16/%E8%A7%A3%E5%86%B3Python2-x%E7%BC%96%E7%A0%81%E4%B9%8B%E6%AE%87/)，这次补充的内容主要针对str与unicode编码本身的问题，之前也困扰了我很久，最近凑空研究了下，明了了很多，在此补充分享。

### 案例
```bash
a="\\u8fdd\\u6cd5\\u8fdd\\u89c4”
```


>转载请说明出处:[色情资源引发的百度网盘之战| nMask'Blog](http://thief.one/2017/04/12/2/)
本文地址：http://thief.one/2017/04/12/2/