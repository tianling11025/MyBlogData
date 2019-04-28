---
title: 自动生成正则大法暨CreateRe模块使用说明
copyright: true
permalink: 1
top: 
date: 2017-11-07 20:06:46
tags:
- 正则
- CreateRe
categories: 编程之道
password:
---
<blockquote class="blockquote-center">妈妈再也不用担心我的正则啦!</blockquote>
　　老早以前就想写个自动生成正则表达式的Python模块出来，但思前想后也没有一个很好的技术方案。今晨突然灵光一闪，一气呵成下写了个CreateRe模块。说实话生成正则的能力一般，此模块能生成简单的正则表达式，适合初学者，可供压根不懂正则表达式也不想学正则的有为青年使用，简单方便一键生成。有想学习正则语法的麻烦青年，请移步：[Python 正则表达式](https://thief.one/2017/10/30/1/)
<!-- more -->

### CreateRe模块介绍
　　Python生成正则表达式模块，此模块用来逆向的生成正则表达式。只需要传入待匹配的字符串，以及预期想要匹配出的结果列表，即可以生成一个正则表达式。
　　当然目前模块还不够成熟，具体表现在：第一生成能力有限（复杂的可能生成不了），第二是生成的正则表达式不够简便（我们知道同一个匹配效果，可以有很多种正则表达式去实现，高手往往能写出最短最优化的正则，而此模块尚处于入门阶段），只适合正则初学者使用。

### CreateRe模块使用
#### Download
```bash
git clone https://github.com/tengzhangchao/CreateRe.git
```

#### Import Module导入模块
导入CreateRe模块，使用实例，可参考项目中的test.py文件
```bash
from CreateRe import create_re
```

#### 生成正则表达式
```bash
# 待匹配的字符串
STRING = u""

# 预想匹配结果列表
S = [""]

cur=create_re() #实例化类
RES=cur.run(STRING,S,tag=True) #生成正则表达式
check_result=cur.check_res(RES,tag=True) #Check正则表达式,返回匹配后的结果
```

#### run函数参数说明

* STRING 待匹配的字符串，必须为unicode格式
* S 预想正则匹配结果列表，必须为List，且如果List中有中文选项，则需要为unicode格式
* tag 贪婪匹配的开关，具体区别下面会介绍

#### 演示说明
```bash
STRING = u'''
http://thief.one nmask
http://tool.nmask.cn nm4k
http://home.nmask.cn nmask
'''

S = ["http://tool.nmask.cn"]

tag=False
cur=create_re()
RES=cur.run(STRING,S,tag=tag)
check_result=cur.check_res(RES,tag=tag)
print RES
print check_result
```
运行结果：
```bash
([a-z]{4}\:/{2}[a-z]{4}\.[a-z]{5}\.[a-z][a-z]) nm4
[u'http://tool.nmask.cn']
```
当改变tag的值，tag=True，运行结果：
```bash
([a-z]{4}\:/{2}[a-z]{4}\.[a-z]{5}\.[a-z][a-z])
[u'http://tool.nmask.cn', u'http://home.nmask.cn']
```

说明：tag=True表示开启贪婪匹配，即生成的正则将会尽可能多的匹配出结果，缺省为False。

S的值也可以指定多个:
```bash
STRING = u'''
http://thief.one nmask
http://tool.nmask.cn nm4k
http://home.nmask.cn nmask
'''

S = ["http://tool.nmask.cn","http://thief.one"]

tag=True
cur=create_re()
RES=cur.run(STRING,S,tag=tag)
check_result=cur.check_res(RES,tag=tag)
print RES
print check_res
```
运行结果:
```bash
([a-z]{4}\:/{2}[a-z]{4}(?:.?){2}[a-z]{3}(?:.?){4}) 
[u'http://thief.one', u'http://tool.nmask.cn', u'http://home.nmask.cn']
```
如果将tag改为False，则结果为：
```bash
([a-z]{4}\:/{2}[a-z]{4}(?:.?){2}[a-z]{3}(?:.?){4}) 
False
```
返回check_res=False表示生成的正则表达式，并不能匹配出想要的结果；可以将tag改为True尝试。

#### 获取模块内置的正则表达式
```bash
cur=create_re()
print cur.get_res("email") #邮箱
print cur.get_res("phone") #电话
print cur.get_res("name") #姓名
print cur.get_res("id_15") #身份证 15位
print cur.get_res("id_18") #身份证 18位
print cur.get_res("car_id") #车牌
print cur.get_res("address") #家庭住址
```

#### 模块返回值
```bash
tag=True
cur=create_re()
RES=cur.run(STRING,S,tag=tag)
check_result=cur.check_res(RES,tag=tag)
```

* RES 模块生成的正则表达式
* check_result 利用正则表达式生成结果与预期相比较，若返回False则表示失败，返回结果列表则表示成功

### 项目地址
https://github.com/tengzhangchao/CreateRe

### 在线正则测试
http://tool.nmask.cn/python_re/

