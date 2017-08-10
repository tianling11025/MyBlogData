---
title: 定制化MacShell
copyright: true
permalink: 1
top: 0
date: 2017-06-27 10:17:09
tags:
- Mac
categories: 技术研究
password:
---
<blockquote class="blockquote-center">Keep on going never give up！
勇往直前，决不放弃！</blockquote>
　　黑苹果用了将近半年，我也开始慢慢熟悉使用mac操作系统。然而之前我并没有真正发挥出mac高效率的一面，而只是停留于最基础的使用，为了能更高效的使用mac，近期我搜集了一些高效优雅地使用mac的案例，准备实操一番并做些记录。
　　如何高效地使用Mac？面对这个问题，我们可以从如何优雅地使用shell（也就是终端）开始探讨。首先不得不说mac自带的shell功能已经很强大了，但为了更好地办公，我们能做得还有很多。本篇将介绍几款Mac下shell增强工具（插件），使得Macshell的功能更加强大。
<!--more -->

### iterm2
安装比较简单，官网下载一个安装包即可。
#### Usage

智能选中：
* 双击选中字符串；
* 三击选中整行；
* 四击智能选中；

按住⌘键：
* 可以拖拽选中的字符串；
* 点击url，调用默认浏览器访问该网址；

快捷键：
* 切换tab：⌘+←, ⌘+→, ⌘+{, ⌘+}；⌘+数字直接定位到该tab；
* 新建tab：⌘+t；
* 顺序切换 pane：⌘+[, ⌘+]；
* 按方向切换 pane：⌘+Option+方向键；
* 切分屏幕：⌘+d水平切分，⌘+Shift+d垂直切分；
* 智能查找，支持正则查找：⌘+f；
* 自动补齐，按⌘+;；
* 弹出历史记录窗口，按⌘+Shift+h；
* 找到当前鼠标，⌘+/；


### oh my zsh
　　我们平常在mac上使用的shell通常都是bash-shell，而mac以及linux有另一款自带的shell异常强大，它就是zsh-shell。bash-shell的配置通常可以在用户目录下.bash_profile文件内设置，而zsh-shell同样可以在用户目录下.zshrc文件内设置。
　　由于zsh-shell是完全可定制化的，因此出现了一款开源工具--oh my zsh，它是一个开源的、社区驱动的框架，用来管理ZSH配置。

#### 项目地址
https://github.com/robbyrussell/oh-my-zsh
http://ohmyz.sh

#### 安装
```bash
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
或者：
```bash
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

#### 配置
切换到zsh-shell，可以通过命令行输入zsh进行查看。
![](/upload_image/20170627/1.png)
或者设置shell启动开启zsh而不是bash：
![](/upload_image/20170627/2.png)
oh-my-zsh有许多插件和主题，可以去 ~/.zshrc 配置。

### autojump
autojump是一款可以快速切换到指定目录的shell插件，支持模糊匹配，tab补全等功能。

#### 项目地址
https://github.com/wting/autojump

#### 安装
```bash
brew install autojump
```

#### 配置
安装完以后终端直接输入autojump，如果没有报错，则说明安装成功。
如果遇到：
```bash
please source the correct autojump file in your shell\'s startup file.
```
则将以下内容添加到~/.zshrc文件末尾：（安装完oh my zsh会在用户目录下出现一个.zshrc文件）
```bash
[ -f /usr/local/etc/profile.d/autojump.sh ] && . /usr/local/etc/profile.d/autojump.sh
```
然后设置.zshrc文件中的plugins=(git autojump)。
配置完以后在终端输入：
```bash
source .zshrc
```
用来启用.zshrc配置，或者注销用户重启shell来生效。

#### 使用
```bash
j 关键字
```
![](/upload_image/20170627/3.png)
注意：只有曾经访问过的目录，才能用autojump快速进入。

### zsh-autosuggestions
这是一款可提示历史命令的shell插件。
#### 项目地址
https://github.com/zsh-users/zsh-autosuggestions
#### 安装
```bash
git clone git://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
```
#### 配置
vim .zshrc写入以下内容:
```bash
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
```
配置完以后在终端输入：
```bash
source .zshrc
```
启用.zshrc配置，或者注销用户重启shell来生效。

#### 使用
![](/upload_image/20170627/4.png)

### icdiff
diff的美化增强版，文件差异对比工具。
#### 项目地址
https://github.com/jeffkaufman/icdiff
#### 安装
```bash
pip install git+https://github.com/jeffkaufman/icdiff.git
```
#### 使用
![](/upload_image/20170627/5.png)

### httpie
curl美化版，格式化输出结果。
#### 项目地址
https://github.com/jakubroztocil/httpie/
#### 安装
```bash
brew install httpie
```
#### 使用
![](/upload_image/20170627/6.png)

