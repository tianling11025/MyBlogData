---
title: Falcon For Python REST API
copyright: true
permalink: 1
top: 0
date: 2017-11-27 19:52:51
tags:
- python
- falcon
categories: 编程之道
password:
---
<blockquote class="blockquote-center">一杯敬明天，一杯敬过往</blockquote>
　　说到Web Api，以往我一直使用Django来写，但众所周知Django框架很厚重，用来写web Api未免显得不够简便。虽然Django有一个专门写Api的框架，[`Django REST Framework`](https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjkrczd297XAhWBypQKHfcKAIcQFggoMAA&url=http%3A%2F%2Fwww.django-rest-framework.org%2F&usg=AOvVaw29pzSINqgKLUWpQ2vWBvg1)（适合写比较复杂的Api，后面我会单独成文介绍），但感觉还是偏厚重了点。那么有没有几行代码就能写出一个Api的方案呢？Falcon框架就是为此而生的。(除此之外，Flask等框架也可用来写Api，但个人认为最轻便的就属Falcon了)
<!--more -->
　　Falcon是一个构建云Api的高性能Python框架，它鼓励使用REST架构风格，尽可能以最少的力气做最多的事情，简单来说它就是用来写Web Api的，有多简便，往下看了就知道。

Falcon官方文档：http://falcon.readthedocs.io/en/stable/api/request_and_response.html
Falcon开源地址：https://github.com/falconry/falcon

### Falcon安装
```bash
pip install falcon
```

### Falcon写一个简单的api
新建一个app.py文件，写入以下内容：
```bash
from wsgiref import simple_server
import falcon

class HelloWorld(object):

    def on_get(self, req, resp):

        print req.context
        print req.scheme
        print req.params

        resp.status = falcon.HTTP_200
        resp.body = ('Get hello world')
    
    def on_post(self, req, resp):

        print req.stream.read() 获取post_data

        resp.status = falcon.HTTP_200
        resp.body = ('Post hello world')


app = falcon.API()
hello = HelloWorld()
app.add_route('/', hello)


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
```
运行app.py文件：
```bash
python app.py
```
运行程序将会在本地监听8000端口，我们可以使用curl或者http工具测试一番：
先发一个GET请求：
```bash
http GET http://127.0.0.1:8000/

HTTP/1.0 200 OK
Date: Mon, 27 Nov 2017 11:50:36 GMT
Server: WSGIServer/0.1 Python/2.7.10
content-length: 15
content-type: application/json; charset=UTF-8

Get hello world
```
尝试发POST请求：
```bash
http POST http://127.0.0.1:8000/

HTTP/1.0 200 OK
Date: Mon, 27 Nov 2017 11:50:45 GMT
Server: WSGIServer/0.1 Python/2.7.10
content-length: 16
content-type: application/json; charset=UTF-8

Post hello world
```
说明：Falcon支持任何类型的请求，比如OPTIONS，PUT，HEAD等，当然前提是需要在app.py代码中定义，定义方式为on_*，比如：on_get、on_post、on_put等。

更复杂一些的api例子，可以参考官网。关于request与response的一些方法，官网有很详细的介绍，这里不再记录。

### 使用gunicorn代替内置的服务器
使用python app.py的方式运行api，其实是使用了其内置的服务器，类似于django的manage.py。用于生产环境时，通常会使用gunicorn来代替内置的服务器，当然代码也可以简略为：
```bash
import falcon

class HelloWorld(object):

    def on_get(self, req, resp):

        print req.context
        print req.scheme
        print req.params

        resp.status = falcon.HTTP_200
        resp.body = ('Get hello world')
    
    def on_post(self, req, resp):

        resp.status = falcon.HTTP_200
        resp.body = ('Post hello world')


app = falcon.API()
hello = HelloWorld()
app.add_route('/', hello)
```
#### 安装gunicorn
```bash
pip install gunicorn 
```
#### 使用gunicorn
```bash
gunicorn app:app -b 127.0.0.1:8080
```
注意：:前的app是指app.py，:后的app是指app.py文件中的app对象。

gunicorn只支持unix（linux、mac），如果是windows用户，可用waitress替代。
```bash
$ pip install waitress
$ waitress-serve --port=8000 app:app
```
关于gunicorn更多的用法，比如指定端口号之类的，可以`gunicorn --help`查看帮助。
