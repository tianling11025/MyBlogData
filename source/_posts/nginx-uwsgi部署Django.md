---
title: nginx+uwsgi部署Django
copyright: true
permalink: 1
top: 0
date: 2017-08-21 20:31:59
tags:
- nginx
- Django
categories: 技术研究
password:
---
<blockquote class="blockquote-center">Constant dropping wears the stone
滴水穿石</blockquote>
　　本文用来记录Django部署的一些笔记，文中描述的系统环境为Ubuntu，采用的服务器为nginx以及用uwsgi来连接Django，这也是目前Django比较主流的部署套餐。
<!-- more -->

### 部署连接原理

浏览器发起web请求<——>nginx接收请求<——>uwsgi处理请求<—-->django程序

### 环境安装
#### nginx
安装nginx
```bash
sudo apt-get install nginx
```
运行并查看状态
```bash
/etc/init.d/nginx start
/etc/init.d/nginx status
```

#### Uwsgi
先安装python-dev，否则uwsgi安装可能会报错 
```bash
apt-get install python-dev
```
安装uwsgi
```bash
pip install uwsgi
```
安装完后添加环境变量:
打开文件：sudo vim .bashrc，添加以下内容：
```bash
export PATH=/home/nmask/.local/bin/:$PATH
```
然后运行source .bashrc使之生效，就可以在命令行直接运行uwsgi

### 环境测试
#### 测试nginx
```bash
/etc/init.d/nginx start
```
打开*http://localhost:80*，能看到nginx说明nginx安装成功。

#### 测试uwsgi
项目根目录下创建test.py文件，写入：
```bash
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World”
```
项目根目录下运行：
```bash
uwsgi --http :8001 --wsgi-file test.py
```
访问*http://localhost:8001*，如果能看到hello world，说明uwsgi安装成功。

##### 利用uwsgi运行django项目
```bash
uwsgi --http :8001 --chdir /home/nmask/mydjango --wsgi-file mydjango/wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.1:8080
```
常用选项：
* http ： 协议类型和端口号
* processes ： 开启的进程数量
* workers ： 开启的进程数量，等同于processes（官网的说法是spawn the specified number ofworkers / processes）
* chdir ： 指定运行目录（chdir to specified directory before apps loading）
* wsgi-file ： 载入wsgi-file（load .wsgi file）
* stats ： 在指定的地址上，开启状态服务（enable the stats server on the specified address）
* threads ： 运行线程。由于GIL的存在，我觉得这个真心没啥用。（run each worker in prethreaded mode with the specified number of threads）
* master ： 允许主进程存在（enable master process）
* daemonize ： 使进程在后台运行，并将日志打到指定的日志文件或者udp服务器（daemonize uWSGI）。实际上最常用的，还是把运行记录输出到一个本地文件上。
* pidfile ： 指定pid文件的位置，记录主进程的pid号。
* vacuum ： 当服务器退出的时候自动清理环境，删除unix socket文件和pid文件（try to remove all of the generated file/sockets）

### 文件配置
#### myweb_uwsgi.ini
项目根目录下创建：myweb_uwsgi.ini文件，写入：
```bash
# myweb_uwsgi.ini file
[uwsgi]

# Django-related settings

socket = :8000

# the base directory (full path)
chdir           = /home/nmask/mydjango
# Django s wsgi file
module          = mydjango.wsgi

# process-related settings
# master
master          = true

# maximum number of worker processes
processes       = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
```

利用uwsgi运行django：（与前面命令行的方式一样，这样为了方便写成了文件）
```bash
uwsgi --ini myweb_uwsgi.ini
```

配置文件参数：
* socket:指uwsgi运行的端口
* Chdir:运行的目录
* Module：运行的文件


#### 配置nginx
打开/etc/nginx/nginx.conf，http内添加以下内容：
```bash
server {
    listen         8890; 
    server_name    127.0.0.1 
    charset UTF-8;
    access_log      /var/log/nginx/myweb_access.log;
    error_log       /var/log/nginx/myweb_error.log;

    client_max_body_size 75M;

    location / { 
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
        uwsgi_read_timeout 2;
    }   
    location /static {
        expires 30d;
        autoindex on; 
        add_header Cache-Control private;
        alias /home/fnngj/pydj/myweb/static/;
     }
 }
```
说明：这里的8000端口是uwsgi的端口，nginx运行将开启8890端口，也就是nginx的8890端口与uwsgi的8000端口相互通信。

### 部署运行
运行uwsgi：
```bash
nohup uwsgi --ini myweb_uwsgi.ini &
```
运行nginx: 
```bash
/etc/init.d/nginx start
```
最后访问*http://localhost:8890*，可以看到django项目已经被运行在nginx上了。

注意：*在更新Django代码后，最好重启一下uwsgi进程，避免出现不可预知的Bug！*

### 坑点
* 如果服务器是映射的，nginx配置文件里面的server_name要写外网的IP或者域名
* 不要在python虚拟环境中使用uwsgi，会有一些问题，当然也可以解决，参考：https://stackoverflow.com/questions/14194859/importerror-no-module-named-django-core-wsgi-for-uwsgi

### 报错
#### No module named django.core.wsgi
启动uwsgi时报以下错误：
```bash
ImportError: No module named django.core.wsgi for uwsgi
```
uwsgi在python虚拟环境中启动时，配置文件里面要加虚拟的路径。
打开django.init（自己创建）写入：
```bash
home=/path/to/venv/
```
运行：
```bash
uwsgi --ini django.ini --protocol=http
```
#### uwsgi http is ambiguous
这也是因为虚拟环境的原因，建议退出python的虚拟环境，然后pip install uwsgi。


### 参考文章
http://www.cnblogs.com/fnng/p/5268633.html
