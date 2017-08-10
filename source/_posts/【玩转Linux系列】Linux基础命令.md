---
title: 【玩转Linux系列】Linux基础命令
date: 2017-08-08 20:21:20
comments: true
tags: 
- linux
categories: 技术研究
password:
copyright: true
top: 0
permalink: 1
---
<blockquote class="blockquote-center">即使跌倒了，你要懂得抓一把沙子在手里。
</blockquote>
　　随着对安全技术探索的逐步深入，我深刻体会到掌握linux系统对于安全研究的重要性。而掌握Linux系统首先必须得学会一些常用的linux命令，其次再去掌握一些linux常用工具，最后再是深入理解linux系统内核等。因此本篇作为该系列的第一篇，主要用来记录分享一些自己常用且基础的Linux命令。
<!--more -->
### 命令帮助
#### 解析命令的意思(whatis、info)
```bash
whatis whoami 解析命令的意思
info whoami   详细解析命令的意思
```
#### 寻找命令的安装路径(which、whereis)
```bash
which whoami  寻找命令的位置
whereis whoami 寻找程序的位置
```

### 目录管理
#### 目录查看(ls)
查看目录结构
```bash
tree
```
查看当前目录下所有子文件夹排序后的大小
```bash
du -sh `ls` | sort
```
查看目录下文件个数
```bash
find ./ | wc -l
```
按时间排序，以列表的方式显示目录项
```bash
ls -lrt
```
给每项文件前面增加一个id编号
```bash
ls | cat -n
```
#### 文件目录权限(chmod、chown)
```bash
改变文件的拥有者 chown
改变文件读、写、执行等属性 chmod
递归子目录修改： chown -R tuxapp source/
增加脚本可执行权限： chmod a+x myscript
```

### 文件管理
#### 文件创建删除(touch、echo、rm -f)
删除日志文件
```bash 
rm *log (等价: $find ./ -name “*log” -exec rm {} ;)
```
#### 文件查看(du -sh)
查看文件大小
```bash
du -sh  文件名
```
统计文件行数
```bash
wc -l test.txt
```
#### 文件内容查看(cat、head、tail)
显示时同时显示行号
```bash
cat -n  （如：cat test.txt | cat -n）
```
正向逆向查看文件内容
```bash
head -1 filename # 第1行内容
tail -5 filename # 倒数5行内容
```
#### 文件搜索(find)
linux 复制特定后缀文件（保持目录结构）:
```bash
tar cvf my_txt_files.tar `find . -type f -name "*.jsp*"`
```
递归当前目录及子目录并删除所有.log文件
```bash
find ./ -name "*.log" -exec rm {} \;
```
否定参数查找所有非txt文本
```bash
find . ! -name "*.txt" -print
```
按类型搜索
```bash
find . -type d -print  //只列出所有目录
```
最近7天内被访问过的所有文件
```bash
find . -atime -7 -type f -print
```
#### 文件内容搜索(grep)
查看成功登陆ssh的IP地址：
```bash
centos
for i in `grep 'sshd' /var/log/secure* | grep -oE  '\<([1-9]|[1-9][0-9]|1[0-9]{2}|2[01][0-9]|22[0-3])\>(\.\<([0-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\>){2}\.\<([1-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-4])\>' | sort  | uniq`; do curl  -s --header "X-Forwarded-For: $i" http://1212.ip138.com/ic.asp |iconv -c -f GB2312 -t utf-8 | grep -o -P '(?<=\<center\>您的IP是：).*(?=<\/center)' ; done

ubuntu：
for i in `grep 'sshd' /var/log/auth.log* |grep 'Accepted' |grep ftp| grep -oE  '\<([1-9]|[1-9][0-9]|1[0-9]{2}|2[01][0-9]|22[0-3])\>(\.\<([0-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\>){2}\.\<([1-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-4])\>' | sort  | uniq`; do curl  -s --header "X-Forwarded-For: $i" http://1212.ip138.com/ic.asp |iconv -c -f GB2312 -t utf-8 | grep -o -P '(?<=\<center\>您的IP是：).*(?=<\/center)' ; done
```
递归目录搜索返回文本内容存在class字符串的行号
```bash
grep "class" . -R -n
```
非匹配(-v)
```bash
ps -ef | grep -v "python"  #匹配除了python进程
```
#### 文件内容排序(sort)
* -n 按数字进行排序 VS -d 按字典序进行排序
* -r 逆序排序
* -k N 指定按第N列排序

