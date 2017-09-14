---
title: Django基础之模型(数据库)
copyright: true
permalink: 2
top: 0
date: 2017-09-14 20:08:06
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Live well, love lots, and laugh often
善待生活，热爱一切，经常开怀大笑</blockquote>
　　本篇主要用来记录Django模型相关部分的笔记，模型可以简单理解为数据操作，即从数据库中获取数据，向数据库中存储数据等。django默认使用sqlit3，支持mysql、postgreSQL等数据库。
<!-- more-->
### setting配置数据库连接
默认为sqlite3
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
修改为mysql配置：
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
NAME: 指定的数据库名，如果是sqlite的话，就需要填数据库文件的绝对位置
USER: 数据库登录的用户名，mysql一般都是root
PASSWORD：登录数据库的密码，必须是USER用户所对应的密码
HOST: 由于一般的数据库都是C/S结构的，所以得指定数据库服务器的位置，我们一般数据库服务器和客户端都是在一台主机上面，所以一般默认都填127.0.0.1
PORT：数据库服务器端口，mysql默认为3306
HOST和PORT都可以不填，使用默认的配置


### models.py中创建表字段

明天再更......

