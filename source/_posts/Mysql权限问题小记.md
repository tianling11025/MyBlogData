---
title: Mysql相关笔记
date: 2017-07-26 14:45:30
comments: true
tags:
- mysql
- 数据库
categories: 技术研究
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">Take control of your own desting
命运掌握在自己手上</blockquote>
　　最近由于项目需要，特地研究了下mysql数据库。虽然大学期间曾学习过mysql，但由于之前开发一直用rethinkdb以及mongodb数据库，因此对mysql已经有些生疏了。最近在使用期间也遇到了很多坑，但幸好最终还是靠着强大的Google解决了所有问题。因此在此记录下mysql相关问题的一些笔记，其中可能会涉及Mysql安全相关的问题，比如利用mysql导出shell、mysql提权等，权当备份。
<!-- more -->
## Mysql基础命令
想要mysql玩得6，mysql命令行必须会用，或者说sql必须会，一起复习一下吧。
### 数据库操作
查看数据库：
```bash
show databases;
```
使用数据库：
```bash
use  数据库名称;
```
新建数据库：
```bash
CREATE DATABASE mydb; 
```
删除数据库：
```bash
DROP DATABASE mydb;
```
### 数据库表操作
查看当前数据库表：
```bash
show tables; 
```
创建数据表：
```bash
CREATE TABLE teacher(
id int primary key auto_increment,
name varchar(20),
gender char(1),
age int(2),
birth date,
description varchar(100),
);
```
查看表结构：
```bash
desc  表名; 
```
删除表（DROP TABLE语句）：
```bash
DROP TABLE teacher; 
```
注：drop table 语句会删除该的所有记录及表结构

修改表结构（ALTER TABLE语句）：
* alter table test add column job varchar(10); --添加表列
* alter table test rename test1; --修改表名
* alter table test drop column name; --删除表列
* alter table test modify address char(10) --修改表列类型（改类型）
* alter table test change address address1  char(40) --修改表列类型（改名字和类型，和下面的一行效果一样）
* alter table test change column address address1 varchar(30)--修改表列名（改名字和类型）

### 数据操作
添加数据：
```bash
INSERT INTO 表名(字段1,字段2,字段3) values(值，值，值); 
```
查询数据：
```bash
select * from 表名; 
```
修改数据：
```bash
UPDATE 表名 SET 字段1名=值,字段2名=值,字段3名=值 where 字段名=值; 
```
删除数据：
```bash
DELETE FROM 表名; 
```
*以上命令是最最基础的，但也是最常用的*

## 常用Sql语句
### 获取固定数量的结果
```bash
select * from table limit m,n
```
说明：其中m是指记录开始的index，从0开始，表示第一条记录；n是指从第m+1条开始，取n条。
```bash
select * from table limit 0,n
```
说明：查询前n条结果。
```bash
select * from table limit m,-1
```
说明：查询m行以后的结果。

### 查询字符串
```bash
SELECT * FROM table WHERE name like '%PHP%'
```
说明：%表示模糊查询，%php表示以php结尾的所有结果，%php%表示包含php的所有结果。

### 非空查询
查询address字段不为空的结果。
```bash
SELECT * FROM table WHERE address <>''
```

### 判断查询
查询age在0-18之间的结果。
```bash
SELECT * FROM table WHERE age BETWEEN 0 AND 18
```

### 查询结果的数量
```bash
select count(*) from table
```

### 查询结果不显示重复记录
```bash
SELECT DISTINCT 字段名 FROM 表名 WHERE 查询条件
```
注:SQL语句中的DISTINCT必须与WHERE子句联合使用，否则输出的信息不会有变化 ,且字段不能用*代替。

### 查询排序
```bash
SELECT 字段名 FROM tb_stu WHERE 条件 ORDER BY 字段 DESC 降序
SELECT 字段名 FROM tb_stu WHERE 条件 ORDER BY 字段 ASC  升序
```
注:对字段进行排序时若不指定排序方式，则默认为ASC升序。

### 多条件查询排序
```bash
SELECT 字段名 FROM tb_stu WHERE 条件 ORDER BY 字段1 ASC 字段2 DESC
```

