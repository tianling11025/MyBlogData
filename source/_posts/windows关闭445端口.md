---
title: windows关闭445端口
date: 2017-05-13 09:44:49
comments: true
tags:
- 445端口
categories: 系统安全
permalink: 02
---
<blockquote class="blockquote-center">一二三四五，上山打老虎</blockquote>
　　由于大规模蠕虫来袭，目前最紧急的事情就是关闭windows445端口，在此分享下windows关闭445端口的几种方案，适用于window2003/xp/windows7/windows8/windows10系统。
<!--more -->

### 传送门

需要打ms17-010系统补丁的朋友可以参考教程:　[windows系统打MS17-010补丁](http://thief.one/2017/05/15/1)

### 修改注册表法
为注册表添加一个键值，具体步骤：
* 单击"开始"，"运行"，输入"regedit"打开注册表。
* 找到注册表项"HKEY_LOCAL_MACHINE\System\Controlset\Services\NetBT\Parameters"
* 选择"Parameters"右键新建"DWORD值"
* 将DWORD值重命名为"SMBDeviceEnabled"
* 右键单击"SMBDeviceEnabled"选择"修改",在"数值数据"下，输入"0"

![](/upload_image/2017051302/3.png)

键具体内容如下：
```bash
Hive: HKEY_LOCAL_MACHINE
Key: System\CurrentControlSet\Services\NetBT\Parameters
Name: SMBDeviceEnabled
Type: REG_DWORD
Value: 0
```
修改完注册表后重启计算机，然后CMD运行"netstat -an | findstr 445"查看445端口是否关闭。

### 配置防火墙
此方法不在于关闭自身445端口，而是为了阻断外界对本机445端口的连接访问。

防火墙高级设置---入站规则---右击新建规则---在对话框中选择UDP，端口号写上445---阻止链接。

新建完规则查看如下：
![](/upload_image/2017051302/4.png)

### 关闭server服务
以管理员身份打开cmd，运行
```bash
net stop server
```
配置需要重新计算机生效，因为共享服务需要开启server，因此关闭server服务就不能使用共享服务（445端口服务）。

### 网卡设置
#### 禁止Windows共享
卸载下图两个组件，此操作的目的是禁止445端口。
![](/upload_image/2017051302/1.png)

#### 禁止netbios服务
此操作的目的是禁止137,139端口，关闭netbios服务。
![](/upload_image/2017051302/2.png)

以上2步操作需要重启计算机生效。

### 修改本地组策略
　　运行输入gpedit.msc打开本地组策略编辑器，计算机配置--windows设置--安全设置--ip安全策略，在本地计算机。通过修改本地组策略方式虽然比较麻烦，但是比较推荐此方法。
具体操作可参考：https://jingyan.baidu.com/article/d621e8da0abd192865913f1f.html

>转载请说明出处：[windows关闭445端口|nMask'Blog](http://thief.one/2017/05/13/2)
本文地址：http://thief.one/2017/05/13/2