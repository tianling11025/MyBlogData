---
title: Upload Package to Pypi
copyright: true
permalink: 1
top: 0
date: 2017-11-08 15:57:44
tags:
- pypi
categories: 技术研究
password:
---
<blockquote class="blockquote-center">斑驳的夜色在说什么
谁能告诉我如何选择</blockquote>
　　相信使用过python的朋友一定熟悉pip，用它可以方便的管理下载第三方包。那么如何上传自己的Python package到pypi网站呢？即可以使用pip命令下载到自己的package包？
<!--more -->

### 注册pypi网站的账号
访问：https://pypi.python.org/pypi?%3Aaction=register_form 注册一个账号。

### 打包package
我们需要将自己写好的python文件，打包成.tar.gz以及.whl的压缩包。
#### 安twine
```bash
pip install twine
```
#### 编写setup.py文件
在项目的根目录下，新建setup.py文件，格式如下：（最简单的）
```bash
from setuptools import setup

setup(
    name='CreateRe',
    version='1.0.0',
    description='To Create Re Python project',
    url='https://github.com/tengzhangchao/CreateRe',
    author='nMask',
    author_email='tzc@maskghost.com',
)
```
复杂一点的例子：https://github.com/pypa/sampleproject/blob/master/setup.py 

#### 生成dist
```bash
python setup.py sdist
```
说明：执行完命令可以看到项目目录下新增了一个dist目录，里面新增了一个.tar.gz压缩包。

#### 生成.whl
```bash
pip install wheel
python setup.py bdist_wheel --universal
```
说明：执行完命令可以看到dist目录里面新增了一个.whl压缩包。

### 上传压缩包到pypi
```bash
twine upload dist/*

>>>输入账号
>>>输入密码
```

### 使用pip下载安装包
例子：https://pypi.python.org/pypi/CreateRe/1.0.0
这是我上传的包，在主页面可以看到.tar.gz与whl两种格式的安装包，另外上传成功后等待10分钟左右，便可以使用pip直接安装了。
```bash
pip install CreateRe
```

### 参考
https://packaging.python.org/tutorials/distributing-packages/