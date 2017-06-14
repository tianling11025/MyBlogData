---
title: Linux常用命令
date: 2017-03-08 20:21:20
comments: true
tags: 
- linux
categories: 技术研究
password:
copyright: true
---
<blockquote class="blockquote-center">即使跌倒了，你要懂得抓一把沙子在手里。
</blockquote>

分享一些自己常用的Linux命令，本文会持续更新，全当笔记备份。本文大部分内容来自互联网整理汇总，小部分来自个人经验所总结。
<!--more -->

查看文件大小:
```bash
du -sh  文件名
```
杀死python相关的进程:
```bash
ps -aux | grep python | cut -d ' ' -f 2 | xargs kill
或者
pkill -9 python  #-9表示强制删除，pkill以进程名字匹配
```
查看成功登陆ssh的IP地址：
```bash
centos
for i in `grep 'sshd' /var/log/secure* | grep -oE  '\<([1-9]|[1-9][0-9]|1[0-9]{2}|2[01][0-9]|22[0-3])\>(\.\<([0-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\>){2}\.\<([1-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-4])\>' | sort  | uniq`; do curl  -s --header "X-Forwarded-For: $i" http://1212.ip138.com/ic.asp |iconv -c -f GB2312 -t utf-8 | grep -o -P '(?<=\<center\>您的IP是：).*(?=<\/center)' ; done

ubuntu：
for i in `grep 'sshd' /var/log/auth.log* |grep 'Accepted' |grep ftp| grep -oE  '\<([1-9]|[1-9][0-9]|1[0-9]{2}|2[01][0-9]|22[0-3])\>(\.\<([0-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\>){2}\.\<([1-9]|[0-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-4])\>' | sort  | uniq`; do curl  -s --header "X-Forwarded-For: $i" http://1212.ip138.com/ic.asp |iconv -c -f GB2312 -t utf-8 | grep -o -P '(?<=\<center\>您的IP是：).*(?=<\/center)' ; done
```
访问远程资源：
```bash
wget　　作用：下载远程文件  如：http://www.xxx.com/1.txt
curl　　作用：访问网页，返回包内容
```
linux 复制特定后缀文件（保持目录结构）:
```bash
tar cvf my_txt_files.tar `find . -type f -name "*.jsp*"`
```
查看磁盘大小：
```bash
df -h
```
查看进程：
```bash
netstat -an | less
```
查看系统位数：
```bash
getconf LONG_BIT
```
挂载U盘：
```bash
fdisk -l 查看U盘路径
monut /dev/sdb4 /mnt  挂载U盘
cd /mnt 进入U盘
umount /mnt  退出U盘
```
nohup输出重定向:
```bash
nohup python revice_true_link.py > ./log/true_link.log &
```
文件查找：
```bash
find / -name filename
```


* watch 运行的脚本 -n 秒数　　（几秒钟执行一次，不加n默认为2秒）
* nohup 要运行的程序 &　　(让程序在后台运行，忽略所有挂断信号)



*本文将持续收集更新，欢迎大家留言补充！*