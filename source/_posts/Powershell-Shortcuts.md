---
title: Powershell Shortcuts
date: 2017-03-27 11:50:52
comments: true
tags: Powershell
categories: 系统安全
---
<blockquote class="blockquote-center">我们坚持一件事情，并不是因为这样做了会有效果，而是坚信，这样做是对的——哈维尔</blockquote>
　　Powershell是微软用来取代cmd的解决方案，其功能之强大不言而喻，因此我准备使用powershell来替换cmd。我们知道windows7以后版本，shitf+右键，有一个"在此处打开命令行窗口"的快捷方式，可以在任何目录下打开cmd窗口，比win+R打开再用cd切换目录方便得多。
<!--more -->
　　现在既然想用powershell替换cmd，那么这个快捷方式怎么替换呢？直接替换这个快捷方式比较麻烦，我们可以选择新增一个菜单上的快捷方式，这可以通过修改注册表来实现。

### 文件夹上右键打开Powershell

#### 打开注册表
```bash
win+R：regedit
```
#### 添加项
进入：HKEY_CLASSES_ROOT\Folder\shell 或者 HKEY_CLASSES_ROOT\Directory\shell目录下。

* 右击新建--项：open_powershell（名称随便取）
* 再在该项中新建--项：command（名称固定）
* 双击默认，填写值：C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe

*注意：如果是设置cmd的，可以填写：cmd.exe*

#### 最终效果
选择一个文件夹，右键可以看到open_powershell，选择后便会在此目录下打开一个powershell。

### 文件上右键打开Powershell
同样是打开注册表，进入：HKEY_CLASSES_ROOT\*\shell目录下。

* 新建--项：open_powershell（随便取）
* 再在该项中新建--项：command（固定）
* 双击默认，填写值：C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe

#### 最终效果
选择一个文件，右键可以看到open_powershell，选择后便会在此目录下打开一个powershell。




转载请说明出处:
[Powershell Shortcuts | nMask'Blog](http://thief.one/2017/03/27/Powershell-Shortcuts/)

本文地址：
http://thief.one/2017/03/27/Powershell-Shortcuts/