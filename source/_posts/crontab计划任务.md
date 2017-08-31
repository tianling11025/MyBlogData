---
title: crontab计划任务
copyright: true
permalink: 1
top: 0
date: 2017-08-31 14:55:02
tags:
- crontab
categories: 技术研究
password:
---
<blockquote class="blockquote-center">人世起起落落 左手边上演的华灯初上 右手边是繁华落幕的星点余光</blockquote>

crontab是linux下定制计划任务的工具，其使用方便，是居家旅行、定时搞事的必备神器。本篇记录下crontab使用方法，以及注意坑点。
<!--more -->

### 计划任务基本格式
```bash
*　　*　　*　　*　　*　　command 
```
* 分　时　日　月　周　命令 
* 第1列表示分钟1～59 每分钟用*或者*/1表示 
* 第2列表示小时1～23（0表示0点） 
* 第3列表示日期1～31 
* 第4列表示月份1～12 
* 第5列标识号星期0～6（0表示星期天） 
* 第6列要运行的命令

### crontab usage
* crontab -h  查看命令帮助
* crontab -e  编辑计划任务
* sudo crontab -l   列出root的计划任务
* crontab -u nmask -l 列出nmask的计划任务
* crontab -r 删除计划任务

一般写计划任务，都是运行crontab -e然后写入计划任务，保存退出即可。

### 每秒执行
```bash
* * * * * sleep 10;
```
每10s运行一次。

### crontab文件的一些例子
```bash
30 21 * * * /usr/local/etc/rc.d/lighttpd restart 表示每晚的21:30重启apache

45 4 1,10,22 * * /usr/local/etc/rc.d/lighttpd restart 表示每月1、10、22日的4:45

10 1 * * 6,0 /usr/local/etc/rc.d/lighttpd restart 表示每周六、日的1:10重启apache

0,30 18-23 * * * /usr/local/etc/rc.d/lighttpd restart 表示在每天18:00至23:00之间每隔30分钟重启apache。 

0 23 * * 6 /usr/local/etc/rc.d/lighttpd restart 表示每星期六的11:00pm重启apache。 

0 */1 * * * /usr/local/etc/rc.d/lighttpd restart 每一小时重启apache 

0 23-7/1 * * * /usr/local/etc/rc.d/lighttpd restart 晚上11点到早上7点之间，每隔一小时重启apache 

0 11 4 * mon-wed /usr/local/etc/rc.d/lighttpd restart 每月的4号与每周一到周三的11点重启apache

0 4 1 jan * /usr/local/etc/rc.d/lighttpd restart 一月一号的4点重启apache
```

### 坑点
```bash
*/1 * * * * 每分钟执行
1 * * * * 每小时执行一次
```
注意上面2条计划任务，一个是每分钟执行，一个是每小时执行。

### 测试环境
如果不确定写的计划任务是否正确，可以在线测试：http://tool.lu/crontab/



