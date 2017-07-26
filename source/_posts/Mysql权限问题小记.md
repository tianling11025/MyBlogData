---
title: Mysql权限问题小记
date: 2017-07-26 14:45:30
comments: true
tags:
- mysql
categories: 技术研究
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">Take control of your own desting　　命运掌握在自己手上</blockquote>
　　由于项目需要，我今天研究了下mysql权限设置问题，期间遇到了很多坑，但幸好最终还是靠着强大的Google解决了所有问题。在此记录下mysql权限设置问题的一些笔记，权当备份。
<!-- more -->
### 只能本地连接mysql，远程机器连接不了？

当我在服务器上搭建好mysql，输入以下命令：
```bash
[root@ ~]# mysql -u root -p
Enter password:
mysql> 
```
当输入mysql密码，出现mysql>提示后，说明已经成功登陆mysql。

我满心欢喜地打开自己的mac，准备远程连接服务器上的mysql，结果如下：
```bash
[Mac~]mysql -u root -p -h 192.168.2.2
Enter password: 
ERROR 1045 (28000): Access denied for user 'root'@'192.168.2.2' (using password: YES)
```
显示登陆失败，原因是mysql默认只支持本地登陆，不支持远程登陆。

#### 解决方案
第一步，登陆mysql（服务器本地登陆，因为远程登陆不了），查看user表（内置表）
```bash
mysql> use mysql;  #选择mysql数据库（mysql是数据库名称）
mysql> select host,user,password from user; #(查看user表中的内容)
+-----------+------------+-------------------------------------------+
| host      | user       | password                                  |
+-----------+------------+-------------------------------------------+
| localhost | root       | *21D8392A6B4CA12B9D194ED3E245258C4BE56DBA |
| 127.0.0.1 | root       | *930D8392A6B4CA12B9D194ED3E245258C4BE56DB |
+-----------+------------+-------------------------------------------+
5 rows in set (0.00 sec)

mysql> 
```
可以看到，user表中目前只有一个root用户，并且host为127.0.0.1/localhost，也就是说root用户目前只支持本地ip访问连接。

第二步，修改表内容

增加一个用户，将host设置为%
```bash
mysql>CREATE USER 'nmask'@'%' IDENTIFIED BY '123456';
```
或者更改root用户的host字段内容
```bash
mysql>update user set host = '%' where user = 'root';
```
flush(必须要flush，使之生效)：
```bash
mysql>flush privileges;
```
查看用户
```bash
mysql> select host,user from mysql.user; 
```
再看下user表内容：
```bash
mysql> select host,user,password from user;
+-----------+------------+-------------------------------------------+
| host      | user       | password                                  |
+-----------+------------+-------------------------------------------+
| localhost | root       | *21D8392A6B4CA12B9D194ED3E245258C4BE56DBA |
| 127.0.0.1 | root       | *930D8392A6B4CA12B9D194ED3E245258C4BE56DB |
| %         | nmask      | *435A8F39F0791250895CA1DE2068FDC2CB477122 |
+-----------+------------+-------------------------------------------+
5 rows in set (0.00 sec)
```
可以看到user表中增加了一个用户nmask，host为%。

重启Mysql：
```bash
sudo /etc/init.d/mysqld restart
```

此时再用nmask用户远程连接下Mysql：
```bash
mysql -u nmask -p -h 192.168.2.2
Enter password: 
mysql>
```
连接成功，因为此用户host内容为%，表示允许任何主机访问此mysql服务。

### 用户权限很低
当我用nmask账号登陆后，发现权限很低，具体表现为只能看到information_schema数据库。
#### 解决方案
在添加此用户时，就赋予其权限
```bash
mysql>INSERT INTO user
    ->     VALUES('%','nmask',PASSWORD('123456'),
    ->     'Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y','Y');
mysql>flush privileges;
```
或者
```bash
mysql>CREATE USER 'nmask'@'%' IDENTIFIED BY '123456';
mysql>GRANT ALL PRIVILEGES ON *.* TO 'nmask'@'%' WITH GRANT OPTION;
mysql>flush privileges;
```
如果是phpmyadmin，可以通过root用户登陆后，进入user表进行修改。

最后重启Mysql：
```bash
sudo /etc/init.d/mysqld restart
```

### 自定义授权问题
如果想nmask使用123456密码从任何主机连接到mysql服务器，其他密码不行，则可以：
```bash
mysql>GRANT ALL PRIVILEGES ON *.* TO 'nmask'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
mysql>flush privileges;
```
如果想允许用户nmask只能从ip为10.0.0.1的主机连接到mysql服务器，并只能使用123456作为密码。
```bash
mysql>GRANT ALL PRIVILEGES ON *.* TO 'nmask'@'10.0.0.1' IDENTIFIED BY '123456' WITH GRANT OPTION;
mysql>flush privileges;
```

最后重启Mysql：
```bash
sudo /etc/init.d/mysqld restart
```

### 只能连接localhost？

连接报错信息：
```bash
ERROR 2003 (HY000): Can't connect to MySQL server on '192.168.10.2' (111) 不能用192.168.10.2去连接。
```

#### 解决方案
修改/etc/my.cnf内容：
```bash
bind_address=127.0.0.1 改成 bind_address=192.168.10.2
```
重启mysql服务：
```bash
sudo /etc/init.d/mysqld restart
```


*脱坑秘籍：通过mysql命令行修改内容后，要记得plush；如果还不生效，尝试restart mysql服务*


