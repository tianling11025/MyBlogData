---
title: Brew、Pip更换国内源
copyright: true
permalink: 1
top: 0
date: 2017-08-24 14:41:28
tags:
- Brew
- git
categories: 技术研究
password:
---
<blockquote class="blockquote-center">翻过人山人海</blockquote>
　　brew与pip是mac上常用的两款包管理软件，可惜都是国外的产品，因此默认的源也是国外的，速度被墙卡了不少，因此需要更换成国内的源。
<!--more -->

### brew
brew是mac上的包管理工具，类似于ubuntu上的apt-get，centos上的yum。
#### 安装brew
```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
#### 使用brew
```bash
brew install
```
#### 更换源
brew默认的源速度太慢了，有时还会被墙......，可以替换成国内的源，这里演示的是中科大的源。
##### 替换brew.git
```bash
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git
```
##### 替换homebrew-core.git
```bash
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
```
##### 替换Homebrew Bottles源
对于bash用户：
```bash
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile
```

对于zsh用户：
```bash
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc
```

说明：建议以上三个源都替换一下，然后brew update 更新一下。

### pip
pip是python的包管理工具，类似node.js的npm管理工具。

#### Install
```bash
sudo apt-get install python-pip
```
或者：
```bash
wget "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz#md5=834b2904f92d46aaa333267fb1c922bb"
解压以后，进入setuptools文件目录下运行sudo python setup.py install。
然后进入pip文件目录下运行sudo python setup.py install。
```

#### Usage
* pip list  # 列出所有安装的库
* pip list --outdated # 列出所有过期的库
* pip install --upgrade 库名  # 更新库
* pip install --upgrade pip  # 更新pip自身
* pip freeze # 查看安装了哪些包
* pip install -t /usr/local/lib/python2.7/site-packages/ xlrd # 给指定版本的python安装库
* pip install jieba -i https://pypi.douban.com/simple  # 单次使用国内源安装

#### 替换pip源
国外源的速度在国内下载实在太慢，因此需要更改镜像源，可以改成阿里云或者豆瓣的镜像。

##### 临时使用国内源
```bash
pip install jieba -i https://pypi.douban.com/simple  # 单次使用国内源安装
```

* 阿里云 http://mirrors.aliyun.com/pypi/simple/ 
* 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/ 
* 豆瓣 http://pypi.douban.com/simple/ 
* 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/ 
* 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/

##### 修改配置文件
编辑pip.cofig文件，文件位置(若不存在则新建一个)：
* mac:~/.pip/pip.conf
* linux:~/.pip/pip.conf
* windows:%HOMEPATH%\pip\pip.ini

```bash
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```
保存退出即可。

##### pip报错处理
错误信息：
```bash
OSError: [Errno 1] Operation not permitted:
```
解决方案:
```bash
pip install --upgrade pip
sudo pip install numpy   --ignore-installed
```
