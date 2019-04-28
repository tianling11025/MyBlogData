---
title: HTTP-API认证，Python实现方案
copyright: true
permalink: 1
top: 0
date: 2017-12-11 16:40:01
tags:
- python
categories: 编程之道
password:
---
<blockquote class="blockquote-center">一杯敬自由，一杯敬死亡</blockquote>
　　标题写的比较模糊拗口，简单来说本文就是介绍如何利用python将http的api接口做加密认证，防止不法分子乱用。这里有几个前提需要说明下，首先我们要实现的是http的加密认证，因此不考虑https。其次认证的目的是为了让一个http的api接口让正确的（通过认证的）人使用，而不是任何都可以用。
<!--more-->
### 设计方案
明白了http api认证的目的，那么就来设计方案吧！

#### 最偷懒的方案
我之前写过几个api接口，主要是自己用来传输一些数据库数据的，由于数据有一点敏感，因此使用了认证。当时为了偷懒，认证的方式写得特别简单无脑，即在api接口上增加了一个auth字段，字段的内容会在服务端进行校验，但其内容是一串写死的md5。这虽然也算是一种认证方式(不知道auth字段内容的朋友无法拿到api接口的数据)，但如果局域网内流量被监听，那这种方案就形同虚设了。

#### 比较简单实用的设计方案
一种比较好的设计方案，是在客户端与服务端实现一套加密算法，算法可自定义但最好复杂一点。如将请求的参数以及内容以一定的方式排列后，可以再加上时间戳，整体做一个hash运算。服务端将获取的参数同样做hash，与客户端传递的hash做对比。因为有了时间戳，即使被监听了流量，进行流量重放也是不能认证成功的。（因为时间戳存在差异）

*说明一下：本文介绍的是api的一个认证方式，这跟网站啥的认证还是有区别的。主要还是看api的应用场景，如果是给内部人员调用，而且调用的用户不多，其实以上认证方案足够了。因为用来加密的密钥（key）可以用其他安全的方式发送给用户（甚至可以写纸上，2333），而不必像https协议一样，使用非对称加密+对称加密，并且使用数字证书等一系列复杂的加密认证方式。*

<hr>

好了，前文介绍了一些api认证的方案，那么接下来再写点啥呢？我不打算介绍怎么去开发一个认证方案的代码，我主要想推荐一个开源的项目---hawk，因为它就是用来实现http加密认证的，而且它有一个python的实现模块（mohawk），推荐它是因为它比较简单实用。

因为之前研究过mohawk模块2个小时（真的是2个小时），因此本文主要介绍一下mohawk的用法。企业内部一般自己设计api的加密认证方案（一般是生成一个token密文，严格一点的会做双因子认证），因此这个模块适合给初学者练练手，也可以给打算自己设计认证方案的朋友提供一种思路。以下内容是我阅读mohawk文档总结的一些基础用法，更详细的可以参考下官网文档。

### hawk介绍
hawk项目地址：https://github.com/hueniverse/hawk
python实现：https://github.com/kumar303/mohawk
官方文档：https://mohawk.readthedocs.io/en/latest/

#### 安装hawk
```bash
pip install mohawk
```

### 构建一个webserver
这里我使用python的falcon框架来构建一个api webserver，如果对falcon框架不熟悉，可以先阅读：https://thief.one/2017/11/27/1/
```bash
import falcon
from mohawk import Receiver # 导入mohawk模块的Receiver方法
from wsgiref import simple_server

# 认证字典,可以创建不同的用户，每个用户都可以用不同的密钥（key）
allowed_senders={

    "test":{

        'id': 'test',
        'key': '110',
        'algorithm': 'sha256'

    }, # test 用户组

    "nmask":{

        'id': 'nmask',
        'key': '112',
        'algorithm': 'sha256'

    }, # nmask 用户组

}


def lookup_credentials(sender_id):
    ''' 验证用户是否在允许的范围内 '''
    if sender_id in allowed_senders:
        return allowed_senders[sender_id]
    else:
        raise LookupError('unknown sender')


class Test(object):
    def on_post(self, req, resp):
    ''' http post 方法 '''
        try:
            Receiver(
                    lookup_credentials, 
                    req.headers.get('AUTHORIZATION'), # 请求时生成的密钥
                    req.url,
                    req.method,
                    content= req.stream.read(),
                    content_type=req.headers.get('CONTENT-TYPE')
            )
        except Exception,e:
            ''' 报错则说明认证失败 '''
            print e
            resp.status = falcon.HTTP_403  # This is the default status
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('Hello World!')


    def on_get(self, req, resp):
        ''' http get 方法 '''
        try:
            Receiver(
                    lookup_credentials,
                    req.headers.get('AUTHORIZATION'),
                    req.url,
                    req.method,
                    content= req.stream.read(),
                    content_type=req.headers.get('CONTENT-TYPE')
            )
        except Exception,e:
            print e
            resp.status = falcon.HTTP_403  # This is the default status
            resp.body = ('authorization fail!')
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('Hello World!')



app = falcon.API()
test = Test()
app.add_route('/', test)


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()

```
### 构建一个http请求
搭建好webserver以后，我们自然需要构建http请求，去验证请求是否经历了认证的过程，且认证的结果是否正确，这里使用requests包去构建。
```bash
import json
import requests
from mohawk import Sender # 导入mohawk模块的Sender方法

url = "http://127.0.0.1:8000/"
post_data = json.dumps("") # 如果是get请求，参数内容可以设置为""
content_type = 'application/x-www-form-urlencoded'

# 用于认证的字典
credentials = {

               'id': 'test',
               'key': '10',
               'algorithm': 'sha256'
           }

sender = Sender(credentials,
                url = url, # 必填
                method = 'POST', # 必填 
                content = post_data, # 必填，如果是get请求，参数内容可以设置为""
                content_type = content_type # 必填
            )

print sender.request_header # 生成的密文，通过header的形式传递到服务端

res=requests.post(
                url = url,
                data = post_data,
                headers={
                        'Authorization': sender.request_header,
                        'Content-Type': content_type
                        }
                )

print res.status_code
print res.text
```
### mohawk模块说明
mohawk是hawk的python实现，有几个主要方法：Sender、Receiver等，详细的可以去阅读源码。

Sender方法用来生成在http请求认证中所需的密码，该方法需要传递几个参数，比如：url、method、content（post_data）、content_type、credentials(认证的字典，包含了id、key、加密方式)等，该方法会根据传递的参数值，生成一个密文密码，然后我们可以将其放在headers中传递到服务端。

Receiver方法用来在服务端接收客户端传递的请求，根据获取的参数的内容计算出一个新的密文密码，与客户端传递的密文进行对比，达到认证的效果。


