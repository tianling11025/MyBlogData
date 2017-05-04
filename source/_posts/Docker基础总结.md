---
title: Docker基础总结
date: 2017-05-04 15:18:37
comments: true
tags:
- docker
categories: 技术研究
permalink: 01
---
<blockquote class="blockquote-center">人生如戏，而你是若不是演员？</blockquote>
　　最近玩了玩Docker，感觉还不错，在此记录分享下docker的一些基础用法。本篇内容会随着本人对docker的不断地深入研究使用而补充，也欢迎大家纠错。
　　Docker的优点这里不再细说，docker的用途非常广，我最近准备使用它搭建测试环境（漏洞测试环境、开发测试环境等），还可以用来部署分布式项目（可以极大程度得利用服务器资源），当然docker的用途还有很多，这里不再详述。
<!--more -->
### docker 介绍
* image:镜像
* Container:容器

　　docker容器是构建在镜像之上的，我们可以将image理解为定义好的类，而container便是实例，一个类可以实例化出很多实例，同样docker也可以在镜像上运行多个容器，每个容器可以是一样的，也可以是定制化的。
### docker install
docker可以运行在linux、mac、windows上。
#### install docker for mac
前往官网下载安装包：https://www.docker.com/products/docker#/mac
下载完以后直接安装，安装完成后运行docker run hello-world，如果没有报错，说明安装成功。
更换镜像源（填写国内的镜像源）：
![](/upload_image/20170504/1.png)
#### install docker for linux
可以上网查询，网上资料比较多，本人暂没有测试安装。
### docker 基础命令
　　docker基础命令包含docker操作、镜像操作、容器操作以及其他相关操作，以下列举了一些常用的命令，更多请参考官方文档，或者使用--help命令查看。
#### docker操作
查看docker信息
```bash
$docker info
Containers: 1  #1个容器
 Running: 1    #1个容器正在运行
 Paused: 0
 Stopped: 0
Images: 5   #5个镜像
Server Version: 1.12.3
......
```
查看docker版本
```bash
$docker -v
Docker version 1.12.3, build 6b644ec
$docker version
Client:
 Version:      1.12.3
 API version:  1.24
 Go version:   go1.6.3
 Git commit:   6b644ec
 Built:        Wed Oct 26 23:26:11 2016
 OS/Arch:      darwin/amd64

Server:
 Version:      1.12.3
 API version:  1.24
 Go version:   go1.6.3
 Git commit:   6b644ec
 Built:        Wed Oct 26 23:26:11 2016
 OS/Arch:      linux/amd64
```
#### 镜像操作
查看本地镜像列表:
```bash
docker images -a  #-a可以查看所有的image
```
![](/upload_image/20170504/4.png)
其他镜像操作：
```bash
docker search (image-name) 查询镜像 example：docker search ubuntu
docker history (image-name) 查看镜像的历史版本
docker push (image-name) 将镜像推送到registry
docker pull image-name:tag pull镜像 example:docker pull ubuntu:latest
docker rmi  <image id>   删除镜像（先stop并删除镜像上的所有容器）
docker rmi $(docker images -q) 删除全部镜像
docker tag image-id imagename:tag 修改镜像的tag标签
docker load -i test.tar 从tar文件中载入镜像
docker save image > test.tar 保存镜像为tar文件
```
#### 容器操作
创建容器：
```bash
docker run --rm -ti ubuntu /bin/bash
```
* --rm   一旦进程退出，则删除容器
* -ti    进入交互模式
* ubuntu 容器立足的镜像名字
* /bin/bash  要运行的命令

```bash
docker run -d -p 8000:80 --name test image-name
```
* -d   后台运行
* -p   映射的端口,:前为本机，后为容器
* --name 自定义名称

注意：创建容器以后， 会返回一个ID，是随机生成的。

检查容器运行状态：
```bash
docker ps -a（显示所有容器，包括已经stop的）
```
![](/upload_image/20170504/5.png)
进入容器内部（shell）：
```bash
docker exec -ti centos /bin/bash
```

容器操作：
```bash
docker attach container 进入容器交互式界面
docker diff  container 列出容器内发生变化的文件与目录
dcoker logs ID(容器的ID，可以用docker ps查看)   查看docker上的容器的状态
docker stop ID(或者容器名字)  关闭运行中的容器
docker start ID 开启容器
docker restart ID  重启运行中的容器
docker stop ID docker rm ID  移除容器（先关闭再删除）
docker kill [options] container 杀死容器的主进程
docker stop $(docker ps -a -q) 停止所有container
docker rm $(docker ps -a -q)   移除所有container
docker commit ID new镜像名字（只能字母加数字） 将容器的状态保存为镜像
docker export container > test.tar  将容器打包成tar文件
docker cp container:path hostpath  从容器内复制文件到指定的路径
```
#### other操作
```bash
docker import http://example.com/example.tar  远程导入文件
docker login [options][server]  用来登陆自己的registry
docker inspect container/image  收集容器的信息（ip地址，端口等）
docker wait container  阻塞
```
### dockerfile
　　dockerfile可以用来动态生成新的镜像，比如说我们pull了一个基础的centos镜像，现在需要在此镜像内安装一些软件，以便可以顺利运行我们准备的项目代码，那么可以使用以下2种方案：
#### 方案一：（手动式）
　　在centos镜像上创建一个容器，进入容器交互式界面后，手动安装一些需要的软件，配置好环境。当做好所有的修改后，使用docker commit container-id newimagename创建新的镜像。再使用新的镜像来创建容器，运行我们的项目代码。
#### 方案二：（自动式）
　　所谓自动化，就是不需要进入容器手动输入命令进行配置，一切都在容器运行时自动处理，那么这就要用到dockerfile了。dockerfile简单来说就是一个配置文件，docker容器在运行时会处理这个文件内容，比如安装软件，修改环境变量，运行程序等。使用dockerfile的好处在于可以很方便的修改配置文件内容，达到创建动态镜像的效果。
#### 创建dockerfile
　　我们需要创建一个目录来存放Dockerfile文件，目录名称可以任意取，在该目录里创建Dockerfile文件。这里我以创建一个基于centos基础镜像，容器运行后会自动开启一个python webserver（本地监听8080端口）的例子。
#### 编写dockerfile
在Dockerfile文件内写入：
```bash
# Version 0.1
# 基础镜像
FROM centos:latest
# 维护者信息
MAINTAINER http://thief.one
# 镜像操作命令
RUN yum install wget
# 容器启动命令
CMD python -m SimpleHTTPServer 8080
```
dockerfile语法类似于MakeDown，基础内容如下：
* FROM 基于的基础镜像名称
* MAINTAINER 维护者信息
* RUN 运行的命令（安装软件等）
* CMD 启动容器时运行的命令（只能写一条）

语法不止这些，更多内容，可以参考官方文档。
#### 生成dockerfile镜像
进入到Dockerfile文件所在目录，运行：
```bash
docker build -t centos_test:01 .
```
此时，运行docker images -a查看，会发现多了一个image，名称为centos_test，tag为01
![](/upload_image/20170504/2.png)
#### 使用dockerfile镜像
在此image上运行容器：
```bash
docker run -d -p 80:8080 centos_test:0.1
```
此时，打开本机的127.0.0.1:80
![](/upload_image/20170504/3.png)

*docker的内容非常多，以上只是一些最基础的用法，本文也将会持续更新*

>转载请说明出处：[Docker基础总结|nMask'Blog](http://thief.one/2017/05/04/1)
本文地址：http://thief.one/2017/05/04/1