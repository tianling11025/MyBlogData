---
title: Python代码热重载函数reload
copyright: true
permalink: 1
top: 0
date: 2018-11-27 17:12:26
tags:
- Python
- reload
categories: 编程之道
password:
---
<blockquote class="blockquote-center">我走过山时，山不说话， 
我路过海时，海不说话， 
小毛驴滴滴答答，倚天剑伴我走天涯。 
大家都说我因为爱着杨过大侠，才在峨嵋山上出了家， 
其实我只是爱上了峨嵋山上的云和霞， 
像极了十六岁那年的烟花。</blockquote>
　　代码热重载是在一个项目中比较常见的需求，尤其是在扫描服务的开发中，扫描插件的代码需要经常修整，因此如何做到插件代码能够热重载加载，而不是每次修改代码后需要重启服务就变得尤为重要。由于最近正好在一个Python项目中需要实现热重载需求，因此写了个python版的代码热重载demo，仅供参考。
<!--more -->

### python中的reload函数
python2中的reload函数可以直接使用，无需导入第三方模块，可以直接使用：
```bash
reload(module) # reload接收的参数必须是已经导入的模块
```
python3中的reload函数移到了imp库里面，因此需要导入：
```bash
from imp import reload
reload(module)
```

### demo_1
demo1是基于最常见的需求，即同一个目录下有2个文件（plugin.py，scan.py），scan.py文件调用plugin.py文件。

plugin.py文件如下：
```bash
print "plugin start scan ......"
```
scan.py文件如下：
```bash
import time
import plugin
while 1:
    reload(plugin)
    time.sleep(1)
```
运行scan.py，然后手工修改plugin.py文件内容，观察输出的变化。
![](/upload_image/20181127/1.jpg)

### demo2
demo2会稍微复杂一点点，即同一个目录下有2个文件（plugin.py，scan.py），scan.py文件调用plugin.py文件里面的crack函数。

plugin.py文件如下：
```bash
def crack():
    print "plugin start scan ......"
```
scan.py文件如下：
```bash
import time
import plugin
while 1:
    reload(plugin)
    eval("plugin.crack()")
    time.sleep(1)
```
运行结果跟demo1一样，就是在调用之前先reload一下模块，然后再利用eval调用模块的函数。

### demo3
demo3针对更为现实的需求，即不同目录下的2个文件（./scan.py，./plugins/plugin.py），scan.py文件调用plugins目录下的plugin.py文件里面的crack函数。

plugin.py文件如下：
```bash
def crack():
    print "plugin start scan ......"
```
scan.py文件如下：
```bash
import time
exec("import plugins.plugin")

while 1:
    reload(eval("plugins.plugin"))
    eval("plugins.plugin.crack()")
    time.sleep(1)
```
运行结果跟demo1一样，这样需要注意的是，reload不支持from plugins improt plugin的方式重载模块，因此可以使用import plugins.plugin的方式导入模块并重载。






