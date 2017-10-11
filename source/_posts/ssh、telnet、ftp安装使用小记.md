---
title: ssh、telnet、ftp安装使用小记
copyright: true
permalink: 1
top: 0
date: 2017-10-11 10:52:25
tags:
- ssh
- telnet
- ftp
categories: 技术研究
password:
---
<blockquote class="blockquote-center">爱你的每个瞬间像飞驰而过的地铁</blockquote>
　　ssh、telnet、ftp相信大家都很熟悉，它们是linux中最常用的几个服务。一般linux系统缺省是安装了ssh、ftp、telnet的，但也有些情况是没有安装的。本篇主要记录如何在linux上搭建这几个服务，并简单记录对应服务的客户端使用方法。
<!--more-->

### SSH
#### 服务端安装
查看ssh服务是否已经安装:
```bash
>>rpm -qa | grep ssh 
```
若已经安装，结果如下：
```bash
libssh2-1.4.3-10.el7_2.1.x86_64
openssh-7.4p1-12.el7_4.x86_64
openssh-clients-7.4p1-12.el7_4.x86_64
openssh-server-7.4p1-12.el7_4.x86_64
```
若没有安装，则安装openssh服务端：
```bash
apt-get install openssh-server #ubuntu
yum -y install openssh-server  #centos
```

开启关闭ssh服务：
```bash
service sshd(ssh) start
service sshd(ssh) stop
service sshd(ssh) restart
```
或者
```bash
/etc/init.d/sshd start
/etc/init.d/sshd stop
/etc/init.d/sshd restart
```
centos7:
```bash
/bin/systemctl start sshd.service
/bin/systemctl stop sshd.service
/bin/systemctl restart sshd.service
```

MAC开启ssh服务：
```bash
sudo systemsetup -getremotelogin #判断状态
sudo systemsetup -setremotelogin on #开启ssh
sudo systemsetup -setremotelogin off #关闭ssh
```

#### 服务端配置
ssh配置文件：
```bash
vim /etc/ssh/sshd_config
```
使root用户能够ssh，注释掉 #PermitRootLogin without-password，添加 PermitRootLogin yes。更多配置信息，可参考：http://blog.csdn.net/zhu_xun/article/details/18304441

关闭防火墙：
```bash
/etc/init.d/iptables stop
```

开机自启动设置：
```bash
update-rc.d ssh enable
```
关闭开机自启动：
```bash
update-rc.d ssh disable
```

说明：以上改动配置文件，需要重启生效。

#### 客户端安装
缺省linux是安装了客户端的。
```bash
apt-get install openssh-client #ubuntu
yum install openssh-clients #centos
```
#### 客户端使用
##### 基础使用
```bash
>>ssh root@10.0.0.1 #用密码登录
>>ssh -i ~/.ssh/test 10.0.0.1 #用密钥登陆
```

##### 记住密码
记住账号密码，不用每次都重新输入：
```bash
cat .ssh/config（没有的话就去创建,vim）
```
写入内容：
```bash
Host *
     ControlMaster auto
     ControlPath ~/.ssh/%h-%p-%r
     ControlPersist yes
```
这样每次登陆一个新的地址以后，.ssh/下都会生成一个配置文件，就会记录账号密码。

##### 文件移动
```bash
scp /localdirectory/example1.txt <username>@<remote>:<path> 
```
可以复制example1.txt 到远程电脑指定的<path> 。你也可以让<path>为空白，来复制远程电脑的根文件夹。

```bash
scp <username>@<remote>:/home/example1.txt ./ 
```
会把example1.txt从远程电脑的主目录移动到本地电脑的当前目录。

##### ssh密钥对
客户端生成密钥对：
```bash
ssh-keygen -t rsa -f test -C "test key"
```
* -t 加密类型
* -f 密钥文件名
* -C 备注

说明：执行命令会在.ssh（若没有可自行创建~/.ssh目录）目录下生成test、test.pub文件，test是私钥，test.pub是公钥。

服务端导入客户端的公钥：
```bash
$ cat test.pub >> .ssh/authorized_keys
```
修改权限：
```bash
chmod 700 .ssh
```
客户端可通过私钥文件去登录，而不需要密码登录
```bash
sudo ssh -i ~/.ssh/test 10.0.0.1
```

