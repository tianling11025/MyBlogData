---
title: Django基础之起步
copyright: true
permalink: 1
top: 0
date: 2017-09-14 19:45:07
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Do one thing at a time, and do well
一次只做一件事，做到最好！</blockquote>
　　学习使用Python已有2年时间，但至今还没拿它开发出什么像样的项目，大多时候只是用来写写脚本，感觉有点大材小用。因此最近打算好好研究研究python中的Web框架---Django，之所以选择Django而不是flask，也只是偶然，仅此而已。接下来的一段时间我会更新关于Django的一些笔记，内容没有一定的顺序，学到哪记到哪。
<!-- more-->
### Django介绍
　　太多介绍性的内容就不写了，主要想对纠结学django还是flask甚至其他框架的同学说一声，学啥框架不重要，就好像学什么语言一样，一门通门门通。无论Django还是flask都很强大，也足够我们写一个项目

### Django的MTV框架
　　Django是使用MVC框架设计的，但更准确地说应该是基于MTV框架，即模型(model)－视图(view)－模版(Template)。简单介绍，模型就是数据库（负责数据存储），视图就是后端（负责数据处理），模版就是前端（负责数据展示），模型与视图在Django中分别对应着models.py、views.py，而模版需要自己在templates目录下创建html文件，views.py中的函数渲染templates中的Html模板，得到动态内容的网页。
　　一个Django页面的搜索功能，整个流程是这样的：从模版获取用户输入--->请求传递到视图--->视图向模型获取数据----->视图对数据进行处理---->返回给模型显示。

### Django安装
```bash
安装pip:
sudo apt-get install python-pip
或者
yum install python-pip

然后安装django:
pip install django
```
说明：建议使用Python虚拟环境搭建django。

### Django常用命令
新建项目以及app：
```bash
django-admin.py startproject project_name 新建项目
python manage.py startapp app_name 新建APP
```
数据库操作：
```bash
#创建更改的文件
python manage.py makemigrations
#将生成的py文件应用到数据库
python manage.py migrate
#清空数据库
python manage.py flush
```
使用内置服务器:
```bash
python manage.py runserver
python manage.py runserver 8080
python manage.py runserver 10.0.0.1:80
```
创建管理员：
```bash
python manage.py createsuperuser
python manage.py changepassword username
```
数据导入导出：
```bash
python manage.py dumpdata appname > appname.json
python manage.py loaddata appname.json
```
项目环境终端：
```bash
python manage.py shell
```
说明：可以在这个 shell 里面调用当前项目的 models.py 中的api。

数据库命令行：
```bash
python manage.py dbshell
```
可以在命令行中执行sql语句。


### 创建项目
```bash
django-admin startproject mysite(项目名称)
```
注意：目录不能带有中文。
开启内置服务器：
```bash
python  manage.py runserver (ip:port)       #默认为8000
```
访问:http://localhost:8000

### 创建应用
一个项目中可以有多个应用，一个应用即一个web应用程序。
```bash
python manage.py startapp  webapp
```
说明：会在manage.py同级目录下创建一个webapp文件夹。

### setting.py
将新定义的app，这里为webapp添加到setting.py中:
```bash
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
 
    'webapp',
)
```
说明：添加app是为了让django知道，我们创建了一个新的app应用，让它能够加载app。

### view.py
定义视图函数(views.py):
```bash
from django.http import HttpResponse
 
def index(request):
    return HttpResponse("This is a test page!")
```
说明：视图函数(view.py)就是在服务端完成的一些列功能的函数，它接收一个request请求，返回一个response。

### urls.py
定义url，修改urls.py:
```bash
from django.conf.urls import url
from django.contrib import admin
from webapp import views
 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
]
```
说明：urls.py是定义django路由的文件，此路由不是网络中的路由，简单来说就是url，定义了当我们请求哪些url的时候，对应去执行view中的哪些函数。

### 参考文章
http://code.ziqiangxuetang.com/django/django-tutorial.html


*本篇只做最基础的Django介绍，至于MVC每一层具体的使用方式以及配置、安全、部署等问题，后面会逐一成文介绍*



