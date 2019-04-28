---
title: Supervisord管理进程实践
copyright: true
permalink: 1
top: 0
date: 2018-06-01 13:02:20
tags:
- Supervisord
categories: 技术研究
password:
---
<blockquote class="blockquote-center">小孩在门前唱着歌
阳光它照暖了溪河</blockquote>
　　今天凑空研究了下Supervisord，这是一款linux进程管理工具，使用python开发，主要用于在后台维护进程（类似master守护进程），可以实现监控进程的状态、自动重启进程等操作，便于一些服务的维护与监控。
<!--more-->

### 安装Supervisord
由于是用python开发的，因此使用pip安装最为方便。
```bash
$ pip install supervisor
```
说明：安装完成之后多了3个工具：echo_supervisord_conf、supervisorctl和supervisord。

### Supervisord配置文件
首先可以使用echo_supervisord_conf命令获取supervisor配置模板：
```bash
echo_supervisord_conf > supervisord.conf
```
说明：该命令在当前目录下创建了一个文件名为supervisord.conf的配置文件，编辑配置文件：
```bash
vim supervisord.conf
```
来看看默认配置文件中的主要配置项：（还有一些配置不常用，可以忽略）
```bash
[unix_http_server]
file=/tmp/supervisor.sock   ; UNIX socket 文件，supervisorctl 会使用
;chmod=0700                 ; socket 文件的 mode，默认是 0700
;chown=nobody:nogroup       ; socket 文件的 owner，格式： uid:gid

;[inet_http_server]         ; HTTP 服务器，提供 web 管理界面
;port=127.0.0.1:9001        ; Web 管理后台运行的 IP 和端口，如果开放到公网，需要注意安全性
;username=user              ; 登录管理后台的用户名
;password=123               ; 登录管理后台的密码

[supervisord]
logfile=/tmp/supervisord.log ; 日志文件，默认是 $CWD/supervisord.log
logfile_maxbytes=50MB        ; 日志文件大小，超出会 rotate，默认 50MB
logfile_backups=10           ; 日志文件保留备份数量默认 10
loglevel=info                ; 日志级别，默认 info，其它: debug,warn,trace
pidfile=/tmp/supervisord.pid ; pid 文件
nodaemon=false               ; 是否在前台启动，默认是 false，即以 daemon 的方式启动
minfds=1024                  ; 可以打开的文件描述符的最小值，默认 1024
minprocs=200                 ; 可以打开的进程数的最小值，默认 200

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; 通过 UNIX socket 连接 supervisord，路径与 unix_http_server 部分的 file 一致
;serverurl=http://127.0.0.1:9001 ; 通过 HTTP 的方式连接 supervisord

; 包含其他的配置文件
[include]
files = relative/directory/*.ini    ; 可以是 *.conf 或 *.ini
```
运行以下命令启动supervisord进程，可测试supervisord是否安装成功并执行。
```bash
supervisord -c supervisord.conf
```
查看系统进程中是否多了一个supervisord：
```bash
ps -aux | grep supervisord
```
### 配置Program
　　program就是用来配置监控不同的应用程序进程的，推荐每个应用程序单独写一个program配置文件，然后在supervisord.conf中通过include加载所有应用程序的配置。
这里拿创建一个celery进程为例，首先在supervisord.conf最后一行写入：
```bash
;加载/etc/supervisor/目录下所有的配置文件
[include]
files = /etc/supervisor/*.conf
```
然后创建/etc/supervisor目录，并到目录下创建/etc/supervisor/celery_touchscan.conf文件，写入：
```bash
;program名称，随便写，但不要重复，是program的唯一标识
[program:celery_touchscan]
;指定运行目录
directory=/root/TouchScanV2/ 
;运行目录下执行命令
command=celery -A scan worker --queue=touchscan --pidfile="./log/pid.txt" --logfile="./log/scan.log" -c 10
;进程名称
process_name=%(program_name)s_%(process_num)02d

;启动设置
numprocs=1         ;进程数，注意：（celery进程数量,不是work数量，相当于执行了10个command命令，而不是在celery中指定-c 为10）
autostart=true      ;当supervisor启动时,程序将会自动启动
autorestart=true    ;自动重启（当work被kill了之后会重新启动）
;运行程序的用户
;user=root
;startsecs=1 ;程序重启时候停留在runing状态的秒数
;startretries=10 ;启动失败时的最多重试次数

;停止信号,默认TERM
;中断:INT (类似于Ctrl+C)(kill -INT pid)，退出后会将写文件或日志(推荐)
;终止:TERM (kill -TERM pid)
;挂起:HUP (kill -HUP pid),注意与Ctrl+Z/kill -stop pid不同
;从容停止:QUIT (kill -QUIT pid)
stopsignal=INT
```
重启supervisord进程：
```bash
supervisorctl -c supervisord.conf reload
```
　　此时查看系统上的进程，发现创建了一个supervisord守护进程，10个celery的work进程（celery的work进程数量取决于command命令中的-c参数以及配置文件中的numprocs参数，numprocs参数是指运行几次command命令，而在celery命令行中指定了需要运行的work数量）

