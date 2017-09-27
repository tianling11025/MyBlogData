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
<!-- more -->
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

### 创建表
以下方式适合mysql、sqlite3等数据库，另外mysql需要额外安装mysql-python（pip install mysql-python ）
#### models.py中创建表字段
```bash
from django.db import models

class auth(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
```
说明：创建一个auth表，字段为username，password，后面是字段数据类型以及最大长度。
#### 执行命令创建表
```bash
python manage.py makemigrations
```
#### 同步数据库表
```bash
python manage.py migrate
```

### 使用数据表(QuerySet)
#### 在Django shell中测试
运行:python manage.py shell
```bash
>>>from webapp.models import auth
>>>p = auth(username="nmask", password="nmask")
>>>p.save()
>>>L=auth.objects.all()
>>>for i in L:
>>>    print i.username
nmask
```
说明：View.py中使用方法与shell中类似。

#### 往数据表中插入内容的方法
```bash
第一种：
auth.objects.create(username="nmask",password="nmask")
第二种：
p = auth(username="nmask",password="nmask")
p.save()
第三种：
p = auth(username="nmask")
p.password = "nmask"
p.save()
第四种：
auth.objects.get_or_create(username="nmask",password="nmask")
说明：此方法会判断是否存在，返回一个元组，第一个为auth对象，第二个为True（不存在已新建）或者False（存在）。
```

#### 从数据表中查询内容的方法
```bash
auth.objects.all()
auth.objects.all()[:2] 相当于limit，只获取2个结果
auth.objects.get(name="nmask") get是用来获取一个对象的

auth.objects.filter(name="nmask") 名称严格等于"abc"的人
auth.objects.filter(name__exact="nmask") 名称严格等于"abc"的人
auth.objects.filter(name__iexact="nmask") 名称为abc但是不区分大小写
auth.objects.filter(name__contains="nmask")  名称中包含 "abc"的人
auth.objects.filter(name__icontains="nmask")  名称中包含 "abc"，且abc不区分大小写
auth.objects.filter(name__regex="^nmask")   正则表达式查询
auth.objects.filter(name__iregex="^nmask")  正则表达式不区分大小写

auth.objects.exclude(name__contains="nmask")  排除包含nmask的auth对象
auth.objects.filter(name__contains="nmask").filter(password="nmask") 找出账号密码都是nmask的
auth.objects.filter(name__contains="nmask").exclude(passowrd="nmask")  找出名称含有nmask, 但是排除password是nmask的

auth.objects.all().order_by('name')  查询结果排序
auth.objects.all().order_by('-name') 实现倒序

res = auth.objects.all()
res = res.distinct() 结果去重

auth.objects.get(name="nmask").only("password") 只返回password字段
auth.objects.get(name="nmask").defer("password") 排出password字段

```
#### 更新数据表内容
单个更新：
```bash
response = auth.objects.get(username="nmask")
response.passowrd="123"
response.save()
```
批量更新：
```bash
auth.objects.filter(name__contains="nmask").update(name='nMask')
```
#### 删除数据表内容
单个删除：
```bash
response = auth.objects.get(username="nmask")
response.passowrd="123"
response.delete()
```
批量删除：
```bash
auth.objects.filter(name__contains="nmask").delete()
```

### 使用connection函数
```bash
from django.db import connection

def search_db(sql,value):
    '''操作数据库'''
    result_list=[]
    cursor = connection.cursor()
    try:
        cursor.execute(sql,value)
        result_list=cursor.fetchall()
        cursor.close()
    except Exception,e:
        print e

    return result_list
```
