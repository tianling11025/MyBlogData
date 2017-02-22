---
title: Shadowsocks折腾记
date: 2017-02-22 21:03:25
comments: true
tags: shadowsocks
categories: 技术交流
---
　　事情的起因是服务器网络被某网站屏蔽，需要使用http代理去访问。由于没有稳定好用的http代理地址（网上免费的信不过，也不稳定），然而手头上还有空余的服务器（云上），于是就想着在云服务器上搭建shadowsocks服务端，本地服务器上搭建客户端用来连接。思路有了，那就动手干吧，搭建shadowsocks服务并不难，然而原本应该只需半小时就能搞定的活，却足足花了2个多小时（socks转http代理问题），因此在此小计一番，以儆效尤。

### Install shadowsocks Server
搭建shadowsocks服务端，分别介绍windows与linux下搭建方法。
#### Windows
先安装python，然后再利用pip安装shadowsocks.
```bash
pip install shadowsocks
```
然后创建一个文件，如：config.json
```bash
{
"server":"",     ##服务器ip地址
"server_port":8000,  ##代理端口
"local_address":"127.0.0.1",
"local_port":1080, ##本地监听端口
"password":"",   ##连接密码
"timeout":300,
"method":"aes-256-cfb", ##加密方式
"dast_open":false
}
```
填写完以后，在cmd里运行：
```bash
ssserver -c config.json
```
如果没有报错的话，shadowsocks服务端就已经搭建好了。

#### Linux
##### Install
与windows的类似，先通过pip安装shadowsocks.
```bash
sudo apt-get install  python-pip
sudo apt-get install python-m2crypto
sudo pip install  shadowsocks
```
##### 配置config文件
```bash
mkdir /etc/shadowsocks
vim /etc/shadowsocks/config.json （一定要在这个目录下）
```
写入：(ip也可以写内网地址，只要能转发出来即可。)
单用户配置：
```bash
{
"server":"",  
"server_port":8000,
"local_address":"127.0.0.1",
"local_port":1080,
"password":"",
"timeout":300,
"method":"aes-256-cfb",
"fast_open":false
}
```
多用户配置：
```bash
{
"server":"",
"local_address":"127.0.0.1",
"local_port":1080,
"port_password":{
"8000":"123456",
"8001":"123456"
},
"timeout":300,
"method":"aes-256-cfb",
"fast_open":false
}
```
##### 命令行启动关闭
```bash
ssserver -c /etc/shadowsocks/config.json -d start 后台启动
ssserver -c /etc/shadowsocks/config.json -d stop 后台停止
```
##### 设置开机启动
将启动的命令加入到/etc/rc.local文件的最后
```bash
vi /etc/rc.local
```
##### 设置非root用户运行ss
```bash
sudo useradd ssuser //添加一个ssuser用户
sudo ssserver [other options] --user ssuser //用ssuser这个用户来运行ss
```
将之前的ssserver -c /etc/shadowsocks.json -d start改为ssserver -c /etc/shadowsocks.json -d start --user ssuser

### Install shadowsocks Client
安装shadowsock客户端我也分为windows与Linux两种情况进行介绍。

#### Windows
windows安装shadowsocks客户端比较简单，直接下载安装程序。
启动以后，填入服务端相应的配置（ip，port，密码，加密方式）
设置模式：
![](/upload_image/20170222/1.png)
![](/upload_image/20170222/2.png)
推荐使用PAC模式。

#### Linux
*此次主要花费的时间就在于linux上搭建shadowsocks客户端，坑不少（~主要是自己脑子有点晕~）*
##### Install
安装同样简单：
```bash
pip install shadowsocks
```
##### 配置condfig
配置也很简单，创建一个shadowsocks.json文件：
```bash
{
"server":"",
"server_port":8000,
"local_port":1080,
"password":"",
"timeout":600,
"method":"aes-256-cfb"
}
```
内容类似上面，然后在命令行中运行：sslocal -c shadowsocks.json 此时系统会监听本地的1080端口。

##### socks转http代理问题
　　此时不是GUI窗口，只是一个命令行，怎么用curl等命令走http代理（网上资料大部分是设置浏览器，但不适合本文），原本可以用其他方案解决，但此时偏偏选择了shadowsocks，就只能一路走下去了。等一切都安装好，启动完以后，我发现http代理仍然用不了，然后就开始了心力憔悴的调试，搞了半天也还是用不了，最终同事发现了问题（socks代理需要转化为http代理，windows可以设置浏览器，linux需要下载工具转化）。
　　发现了原因所在，那么现在的问题是怎么讲socks代理转化为http代理？

##### socks转http代理方案
* proxychains 可以自动将socks代理转化为http代理。
* polipo      用这个工具将socks代理转化为http代理。

##### proxychains
安装：
```bash
git clone https://github.com/haad/proxychains
./configure
make
sudo make install
```
配置：
修改配置文件proxychains.conf
```bash
将socks4 127.0.0.1 9095改为socks5  127.0.0.1 1080  //1080改为你自己的端口
```
使用：
```bash
proxychains curl http://thief.one
```
详情参考：[http://www.tuicool.com/articles/rUNFF3](http://www.tuicool.com/articles/rUNFF3)
##### polipo
安装：
```bash
sudo apt-get install polipo
```
配置：
停止polipo服务 sudo service polipo stop
编辑polipo配置文件/etc/polipo/config，添加如下内容：
```bash
socksParentProxy = localhost:1080
proxyPort = 1081
```
启动polipo服务 sudo service polipo start

使用：
* app里面配置http_proxy=http://127.0.0.1:8787
* bash里面可以编辑$HOME/.bashrc，添加export http_proxy=http://127.0.0.1:8787　导出环境变量。当前bash要执行source $HOME/.bashrc来使配置文件生效。
* git配置git config --global http.proxy 127.0.0.1:8787

详情参考：[http://blog.csdn.net/zcq8989/article/details/50545078](http://blog.csdn.net/zcq8989/article/details/50545078)



*本文没有什么技术干货，都是一些操作细节。当然，技术本身也是由一个个细节拼凑而成！*