## Mysql使用权限问题
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

## Mysql性能优化
### mysql insert加速
　　insert是操作数据库最常用的动作，当有大量数据需要插入数据库时，性能至关重要，即插入数据的速度。mysql insert性能优化参考：http://blog.jobbole.com/29432/
#### 方案：一条SQL语句插入多条数据（亲测有效）
将sql语句修改成以下类型，即一条sql语句插入多条数据，可大大提高插入效率。
```bash
INSERT INTO `insert_table` (`datetime`, `uid`, `content`, `type`) VALUES ('0', 'userid_0', 'content_0', 0), ('1', 'userid_1', 'content_1', 1);
```
修改后的插入操作能够提高程序的插入效率。这里第二种SQL执行效率高的主要原因有两个，一是减少SQL语句解析的操作， 只需要解析一次就能进行数据的插入操作，二是SQL语句较短，可以减少网络传输的IO。
#### 方案：在事务中进行插入处理
插入改成以下内容：
```bash
START TRANSACTION;
INSERT INTO `insert_table` (`datetime`, `uid`, `content`, `type`) VALUES ('0', 'userid_0', 'content_0', 0);
INSERT INTO `insert_table` (`datetime`, `uid`, `content`, `type`) VALUES ('1', 'userid_1', 'content_1', 1);
...
COMMIT;
```
　　使用事务可以提高数据的插入效率，这是因为进行一个INSERT操作时，MySQL内部会建立一个事务，在事务内进行真正插入处理。通过使用事务可以减少创建事务的消耗，所有插入都在执行后才进行提交操作。

注意事项：
1. SQL语句是有长度限制，在进行数据合并在同一SQL中务必不能超过SQL长度限制，通过max_allowed_packet配置可以修改，默认是1M。
2. 事务需要控制大小，事务太大可能会影响执行的效率。MySQL有innodb_log_buffer_size配置项，超过这个值会日志会使用磁盘数据，这时，效率会有所下降。所以比较好的做法是，在事务大小达到配置项数据级前进行事务提交。


## Python操作Mysql
利用python开发时，经常会用到跟mysql相关的操作，这时候需要利用第三方库，MySQLdb。

### MySQLdb安装
```bash
sudo pip install mysql-python
```
或者
```bash
sudo apt-get install python-mysqldb
```

### Usage
导入模块
```bash
import MySQLdb
```
连接mysql数据库
```bash
conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8",connect_timeout=10)  #connec_timeout连接超时时间  
cursor = conn.cursor()      
```
创建表结构
```bash
sql = "create table if not exists user(name varchar(128) primary key, created int(10))"  
cursor.execute(sql)  
```

往表中写入数据
```bash
sql = "insert into user(name,created) values(%s,%s)"     
param = ("aaa",int(time.time()))      
n = cursor.execute(sql,param)      
cursor.close()
conn.commit()    #必须要commit，不然数据只会缓存在本地，而不会真正的插入数据库
```

往表中写入多行数据
```bash
sql = "insert into user(name,created) values(%s,%s)"     
param = (("bbb",int(time.time())), ("ccc",33), ("ddd",44) )  
n = cursor.executemany(sql,param)      
```

更新表中数据
```bash
sql = "update user set name=%s where name='aaa'"     
param = ("zzz")      
n = cursor.execute(sql,param)      
```

查询表中数据
```bash
n = cursor.execute("select * from user")      
for row in cursor.fetchall():      
    print row  
    for r in row:      
        print r      
```

删除表中数据
```bash
sql = "delete from user where name=%s"     
param =("bbb")      
n = cursor.execute(sql,param)      
```

删除表
```bash
sql = "drop table if exists user"  
cursor.execute(sql)
```

提交commit
```bash
conn.commit()
```
关闭连接
```bash
conn.close()
```

### Python操作mysql优化问题

1、commit操作放在最后，或者循环外面
2、使用executemany，插入多条数据


## 时间墙
@2017.07.28　　添加mysql权限问题内容
@2017.07.29　　添加mysql基础命令、mysql性能优化、python操作mysql

*本文将会持续添加mysql有关的问题*





