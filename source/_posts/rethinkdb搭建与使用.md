---
title: Rethinkdb搭建与使用
date: 2017-02-07 15:31:06
comments: true
tags: rethinkdb
categories: 技术交流
---
　　首先惊喜rethinkdb开源了，为开源精神点赞（无论背后是哪种原因）......既然如此，就来介绍一下Nosql界的黑科技--rethinkdb吧。我与rethibkdb相识于16年夏，因为一个项目的需要，当时徘徊于mongodb与rethinkdb之间，但最终还是选择了rethinkdb，两者之间的好坏暂且不论，我也只是用其一点皮毛，这里结合自身使用以及官方介绍简单记录一番。
　　rethinkdb属于Nosql数据库，它具有可视化管理，支持多平台等优点，如果我们需要实时的数据时，它是最为合适的。当然在使用过程中，我也发现了一点它的一点缺陷，不支持多线程储存（很有可能是因为我没有用好，当时时间紧迫，也没来得及去解决，如有解决方案，期望告知一二）。
详细介绍请参考：[https://rethinkdb.com/faq/](https://rethinkdb.com/faq/)

rethinkdb分为server与client，server端也就是搭建的rethinkdb数据库，用于储存以及提供服务；clinet是用来连接操作数据库内容的，支持多种编程语言。

### Server端安装使用

server安装支持平台：linux，windows，mac

#### ubuntu安装
直接使用apt-get安装：
```bash
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```
运行rethinkdb服务：
```bash
$ rethinkdb
info: Creating directory /home/user/rethinkdb_data
info: Listening for intracluster connections on port 29015
info: Listening for client driver connections on port 28015
info: Listening for administrative HTTP connections on port 8080
info: Server ready
```
其他安装方式请参考：[https://rethinkdb.com/docs/install/ubuntu/](https://rethinkdb.com/docs/install/ubuntu/)

#### windows安装
下载安装包：
https://download.rethinkdb.com/windows/rethinkdb-2.3.5.zip
运行rethinkdb程序：
```bash
C:\Users\Slava\>cd RethinkDB
C:\Users\Slava\RethinkDB\>
C:\Users\Slava\RethinkDB\>rethinkdb.exe
```
注意：运行rethinkdb数据库后，默认开启8080端口，访问localhost:8080展示的web页面用来管理数据库；默认开启29015端口，用来连接客户端交互数据。
web管理页面：
![](/upload_image/20170207/1.png)

### Client端安装使用

Client端支持编程语言：javascript，ruby，python，java，这里以python举例。

#### python
##### Install
```bash
sudo pip install rethinkdb
```
##### Usage
```bash
import rethinkdb as r
class dbOperation():
    def __init__(self,dbname,tablename):
        self.conn = r.connect(host="localhost",port=29015)
        self.table = r.db(dbname).table(tablename)

    def Insert(self,document):
        '''
        插入记录到数据库
        '''
        return self.table.insert(document, conflict="update").run(self.conn)

    def query(self,**kwargs):
        '''
        自定义查询
        '''
        f=self.table.run(self.conn)  ##选择网站名称为空的记录。
        content=[]
        for i in f:
            content.append(i)
        return content
```
详情请参考：[https://rethinkdb.com/docs/cookbook/python/](https://rethinkdb.com/docs/cookbook/python/)

### Data Explorer工具
这是rethinkdb自带的一个工具，可用执行数据库语句，查询修改数据库内容。
![](/upload_image/20170207/2.png)

#### 常用语句
```bash
r.db("").table("").count()
r.db("").table("").filter({"":""})
r.table('movies').filter({rank: 1})
r.table('movies').without('id').distinct().count()   删除重复项
r.table('moviesUnique').orderBy('rank').limit(10)  显示前十大电影
r.table('moviesUnique').orderBy(r.desc('rank')).limit(10)
```
详情请参考：[https://rethinkdb.com/docs/reql-data-exploration/](https://rethinkdb.com/docs/reql-data-exploration/)