### FTP
#### 服务端安装
```bash
sudo apt-get update
sudo apt-get install vsftpd

yum install vsftpd
```
启动服务：
```bash
sudo service vsftpd start
```
#### 服务端配置
FTP服务端配置：
```bash
/etc/vsftpd/vsftpd.conf #配置文件
```

配置文件内容：
```bash
anonymous_enable=YES
允许匿名用户登录

local_enable=YES
允许系统用户名登录

write_enable=YES
允许使用任何可以修改文件系统的FTP的指令

local_umask=022
本地用户新增档案的权限

#anon_upload_enable=YES
允许匿名用户上传文件

#anon_mkdir_write_enable=YES
允许匿名用户创建新目录

dirmessage_enable=YES
允许为目录配置显示信息,显示每个目录下面的message_file文件的内容

xferlog_enable=YES
开启日记功能 

connect_from_port_20=YES
使用标准的20端口来连接ftp 

#chown_uploads=YES
所有匿名上传的文件的所属用户将会被更改成chown_username

#chown_username=whoever
匿名上传文件所属用户名 

#xferlog_file=/var/log/vsftpd.log
日志文件位置 

xferlog_std_format=YES
使用标准格式 

#idle_session_timeout=600
空闲连接超时 

#data_connection_timeout=120
数据传输超时 

#nopriv_user=ftpsecure
当服务器运行于最底层时使用的用户名 

#async_abor_enable=YES
允许使用\"async ABOR\"命令,一般不用,容易出问题 

#ascii_upload_enable=YES
管控是否可用ASCII 模式上传。默认值为NO
#ascii_download_enable=YES
管控是否可用ASCII 模式下载。默认值为NO

#ftpd_banner=Welcome to blah FTP service. 
login时显示欢迎信息.如果设置了banner_file则此设置无效 

#deny_email_enable=YES
如果匿名用户需要密码,那么使用banned_email_file里面的电子邮件地址的用户不能登录

#banned_email_file=/etc/vsftpd/banned_emails
禁止使用匿名用户登陆时作为密码的电子邮件地址 

#chroot_list_enable=YES
如果启动这项功能，则所有列在chroot_list_file中的使用者不能更改根目录 

#chroot_list_file=/etc/vsftpd/chroot_list
定义不能更改用户主目录的文件 

#ls_recurse_enable=YES   
是否能使用ls -R命令以防止浪费大量的服务器资源 

listen=YES 
绑定到listen_port指定的端口,既然都绑定了也就是每时都开着的,就是那个什么
standalone模式 

pam_service_name=vsftpd  
定义PAM 所使用的名称，预设为vsftpd

userlist_enable=YES 
若启用此选项,userlist_deny选项才被启动 

tcp_wrappers=YES 
开启tcp_wrappers支持 
```

#### 客户端使用
ftp连接：
```bash
ftp root@10.0.0.1
ftp 10.0.0.1
ftp 10.0.0.1 21
```

### TELNET
#### 服务端安装
```bash
yum -y install xinetd telnet telnet-server
```

开启telnet服务：
```bash
systemctl enable telnet.socket  
systemctl start telnet.socket  
systemctl enable xinetd  
systemctl start xinetd 
```

#### 服务端配置
编辑：/etc/xinetd.d/telnet文件

要允许通过xinetd联接telnet，需要编辑/etc/xinetd.d/telnet文件：
```bash
vim /etc/xinetd.d/telnet
```
将'disable'的值从'yes'修改为'no'。

要允许telnet从其他机子联接到本机，需要添加允许规则:
```bash
vim/etc/hosts.allow
添加如下行：
in.telnetd: ALL
```

如果需要开机自动开启该服务，将xinetd加入到/etc/rc.conf的"DAEMONS"中：
```bash
DAEMONS=(syslog-ng network netfs crond ............ xinetd)
```

说明：centos7下面安装telnet 没有生成 /etc/xinetd.d/telnet 文件。

#### 客户端使用
```bash
telnet 10.0.0.1 [port]
>>输入账号密码即可
```