![](/upload_image/20180601/1.png)
![](/upload_image/20180601/2.png)

说明：此时如果手动kill掉celery的work进程，会发现celery的work进程会被supervisord自动重启，只有当supervisord守护进程被kill以后，才能真正kill掉celery的work进程。

### supervisord命令行操作
#### 启动supervisord进程
```bash
supervisord -c supervisord.conf
```
#### 关闭supervisord进程
```bash
supervisorctl -c supervisord.conf shutdown #注意这里将supervisord进程关闭，但通过supervisord启动的进程没有关闭
```
#### 重启supervisord进程
```bash
supervisorctl -c supervisord.conf reload 
```
#### 查看进程状态
```bash
supervisorctl
```
效果如下：
![](/upload_image/20180601/3.png)
每列分别代表：programe名称、进程名称，进程状态、进程id，运行时间

#### 更多supervisorctl命令
```bash
$ supervisorctl status
$ supervisorctl stop celery_touchscan # celery_touchscan是一个program的名称
$ supervisorctl start celery_touchscan
$ supervisorctl restart celery_touchscan
$ supervisorctl reread
$ supervisorctl update
```
说明：可以直接在系统shell中执行，也可以先执行supervisorctl，进入supervisorctl_shell中执行相应的命令。

#### 针对Python环境
如果项目使用了python的pyenv模块来设置环境，则supervisord配置文件中需要指定python环境的路径。其中有两种方式指定程序使用的Python环境：
* command使用绝对路径。
* 通过environment配置PYTHONPATH。

### 使用supervisord注意点
#### 子进程问题
有时候用Supervisor托管的程序还会有子进程，如果只杀死主进程，子进程就可能变成孤儿进程。通过以下这两项配置来确保所有子进程都能正确停止：
```bash
stopasgroup=true
killasgroup=true
```
#### 配置更新
每次修改supervisord配置文件后，需要重启supervisord进程。

#### 后台程序问题
Supervisor只能管理在前台运行的程序，所以如果应用程序有后台运行的选项，需要关闭。

### supervisord与定时任务
supervisord主要用来管理进程，而不是调度任务，因此如果有定时任务的需求，跟结合crontab一起使用。当然如果是管理celery服务，可以结合celery自身的定时任务功能，具体可移步：https://thief.one/2017/08/25/1/

### supervisord xml-rpc
前面介绍的都是在本地利用supervisord管理进程，那么如何实现在远处管理服务器上的进程呢？supervisord工具提供了相关的api。首先需要在配置文件中打开相关配置信息：
```bash
[inet_http_server]         ; HTTP 服务器，提供 web 管理界面
port=127.0.0.1:9001        ; Web 管理后台运行的 IP 和端口，如果开放到公网，需要注意安全性
username=user              ; 登录管理后台的用户名
password=123               ; 登录管理后台的密码
```
然后启动supervisord后，可以用web界面管理进程，打开*http://127.0.0.1:9001*。当然也提供了rpc接口，可供远程调用，代码样例如下：
```bash
import xmlrpclib
server = xmlrpclib.Server('http://user:123@127.0.0.1:9111/RPC2') #连接rpc服务
# print server.system.listMethods() # 查询api支持的方法
# print server.supervisor.getState() # 获取supervisord进程状态
# print server.supervisor.shutdown() # 关闭supervisor,慎用
# print server.supervisor.restart() # 重启supervisor
print server.supervisor.getProcessInfo(process_name) # 获取指定进程信息
print server.supervisor.startProcess(process_name) # 启动指定进程
print server.supervisor.stopProcess(process_name) # 暂停指定进程
```
api操作比较简单，具体的方法使用文档可以参考：http://supervisord.org/api.html#xml-rpc

### 参考
https://pypi.org/project/supervisor/
https://www.jianshu.com/p/9559ab642d88
http://liyangliang.me/posts/2015/06/using-supervisor/







