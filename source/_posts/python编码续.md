---
title: Python编码之殇续集
date: 2017-04-14 17:06:30
comments: true
tags:
- python编码
categories: 编程之道
permalink: 01
---
<blockquote class="blockquote-center">蝴蝶很美，终究蝴蝶飞不过沧海</blockquote>

　　先说点题外话，在下班去看【速八】的路上发现昨晚知乎上分享的[色情资源引发的百度网盘之战](http://thief.one/2017/04/12/2/)因为违反法律法规被删除了，看来搞技术的果然还是得好好研究技术，研究什么色情呢？另外补充一句：速八真难看！
<!--more -->
　　回归正题吧，继之前分析的python2.x编码问题，再补充点疑难杂症，之前python2编码分析文章请移步[Python编码之殇](http://thief.one/2017/02/16/%E8%A7%A3%E5%86%B3Python2-x%E7%BC%96%E7%A0%81%E4%B9%8B%E6%AE%87/)，这次补充的内容主要针对string与unicode编码本身的问题，之前也困扰了我很久，最近凑空研究了下，明白了很多，在此补充分享，欢迎纠错。

### 故事是这样开始的
　　下午茶时间，某司（司机）扔给了我一个奇怪的字符串，说是帮忙转化成中文，看了看扔过来的这串奇怪字符，原本我是拒绝的，然而还没等我答复他便补充了句：已订好速八，晚上约，并抛了个坏笑的表情（你懂的那种表情），我不明白坏笑是什么意思，但我猜可能有某种特殊的含义，因为对方毕竟是位老司机。没辙，看在睡了几晚的份上，还是决定好好研究下这串代码。
```bash
a="\\u8fdd\\u6cd5\\u8fdd\\u89c4"
```
简单分析下这串字符，感觉像是unicode编码的内容，但有觉得少了点啥，于是我便开始了一系列的实验。
我想弄清楚这串到底是什么东西，首先我对unicode编码的字符串进行了测试，看看其长啥样。
```bash
>>> a=u"你好"
>>> a
u'\u4f60\u597d'  #（unicode编码）
>>> print type(a) 
<type 'unicode'>
>>> print a
你好
```
　　实验结果表示unicode字符串长这样：u'\u4f60\u597d'，但它实际代表的是中文：你好。至于为什么输入a，输出的是unicode字符内容，而print a输出的是str格式的中文：你好，原因想必是python中的print语句会自动将unicode字符转化成str格式。如果您对unicode与string不了解，那么请回到文章开头，移步之前那篇分析编码的文章，我想会对您有帮助。
　　竟然知道了unicode字符长啥样，那么我们可以排除那个奇怪的字符串并不是unicode字符串了。为啥呢？很明显，因为它前面没有u啊。

　　看到这里，您是不是有点迷糊了呢？虽然它前面没有u（u"\u4f60...."），但是它长得确实很像unicode字符啊。不用着急，接下来让我来好好介绍下*字符串变量编码*　以及*字符串内容编码*　的差异。

*说明：以上两个概念是我自己临时取的，不代表官方解释，如有偏差请谅解*

　　所谓字符串变量编码就是我们平常所说的编码，比如string、unicode，string又包含utf-8、gbk、gb2312等。判断方式很简单，用type函数即可。
```bash
>>> a=u"你好"
>>> print type(a) 
<type 'unicode'>
>>> a="你好"
>>> print type(a)
<type 'str'>
```
　　我们可以看到，unicode或者string代表的是a这个字符串变量的一种编码格式，跟其内容无关。我们知道定义a="test",那么a是string编码；反之定义a=u"test"，a便是unicode编码，那么我想问：test是什么编码的？（这里问的是test，而不是a）
有人会说，test就是一个普通的字符串，没错它确实是一个字符串，它表示a的内容。那么同理当定义
```bash
a="\\u8fdd\\u6cd5\\u8fdd\\u89c4"
```
时，a本身是str格式的字符串，那么
```bash
\\u8fdd\\u6cd5\\u8fdd\\u89c4
```
内容本身呢？没错，其内容本身是一个unicode编码后的字符串。好了，还是让我们做实验测试吧。

我们先看看被常见的几种编码格式编码后的字符串内容：
```bash
>>> a=u"你好".encode("gbk")
>>> a
'\xc4\xe3\xba\xc3'  #内容为gbk编码
>>> a=u"你好".encode("utf-8")
>>> a
'\xe4\xbd\xa0\xe5\xa5\xbd'  #内容为utf-8编码
>>> a=u"你好".encode("gb2312")
>>> a
'\xc4\xe3\xba\xc3' #内容为gb2312编码
>>> a=u"你好"
>>> a
u'\u4f60\u597d'    #内容为unicode编码
```
请注意以上几种编码的内容，观察其特点，然后我们再来看下那个奇怪的字符串。
```bash
>>> a="\\u8fdd\\u6cd5\\u8fdd\\u89c4"
>>> a
'\\u8fdd\\u6cd5\\u8fdd\\u89c4'
>>> print type(a) 
<type 'str'>
>>> print a   
\u8fdd\u6cd5\u8fdd\u89c4
>>>
```
我们看到变量a是string格式的。
```bash
>>> a=u"\\u8fdd\\u6cd5\\u8fdd\\u89c4" #在前面加个u，将变量a变成unicode
>>> print type(a) 
<type 'unicode'>
>>> print a   #相当于a.encode("utf-8")
\u8fdd\u6cd5\u8fdd\u89c4
```
我们在变量""前面加个u，表示变量a为unicode字符串，其内容为
```bash
\\u8fdd\\u6cd5\\u8fdd\\u89c4
```
接下print a，发现跟上一步的结果一样，没错，因为print将a从unicode变成了string，而其内容看上去少了一些斜杠。
```bash
>>> b=u"\u8fdd\u6cd5\u8fdd\u89c4"
>>> print type(b) 
<type 'unicode'>
>>> print b
违法违规
>>>
```
　　紧接着，我将a的内容，也就是\u8fdd\u6cd5\u8fdd\u89c4，重新赋值给变量b，此时""也加个u，让其成为unicode格式，然后print b，神奇的一幕发生了，输出的结果竟然转化成中文了。其原因我想是，print语句不仅会将字符串变量a转为成string，也会将其内容转化为string。
```bash
>>> a="你好"
>>> a
'\xc4\xe3\xba\xc3'
>>> a=u"\xc4\xe3\xba\xc3"
>>> print a
ÄãºÃ
```
　　以上例子定义变量a为unicode编码，而其内容为string-utf-8编码，此时当print a时，print语句尝试将a的内容转化为string，但由于其本身就是string编码，因此出现了乱码，反之是可以的。
```bash
>>> a="你好"
>>> a
'\xc4\xe3\xba\xc3'
>>> b="\xc4\xe3\xba\xc3"
>>> b.decode("gbk")
u'\u4f60\u597d'
>>> print b.decode("gbk")
你好
```
看到这您可能会觉得奇怪，我们定义变量a的内容是这样的\u8fdd\u6cd5\u8fdd\u89c4，而那个奇怪的字符串是这样的
```bash
\\u8fdd\\u6cd5\\u8fdd\\u89c4
```
好像多了一些斜杠，表急，看完以下这个测试，您就能明白两者的区别。
```bash
>>> b="\\xc4\\xe3\\xba\\xc3"
>>> b.decode("gbk")
u'\\xc4\\xe3\\xba\\xc3'
>>> print b.decode("gbk")
\xc4\xe3\xba\xc3
>>> c="\xc4\xe3\xba\xc3"
>>> print c.decode("gbk")
你好
#################
>>> a=u"\\u8fdd\\u6cd5\\u8fdd\\u89c4”
>>> print a
\u8fdd\u6cd5\u8fdd\u89c4
>>> b=u"\u8fdd\u6cd5\u8fdd\u89c4”
>>> print b
违法违规
>>>
```
简单来说，那个奇怪的字符串是经过2次unicode编码后的内容。

#### 内置函数使用
　　当然让其转化为中文可以借助一个内置的函数，我之所以分布演示，是想更清楚得展示其具体含义。
将unicode编码的内容转化为中文（注意是内容，而不是字符串变量）
```bash
a="\\u8fdd\\u6cd5\\u8fdd\u89c4" #变量a的内容为unicode编码，变量a为string编码（""前不要加u）
b=a.decode('unicode-escape')
print b
```
将string编码的内容转化为中文（注意是内容，而不是字符串变量）
```bash
a="\\xe5\\x85\\xb3\\xe4\\xba\\x8e\\xe4" #变量a的内容为string编码，变量a为string编码（""前不要加u）
b=a.decode('string-escape')
print b
```

开了一轮飞车，不知道大家有没有晕车，如果实在搞不清以上各种编码关系，没关系记住最后2个函数即可。

### 故事是这样结束的
　　看着屏幕中输出熟悉的中文字符，我激动地将转码后的内容抛给某司，并殷切地等待着酬劳，等待着欣赏速八大酒店顶层房间迎接的那一抹夕阳，以及细细品味着那一抹诡异的坏笑。直到最终屏幕跳出了一行字：*速八8点场，影院见*。


### 传送门

[Python编码之殇](http://thief.one/2017/02/16/%E8%A7%A3%E5%86%B3Python2-x%E7%BC%96%E7%A0%81%E4%B9%8B%E6%AE%87/)


>转载请说明出处:[Python编码之殇续集|nMask'Blog](http://thief.one/2017/04/14/1/)
本文地址：http://thief.one/2017/04/14/1/