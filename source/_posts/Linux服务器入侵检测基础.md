---
title: Linux服务器入侵检测基础
date: 2017-03-24 11:26:24
comments: true
tags: Linux入侵检测
categories: 系统安全
---
<blockquote class="blockquote-center">人是生而自由的，但却无往不在枷锁之中，自以为是其他一切主人的人，反而比其他一切更是奴隶</blockquote>
　　最近遇到了很多服务器被入侵的例子，为了方便日后入侵检测以及排查取证，我查询了一些linux服务器入侵取证的相关资料，并在此总结分享，以便日后查询。
　　一般服务器被入侵的迹象，包括但不局限于：由内向外发送大量数据包（DDOS肉鸡）、服务器资源被耗尽（挖矿程序）、不正常的端口连接（反向shell等）、服务器日志被恶意删除等。那么既然是入侵检测，首先要判断的是服务器是否被入侵，必须排除是管理员操作不当导致的问题，因此入侵检测的第一项工作就是询问管理员服务器的异常现象，这对之后入侵类型的判断非常重要。
<!--more -->
　　在询问了相关异常信息，排除了管理员操作失误等原因后，那么便可以开始正式的上服务器进行入侵检测以及取证操作了。

### 审计命令

#### last
　　这个命令可用于查看我们系统的成功登录、关机、重启等情况，本质就是将/var/log/wtmp文件格式化输出，因此如果该文件被删除，则无法输出结果。

相关参数：
last -10（-n）   查看最近10条记录
last -x reboot   查看重启的记录
last -x shutdown 查看关机的记录
last -d          查看登陆的记录
last --help      命令帮助信息
last -f wtmp     用last命令查看wtmp文件（直接打开无法查看）

#### lastb
这个命令用于查看登录失败的情况，本质就是将/var/log/btmp文件格式化输出。

相关参数：
lastb name（root） 查看root用户登陆失败记录
lastb -10（-n）    查看最近10条登陆失败记录
lastb --heplp      命令帮助信息

#### lastlog
这个命令用于查看用户上一次的登录情况，本质就是将/var/log/lastlog文件格式化输出。

相关参数：
lastlog 所有用户上一次登陆记录
lastlog -u username（root） root用户上一次登陆记录
lastlog --help 命令帮助信息

#### who
　　这个命令用户查看当前登录系统的情况，本质就是将/var/log/utmp文件格式化输出。主要用来查看当前用户名称，以及登陆的ip地址信息，w命令与who一样，会更详细一些。

#### history
查看历史命令记录，其实就是查看root/.bash_history文件内容，删除这个文件，记录就没了。

相关参数：
history 查看所有历史记录
history -10 查看最近10条记录
history | grep "wget"  查看wget相关信息的记录
history --help         命令帮助信息

history显示时间戳：
```bash
export HISTTIMEFORMAT="%F %T `whoami` "
history | more
```

### 检查用户
Linux不同的用户，有不同的操作权限，但是所有用户都会在/etc/passwd、/etc/shadow、/etc/group文件中记录。
```bash
less /etc/passwd　　查看是否有新增用户
grep :0 /etc/passwd　　查看是否有特权用户（root权限用户）
ls -l /etc/passwd　　查看passwd最后修改时间
awk -F: '$3==0 {print $1}' /etc/passwd　　查看是否存在特权用户
awk -F: 'length($2)==0 {print $1}' /etc/shadow　　查看是否存在空口令用户
```
注：linux设置空口令：passwd -d username

### 检查进程
　　一般被入侵的服务器都会运行一些恶意程序，或是挖矿程序，或者DDOS程序等等，如果程序运行着，那么通过查看进程可以发现一些信息。
#### 普通进程
```bash
ps -aux　　查看进程
top        查看进程
lsof -p pid　　查看进程所打开的端口及文件
lsof -c 进程名　　查看关联文件
ps -aux | grep python | cut -d ' ' -f 2 | xargs kill   杀死python相关的进程
检查/etc/inetd.conf文件，输入：cat /etc/inetd.conf | grep –v "^#"，输出的信息就是你这台机器所开启的远程服务。
```
如果进程中没有发现异常，那么可以看看有没有开启某些隐藏进程。
#### 隐藏进程
```bash
ps -ef | awk '{print}' | sort -n | uniq >1
ls /proc | sort -n |uniq >2
diff 1 2
```
注：以上3个步骤为检查隐藏进程。

### 检查文件
被入侵的网站，通常肯定有文件被改动，那么可以通过比较文件创建时间、完整性、文件路径等方式查看文件是否被改动。
```bash
find / -uid 0 -print　　查找特权用户文件
find / -size +10000k -print　　查找大于10000k的文件
find / -name "…" -prin　　查找用户名为…的文件
find / -name core -exec ls -l {} \;　　查找core文件，并列出详细信息
md5sum -b filename　　查看文件的md5值
rpm -qf /bin/ls　　检查文件的完整性（还有其它/bin目录下的文件）
whereis 文件名　　查看文件路径
ls -al 文件名　　查看文件创建时间
du -sh  文件名   查看文件大小
```
### 检查网络
检查网络的目的，是查看黑客是否通过篡改网卡类型，进行流量嗅探等操作。
```bash
ip link | grep PROMISC　　正常网卡不应该存在promisc，如果存在可能有sniffer
lsof -i
netstat -nap　　查看不正常端口
arp -a　　查看arp记录是否正常
ifconfig -a　　查看网卡设置
```

