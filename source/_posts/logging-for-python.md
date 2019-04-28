---
title: logging for python
copyright: true
permalink: 1
top: 0
date: 2017-11-10 14:56:59
tags:
- logging
- python
categories: 编程之道
password:
---
<blockquote class="blockquote-center">远距离的欣赏，近距离的迷惘</blockquote>
　　开发项目中缺不了日志控制，而在python中编写日志往往选择封装logging库，因为logging库足够强大，且支持自由配置。今日在开发项目的过程中，折腾了logging好一会儿，在此记录一下。
<!--more-->

### logging模块
日志级别（level）：
```bash
CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
```

### logging基础使用
```bash
import logging

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
logging.error('This is error message')

>>>运行结果
WARNING:root:This is warning message
ERROR:root:This is error message
```
说明：运行程序将直接在控制台输出日志内容，默认情况下日志级别为WARNING，即级别大于等于WARNING的日志才会被输出。

### logging.basicConfig
通过basiConfig函数对logging日志进行配置：
```bash
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')
    
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
logging.error('This is error message')

```
说明：运行程序将不会在控制台有任何输出，而是生成了一个test.log文件，文件内容为：
```bash
Fri, 10 Nov 2017 15:04:44 logging_test.py[line:20] DEBUG This is debug message
Fri, 10 Nov 2017 15:04:44 logging_test.py[line:21] INFO This is info message
Fri, 10 Nov 2017 15:04:44 logging_test.py[line:22] WARNING This is warning message
Fri, 10 Nov 2017 15:04:44 logging_test.py[line:23] ERROR This is error message
```

basicConfig函数参数：
```bash
filename: 指定日志文件名
filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
format: 指定输出的格式和内容，format可以输出很多有用信息，如上例所示:
     %(levelno)s: 打印日志级别的数值
     %(levelname)s: 打印日志级别名称
     %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
     %(filename)s: 打印当前执行程序名
     %(funcName)s: 打印日志的当前函数
     %(lineno)d: 打印日志的当前行号
     %(asctime)s: 打印日志的时间
     %(thread)d: 打印线程ID
     %(threadName)s: 打印线程名称
     %(process)d: 打印进程ID
     %(message)s: 打印日志信息
datefmt: 指定时间格式，同time.strftime()
level: 设置日志级别，默认为logging.WARNING
stream: 指定将日志的输出流，可以指定输出到sys.stderr,sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略
```

### StreamHandler
将日志同时输出控制台以及记录到文件中，可以使用StreamHandler函数创建一个输出到console的流。
```bash
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger=logging.getLogger('')
logger.addHandler(console)

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
```

### logging.conf配置文件
如果项目比较简单，以上的介绍已经足够使用了，但如果项目较大，建议使用配置文件的方式。

#### 创建一个配置文件logger.conf
```bash
###################### loggers #########################
[loggers]
keys=root,scan,heart

[logger_root]

handlers=hand_console,hand_file_scan
qualname=logger_root
propagate=0
level=INFO

[logger_scan]

handlers=hand_console,hand_file_scan
qualname=logger_scan
propagate=0
level=INFO

[logger_heart]

handlers=hand_console,hand_file_heart
qualname=logger_heart
propagate=0
level=INFO

####################### handlers ########################

[handlers]
keys=hand_console,hand_file_scan,hand_file_heart

[handler_hand_console]

class=StreamHandler
level=WARNING
formatter=form
args=(sys.stderr,)

[handler_hand_file_scan]

class=FileHandler
level=INFO
formatter=form
args=(os.getcwd()+"/log/"+time.strftime('%Y%m%d',time.localtime())+"/"+'scan.log', 'a')

[handler_hand_file_heart]

class=FileHandler
level=INFO
formatter=form
args=(os.getcwd()+"/log/"+time.strftime('%Y%m%d',time.localtime())+"/"+'heart.log', 'a')

##################### formatters ##########################

[formatters]

keys=form

[formatter_form]

format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s

datefmt=%Y-%m-%d %X

```
#### 加载使用配置文件
```bash
import logging
import logging.config

logging.config.fileConfig("logger.conf") # 加载配置文件

logger = logging.getLogger("logger_scan") # 选择logger为logger_scan
logger.info('This is info message')

logger = logging.getLogger("logger_heart") # 选择logger为logger_heart
logger.info('This is info message')

# 注意：logger_scan必须与配置文件中的名字一样，看到有些教程里面写的是scan，这是不对的，需要写全名。

```
说明：观察配置文件，可以看到loggers有三个，分别是root,scan,hearts；root是默认的，即config.fileConfig中不写表示选择root；然后scan logger 中的handlers是handler_console,handler_file_scan，说明这个logger有2个流，一个是输出到控制台的，一个是写入文件的。这几个handler中的formatter选项都一样，为formatter_form，即可以在这个选项中配置日志的格式。

#### handler配置说明
　　可以看到以上配置文件handler_console中的args参数，在console中使用sys.stderr，将会把输出到控制台；而另外2个handler的args参数的内容是文件地址，注意这个文件地址可以是静态地址，比如：test.log，也可以是动态生成的，比如上面使用当前日期生成的。之所以可以这么写，是因为配置文件将会被执行eval函数，因此可以在这个配置文件里面写python代码，将会被执行。
　　当然除了写入文件，输出到控制台外，logging还支持其他的日志记录方式，参考摘录自logging文档：
```bash
[handler_hand02]
class=FileHandler
level=DEBUG
formatter=form02
args=('python.log', 'w')

[handler_hand03]
class=handlers.SocketHandler
level=INFO
formatter=form03
args=('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)

[handler_hand04]
class=handlers.DatagramHandler
level=WARN
formatter=form04
args=('localhost', handlers.DEFAULT_UDP_LOGGING_PORT)

[handler_hand05]
class=handlers.SysLogHandler
level=ERROR
formatter=form05
args=(('localhost', handlers.SYSLOG_UDP_PORT), handlers.SysLogHandler.LOG_USER)

[handler_hand06]
class=handlers.NTEventLogHandler
level=CRITICAL
formatter=form06
args=('Python Application', '', 'Application')

[handler_hand07]
class=handlers.SMTPHandler
level=WARN
formatter=form07
args=('localhost', 'from@abc', ['user1@abc', 'user2@xyz'], 'Logger Subject')

[handler_hand08]
class=handlers.MemoryHandler
level=NOTSET
formatter=form08
target=
args=(10, ERROR)

[handler_hand09]
class=handlers.HTTPHandler
level=NOTSET
formatter=form09
args=('localhost:9022', '/log', 'GET')
```

### 参考文章
http://python.usyiyi.cn/translate/python_278/library/logging.config.html
https://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html
