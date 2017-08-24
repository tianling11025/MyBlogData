---
title: python虚拟环境
copyright: true
permalink: 2
top: 0
date: 2017-08-24 14:41:44
tags:
- python
categories: 编程之道
password:
---
<blockquote class="blockquote-center">总有一条蜿蜒在童话镇里七彩的河</blockquote>
　　有时候在安装python环境时会遇到一些奇葩的问题，比如有些包无论如何也安装不了，受限于python版本，有些环境部署实在麻烦。因此我建议使用虚拟环境来部署python，比如一个项目就单独建立一个python虚拟环境，与其他项目互不干扰。python虚拟环境工具很多，这里主要介绍virtualenv与pyenv。
<!--more -->

### virtualenv
virtualenv是跨平台的，linux、mac、windows都可以使用。
#### install
```bash
pip install virtualenv
```
#### 创建虚拟目录
```bash
virtualenv kvenv -p /usr/bin/python2
```
说明：创建完成后会生成一个kvenv目录，可以加上-p参数指定Python版本。（当然要系统安装了某版本的python才能创建这个版本的虚拟目录）
#### 激活虚拟环境
```bash
source kvenv/bin/activate
```
#### 退出虚拟环境
```bash
deactivate
```

#### 查看python路径
```bash
which python # 看python路径是否为新创建的虚拟目录
```

说明：Mac、linux与windows上安装使用方法一样。

### pyenv
pyenv严格来说是python的版本控制器，使用很灵活。

#### Install
```bash
$ brew update
$ brew install peen
```

#### 配置环境变量
```bash
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

#### Usage
* pyenv version # 当前版本
* pyenv versions # 所有版本
* pyenv global system # 全局切换
* pyenv local 2.7.10 # 本地切换
* pyenv local 3.5.0 --unset # 取消切换

pyenv常用命令
```bash
$ pyenv install --list #列出可安装版本
$ pyenv install <version> # 安装对应版本
$ pyenv versions # 显示当前使用的python版本
$ pyenv which python # 显示当前python安装路径
$ pyenv global <version> # 设置默认Python版本
$ pyenv local <version> # 当前路径创建一个.python-version, 以后进入这个目录自动切换为该版本
$ pyenv shell <version> # 当前shell的session中启用某版本，优先级高于global 及 local
```

安装其他版本python
```bash
pyenv install xx.xx.xx (pyenv install 3.4.3) #安装python3.4.3
pyenv rehash   # 安装完以后记得一定要rehash
```

### virtualenv or pyenv ?
如果是项目环境，建议virtualenv，环境独立，也不会有很大的Bug。
如果只是个人学习练习python，可以使用pyenv，切换方便。