### 检查计划任务
当我们尝试kill恶意程序时，往往会遇到被kill程序自动启动的问题，那么就要检查下计划任务(cron)了。
```bash
crontab -u root -l　　查看root用户的计划任务
cat /etc/crontab
ls -l /etc/cron.*　　查看cron文件是否变化的详细信息
ls /var/spool/cron/
```

### 检查系统后门
可以使用工具，如：Conmodo、rkhunter等，当然也可以手工输入命令检查。
```bash
vim $HOME/.ssh/authorized_keys　　查看ssh永久链接文件
lsmod　　检查内核模块
chkconfig –list/systemctl list-units –type=service　　检查自启
```
查看著名的木门后门程序：
```bash
ls /etc/rc.d   #系统开机后，此目录下的文件会被启动
ls /etc/rc3.d  
find / -name “.rhosts” –print
find / -name “.forward” –print
```

### 检查网站后门
　　如果服务器上运行着web程序，那么需要检查是否通过web漏洞入侵服务器，具体的判断方法可以结合分析中间件日志以及系统日志，但过程需要较长时间。我们也可以通过检查服务器上是否留有入侵者放置的网站后门木马，以此判断黑客是否通过web应用入侵到服务器。

#### Method One
* 将网站目录下，文件名中含有jsp、php、asp、aspx的文件（注意是含有）都copy出来并压缩。
* 通过windows下的[D盾](http://www.d99net.net/)工具扫描打包出来的目录，扫描是否存Webshell（网站后门）

#### Method Two
　　直接使用[MaskFindShell](https://github.com/tengzhangchao/MaskFindShell)工具，进行webshell扫描（目前只能扫描jsp与php的网站，并且php的误报比较高）
关于MaskFindShell详细用法，可以参考：[MaskFindShell-Document](https://github.com/tengzhangchao/MaskFindShell/blob/master/README.md)

#### 寻找服务器物理路径
无论哪种方法的webshell查找，首先要确定的是web服务器安装的路径，因为webshell都是放在web路径下的。

* 询问管理员、网站开发商
* [SearchWebPath](https://github.com/tengzhangchao/SearchWebPath)，具体用法参考：[SearchWebPath用法](http://thief.one/2017/03/10/SearchWebPath/)


### 打包文件
　　当我们做好一切入侵检测分析后，我们需要把一些日志文件copy到本地进行更进一步详细的分析时，怎么打包服务器相关信息，并且copy到本地呢？

#### 打包web文件
打包文件名中包含jsp的文件，打包后的文件为my_txt_files.tar：
```bash
tar cvf my_txt_files.tar `find . -type f -name "*.jsp*"`
```
#### 打包日志文件
```bash
tar -cvf log.tar /var/log
```
#### 打包其他信息
```bash
last > last.log
netstat -an > netstat.log
......
```
### 传输文件到本地
将服务器上的文件传输到本地电脑上的几种方法。
#### lrzsz
如果ssh连接的客户端为xshell等，可以安装lrzsz命令（putty无法使用）
```bash
apt-get install lrzsz
```
使用：
上传文件到linux，rz；下载linux文件，sz 文件名。

#### 开启ftp或者http
　　开ftp这里我不介绍了，网上很多教程，这里主要说说开启http服务。
　　一般linux服务器都默认安装了python，那么可以借助python快速开启一个http服务，详细参考：[基于Python的WebServer](http://thief.one/2016/09/14/%E5%9F%BA%E4%BA%8EPython%E7%9A%84WebServer/)

#### U盘挂载
如果我们不是通过ssh的方式连接，而是直接通过显示器连接上服务器进行操作，那么可以尝试U盘传输。
```bash
fdisk -l 查看U盘路径
monut /dev/sdb4 /mnt  挂载U盘
cd /mnt 进入U盘
umount /mnt  退出U盘
```

本文总结的都是一些Linux入侵检测最基础的命令，至于怎么用好这些命令，需要结合实际情况，主要还是看经验。以上所诉，还只是入侵检测信息收集阶段，至于如何通过现有信息分析出入侵途径，还需要借助其他工具以及知识。


参考链接：http://www.jb51.net/hack/421908.html

转载请说明出处:
[Linux服务器入侵检测基础 | nMask'Blog](http://thief.one/2017/03/24/Linux%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%85%A5%E4%BE%B5%E6%A3%80%E6%B5%8B%E5%9F%BA%E7%A1%80/)

本文地址：
http://thief.one/2017/03/24/Linux%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%85%A5%E4%BE%B5%E6%A3%80%E6%B5%8B%E5%9F%BA%E7%A1%80/