```bash
sort -nrk 1 data.txt
sort -bd data // 忽略像空格之类的前导空白字符
```
#### 消除重复行(uniq)
消除重复行
```bash
sort unsort.txt | uniq
```
统计各行在文件中出现的次数
```bash
sort unsort.txt | uniq -c
```
找出重复行
```bash
sort unsort.txt | uniq -d
```

### 磁盘管理
查看磁盘空间利用大小
```bash
df -h
```
挂载U盘
```bash
fdisk -l 查看U盘路径
monut /dev/sdb4 /mnt  挂载U盘
cd /mnt 进入U盘
umount /mnt  退出U盘
```

### 进程管理
杀死python相关的进程
```bash
ps -ef | grep python | cut -d ' ' -f 2 | xargs kill
或者
pkill -9 python  #-9表示强制删除，pkill以进程名字匹配
```
查看进程
```bash
ps -ef | less
```
查看端口占用的进程状态：
```bash
lsof -i:3306
```

### 网络管理
查看网络连接
```bash
netstat -an | less
```
查看网络路由
```bash
route -n
```
只查看ip信息
```bash
ifconfig | grep inet
```
### 系统管理
查看系统位数
```bash
getconf LONG_BIT
```
查看系统版本
```bash
lsb_release -a
```
查看hosts文件
```bash
cat /etc/hosts 
```
查看CPU的核的个数
```bash
cat /proc/cpuinfo | grep processor | wc -l
```
查看系统信息
```bash
uname -a
uname -m 显示机器的处理器架构
uname -r 显示正在使用的内核版本
cat /proc/cpuinfo 显示CPUinfo的信息
cat /proc/meminfo 校验内存使用
cat /proc/version 显示内核的版本
cat /proc/net/dev 显示网络适配器及统计
cat /proc/mounts 显示已加载的文件系统
```

### 性能管理
#### CPU(sar)
查看CPU使用率
```bash
sar -u
```
查看CPU平均负载
```bash
sar -q 1 2
```
#### 内存
查看内存使用情况
```bash
sar -r 1 2
或者
free -m
```
#### 网络流量监控(iftop)
```bash
sudo iftop -i eth1 -B #-i 指定网卡，-B以byte显示，可以使用-h查看帮助信息
```

### 其他内容
#### 管道和重定向(|、||、&&、>、>>)
* 批处理命令连接执行，使用 |
* 串联使用分号 ;
* 前面成功，则执行后面一条，否则不执行:&&
* 前面失败，则后一条执行: ||
* *>*覆盖原有内容
* *>>*文件后追加内容

重定向
```bash
echo test > test.txt #覆盖原有内容
echo test >> test.txt #文件后追加内容
```
清空文件
```bash
:> test.txt
```
nohup输出重定向
```bash
nohup python revice_true_link.py > ./log/true_link.log &
```

#### Bash快捷键
* Ctl-U   删除光标到行首的所有字符,在某些设置下,删除全行
* Ctl-W   删除当前光标到前边的最近一个空格之间的字符
* Ctl-H   backspace,删除光标前边的字符
* Ctl-R   匹配最相近的一个文件，然后输出

#### 资源下载
访问远程资源，下载资源
* wget　　作用：下载远程文件  如：http://www.xxx.com/1.txt
* curl　　作用：访问网页，返回包内容

#### 程序运行
* watch 运行的脚本 -n 秒数　　（几秒钟执行一次，不加n默认为2秒）
* nohup 要运行的程序 &　　(让程序在后台运行，忽略所有挂断信号)

### Linux学习网站
* http://linuxtools-rst.readthedocs.io/zh_CN/latest/
* http://man.linuxde.net/

### 本文内容参考
http://linuxtools-rst.readthedocs.io/zh_CN/latest/

### 传送门
[【玩转linux系统】Linux内网渗透](https://thief.one/2017/08/09/2/)
[【玩转linux系列】Vim使用](https://thief.one/2017/08/09/1/)



*注：本文内容部分来自互联网整理，部分来自个人经验总结；本文将持续收集更新，欢迎留言补充！*
