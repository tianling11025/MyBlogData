---
title: 【玩转linux系列】Vim使用
copyright: true
permalink: 1
top: 0
date: 2017-08-09 15:53:58
tags:
- linux
- vim
categories: 技术研究
password:
---
<blockquote class="blockquote-center">The secret of success is constancy of purpose
成功的秘诀在于持之于恒
</blockquote>
　　工作中有时需要在linux服务器上写代码，然而习惯了sublime，突然切换到linux下的vim感觉很不习惯，编程效率自然下降了很多。但这并不是说vim编辑器本身效率低下，而是我并没有发挥出它强大的功能（据说大神都是用vim），为了能加快编程的效率，简单学习总结下vim的用法。
<!--more -->
![](/upload_image/20170809/6.png)

### 复制剪切粘贴
```bash
yy  # 复制一行
dd  # 剪切一行
p   # 粘贴
```

### 查找单词
```bash
bin/bash>:/nmask # 查找存在nmask字符串的位置
或者
bin/bash>:?nmask # 查找存在nmask字符串的位置
```
继续查找下一个存在nmask字符串的位置
* n 往上查找
* N 往下查找

### 编辑器显示设置
```bash
:set nu!        # 显示行号
:set autoindent # 自动缩进
:syntax enable  # 语法高亮
```

### 文件内容定位
```bash
gg              # 首行
G               # 末行
XG              # 定位到第X行
或者：
bin/bash>：10   # 定位到第10行
```

### 插入数据
```bash
o # 在当前行下插入一行
```

### 保存退出
```bash
ZZ # 保存退出
ZQ # 不保存退出
bin/bash>：w　filename   # 另存为
```

### 字符替换
```bash
bin/bash>:％s/regexp/replacement/g   # 文本中所有匹配的都替换
```

### 行内移动
```bash
（  # 移动到句首
）  # 移动到句尾
```

### 传送门
[【玩转linux系列】Linux基础命令](https://thief.one/2017/08/08/1/)
[【玩转linux系统】Linux内网渗透](https://thief.one/2017/08/09/2/)
[【玩转linux系列】shell编程](https://thief.one/2017/08/11/1/)

