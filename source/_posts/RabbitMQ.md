---
title: RabbitMQ+Pika
date: 2017-04-06 10:36:47
comments: true
tags: 
- RabbitMQ
- pika
categories: 编程之道
password:
copyright: true
---
<blockquote class="blockquote-center">如何看待“年轻时就释怀与淡泊，是没有希望的”这句话？
试图用一句话就来总结复杂的人生，是没有希望的</blockquote>
MQ全称为Message Queue,消息队列（MQ）是一种应用程序对应用程序的通信方法，是消费-生产者模型的一个典型的代表。在python中，线程间通信可以使用Queue，进程间通信可以使用multiprocessing.Queue，然而不同服务器之间通信便可以使用MQ，本文用于记录MQ的安装使用过程。
<!--more -->
### Rabbitmq安装
首先需要按照rabbitmq服务，可以在本地装，也可以在远程服务器上安装。
#### ubuntu下安装
```bash
sudo apt-get install rabbitmq-server
```
安装后，rabbitmq服务就已经启动了。
详细参考：http://www.rabbitmq.com/download.html（官网）

#### centos下安装
安装Erlang语言：
```bash
yum install erlang
```
安装Rabbitmq：
```bash
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.3.5/rabbitmq-server-3.3.5-1.noarch.rpm
yum install rabbitmq-server-3.3.5-1.noarch.rpm
```
加入开机启动服务
```bash
chkconfig rabbitmq-server on
```
然后启动
```bash
service rabbitmq-server start
service rabbitmq-server status
service rabbitmq-server stop
service rabbitmq-server restart
```
开启web插件：
```bash
rabbitmq-plugins enable rabbitmq_management
```
访问http://localhost:15672

但是此时，guest用户登录不了，因为默认是不允许guest用户登录的，解决方案可以是创建一个新的用户：
```bash
rabbitmqctl delete_user  guest
rabbitmqctl add_user admin 123456
rabbitmqctl set_user_tags admin administrator
```
当然也可以为guest添加权限，使其可以登陆：
```bash
[{rabbit, [{loopback_users, []}]}] #编辑rabbitmq配置文件，删除这一行中的guest
```
centos安装rabbitmq参考：http://www.qaulau.com/linux-centos-install-rabbitmq/

### Rabbitmq配置
#### rabbitmq命令
```bash
rabbitmqctl status  查看运行状态
rabbitmqctl list_queues  查看队列情况
rabbitmq-plugins enable rabbitmq_management 开启插件（不然网页管理界面打不开）
sudo rabbitmq-server 运行以后访问http://127.0.0.1:15672
sudo rabbitmq-server -detached 运行
sudo rabbitmqctl stop  结束
rabbitmqctl reset  清除所有队列 (要先关闭)
```
#### 配置rabbitmq
```bash
$ sudo rabbitmqctl add_user myuser mypassword
$ sudo rabbitmqctl add_vhost myvhost
$ sudo rabbitmqctl set_user_tags myuser mytag
$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```
#### rabbitmq更改WEB插件端口
安装完rabbitmq后，/usr/share/doc/rabbitmq-server-3.5.6目录下默认会有一个配置文件模版rabbitmq.config.example。

##### 复制配置文件到/etc/rabbitmq目录下
```bash
cp /usr/share/doc/rabbitmq-server-3.5.6/rabbitmq.config.example /etc/rabbitmq/
```
##### 更改配置文件名字
```bash
cd /etc/rabbitmq/
mv rabbitmq.config.example rabbitmq.config
```
##### 编辑配置文件
vim rabbitmq.config
```bash
{rabbitmq_management,
  [
{listener, [{port,     8080},
             {ip,       "0.0.0.0"},
             {ssl,     false}
]},
```
说明：可以用"?rabbitmq_management"定位到这一行，然后%%是注释的意思，将%%删除，整个rabbitmq_management字典写成上面的内容。rabbitmq配置文件可以设置很多东西，默认是没有的，建议创建起来。

##### 重启rabbitmq
```bash
Service rabbitmq-server restart 
```
重启服务，如果报错，则查看日志文件：cat /var/log/rabbitmq/startup_err。

### Rabbitmq报错处理
#### [Errno 104] Connection reset by peer
在连接rabbitmq时报此错误，说明该用户与虚拟目录的权限不够，解决方案：
（1）查看已经存在的虚拟目录：
```bash
rabbitmqctl list_vhosts
```
（2）将用户与虚拟目录绑定且设定权限，如：
```bash
rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
```
默认情况下就一个vhost，即／，当然也可以自己添加，然后跟用户绑定：
```bash
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```
#### ERROR: epmd error for host nmask: timeout (timed out)
在启动rabbitmq时报这个错，则需要更改/etc/hosts文件，因为造成这个错误的原因是找不到host，绑定一下即可。
比如，在/etc/host文件添加：
```bash
127.0.0.1 nmask
```
#### ** WARNING ** Mnesia is overloaded: {dump_log, write_threshold}
字面理解这个错误是过载，异步写入太频繁，会导致rabbitmq本崩溃退出。解决方案主要有2种：修改rabbitmq配置文件、升级erlang版本。
##### 修改rabbitmq配置文件
在配置文件中添加：
```bash
{mnesia, [{dump_log_write_threshold, 50000},{dc_dump_limit,40}]},
```
最终效果如下：
```bash
[
{mnesia, [{dump_log_write_threshold, 50000},{dc_dump_limit,40}]},
 {rabbit,
  [
```
说明：但我尝试发现还是不能解决问题。

##### 升级erlang
实际测试发现升级erlang可以解决此类问题。

### Client Usage
接下来可以在两台不同的PC上，运行两段代码，一段用来向rabbitmq队列中发送消息，另一段用来获取消息。
#### rabbitmq for python
python中来用连接操作rabbitmq服务的库有pika、txAMQP、py-amqplib，celery等，这里主要介绍下pika。

### Rabbitmq+pika
pika是python中用来连接rabbitmq服务端的第三方库。
pika文档：http://pika.readthedocs.io/en/latest/examples/blocking_consume.html

#### 安装pika
```bash
pip install pika
```
#### pika Usage
先搭建一个rabbitmq服务器用来存储消息队列，然后利用pika来存放获取队列中的任务，pika分为生产者与消费者模式.
##### 生产者代码
```bash
import pika
'''
生产者模式代码，向rabbitmq消息队列中存放消息（任务）
'''
credentials = pika.PlainCredentials("test", "test")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.1.2',virtual_host="/",credentials=credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2')) #链接rabbitmq服务器,端口可以不写。
channel = connection.channel()

#声明消息队列，消息将在这个队列中进行传递。
channel.queue_declare(queue='hello')#申明hello队列，如果该队列不存在，则自动创建。

#发送消息到hello队列中，若队列不存在，则自动清除这些消息。
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
#exchange表示交换器，能精确指定消息应该发送到哪个队列,routing_key设置为队列的名称，body就是消息内容。
print " [x] Sent 'Hello World!'"
connection.close() #关闭连接
'''
rabbitmq服务器可以用rabbitmqctl list_queues来查看队列情况
'''
```
##### 消费者代码
```bash
import pika
'''
消费者模式代码，从rabbitmq消息队列中取出消息（任务）
'''
credentials = pika.PlainCredentials("test", "test")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.1.2',virtual_host="/",credentials=credentials)) #链接rabbitmq服务器,端口可以不写。
channel = connection.channel()

#声明消息队列，消息将在这个队列中进行传递。
channel.queue_declare(queue='hello')

#定义回调函数来处理接受到的消息
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

#告诉rabbitmq使用callback来接受消息
channel.basic_consume(callback, queue='hello', no_ack=True)
print ' [*] Waiting for messages. To exit press CTRL+C'
#开始接受消息，并进入阻塞状态，队列里有消息才会调用callback进行处理，按ctrl+c退出。
channel.start_consuming()
```
以上两段代码为最简单的生产者与消费者，没有涉及到持久化存储以及消息返回等内容。

#### 消息确认
当一个正在执行的消费者中断了，则需要返回消息，告诉rabbitmq重新将其分配给其他消费者。
```bash
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(5)
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)
```
然后修改no_ack为False
```bash
channel.basic_consume(callback, queue='hello', no_ack=False)
```
　　如果消息不确认，rabbitmq默认是没有超时时间的概念，即只要客户端连接不中断就会一直等待ack确认消息，那么此任务将会阻塞。针对这种情况，我们可以在程序中手动确认消息，即利用上面的代码。但如果程序在运行过程中出错，我们必须将此任务重新放回队列重新取出执行，则要用到channel.basic_nack(delivery_tag = method.delivery_tag)方法，可以实现将任务重新放回队列。
#### 消息持久化存储
　　虽然有了消息反馈机制，但是如果rabbitmq自身挂掉的话，那么任务还是会丢失。所以需要将任务持久化存储起来。
```bash
channel.queue_declare(queue='hello', durable=True)
但是这个程序会执行错误，因为hello这个队列已经存在，并且是非持久化的，rabbitmq不允许使用不同的参数来重新定义存在的队列。重新定义一个队列：
channel.queue_declare(queue='task_queue', durable=True)
在发送任务的时候，用delivery_mode=2来标记任务为持久化存储：
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
```
#### 公平调度
　　上面实例中，虽然每个工作者是依次分配到任务，但是每个任务不一定一样。可能有的任务比较重，执行时间比较久；有的任务比较轻，执行时间比较短。如果能公平调度就最好了，使用basic_qos设置prefetch_count=1，使得rabbitmq不会在同一时间给工作者分配多个任务，即只有工作者完成任务之后，才会再次接收到任务。
```bash
channel.basic_qos(prefetch_count=1)
```
### pika vs celery
　　celery用来分配任务的，主要是做异步任务队列的。
　　pika+rabbitmq主要是用来消息的收发功能，并不带有任务分配功能。比如说我们有很多台机器需要去rabbitmq服务器消息队列中取任务，任务怎么分配，pika应该做不到。pika只能做到消息的发送，以及消息的获取。又或者说pika其实就是用来使用rabbitmq的一个客户端，本身只是消息存储功能，并没有任务的分配等。如果需要此功能，就需要理由pika模块自己写一个调度方案，相当于自己写一个celery模块。

### Rabbitmq任务调度问题
首先，Rabbitmq任务调度应该是阻塞的，看代码：
```bash
import pika
import time
'''
消费者模式代码，从rabbitmq消息队列中取出消息（任务）
'''
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2')) #链接rabbitmq服务器,端口可以不写。
channel = connection.channel()

#声明消息队列，消息将在这个队列中进行传递。
channel.queue_declare(queue='hello')

#定义回调函数来处理接受到的消息
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    #ch.basic_ack(delivery_tag = method.delivery_tag) ##消息确认，告诉队列这个任务做完了

#告诉rabbitmq使用callback来接受消息
channel.basic_qos(prefetch_count=10) #最多只会让消费者同时做10个任务
channel.basic_consume(callback, queue='hello')
print ' [*] Waiting for messages. To exit press CTRL+C'
#开始接受消息，并进入阻塞状态，队列里有消息才会调用callback进行处理，按ctrl+c退出。
channel.start_consuming()
```
运行结果：每隔1s输出一个hello world，输出10个后停止。

　　我们把ch.basic_ack(delivery_tag = method.delivery_tag)注释去掉，再运行.
　　每隔1s输出一个hello world ，不会停止。可以看到的是prefetch_count=10，也就是说可以同时执行10个任务，然而结果是并没有并发执行，而是单线程执行的，也就是说是一个任务一个任务执行的。
　　ch.basic_ack(delivery_tag = method.delivery_tag)的作用在于告诉队列，单个任务已经执行完，也就是说如果不回复，那么队列认为此任务还没做完，累计到10个任务后，达到了同时执行的最大任务量，因此便不会再下派任务。

　　那么加上消息确认，为何也没有达到10个任务并发执行呢？

　　我的猜想是，rabbitmq本身并不是异步的（是阻塞的），也没有并发的功能，想要实现并发，需要自己写程序解决。修改代码，我们再看看.
```bash
import pika
import time
import threading
'''
消费者模式代码，从rabbitmq消息队列中取出消息（任务）
'''
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2')) #链接rabbitmq服务器,端口可以不写。
channel = connection.channel()

#声明消息队列，消息将在这个队列中进行传递。
channel.queue_declare(queue='hello')

def test(ch,method,body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    ch.basic_ack(delivery_tag = method.delivery_tag) ##消息确认，告诉队列这个任务做完了

#定义回调函数来处理接受到的消息
def callback(ch, method, properties, body):
    t=threading.Thread(target=test,args=(ch,method,body)) #多线程
    t.start()

#告诉rabbitmq使用callback来接受消息
channel.basic_qos(prefetch_count=2) #最多只会让消费者同时做10个任务
channel.basic_consume(callback, queue='hello')
print ' [*] Waiting for messages. To exit press CTRL+C'
#开始接受消息，并进入阻塞状态，队列里有消息才会调用callback进行处理，按ctrl+c退出。
channel.start_consuming()
```
运行结果：每隔1s，并发输出2个hello world，确实达到了并发的效果，然后并发的数量取决于prefetch_count=2的设置。

　　那么我们可以得出结论，从rabbitmq队列取出数据本身是阻塞的，没有达到并发，但是通过设置prefetch_count=2以及编写多线程函数，还是可以达到并发的效果。（prefetch_count 不设置，默认应该是没有上限）

### Rabbitmq并发调度问题
Rabbitmq取任务本身不是并发的，但可以结合多线程、协程、多进程达到并发的效果。

@更新于2017年5月9日：
*以下并发方式并不适用于pika，因为其在一个blocking_connection中不支持并发，这里当做错误示范保留。如果需要并发，可以把多线程写在每个连接外面，即每个线程都去连接队列，达到并发收取队列任务的效果。*

#### 多线程
代码：
```bash
import pika
import time
import threading
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def test(ch,method,body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def callback(ch, method, properties, body):
    t=threading.Thread(target=test,args=(ch,method,body))
    t.start()

channel.basic_qos(prefetch_count=2)
channel.basic_consume(callback, queue='hello')
channel.start_consuming()
```
　　代码中定义的回调函数是一个多线程启动器，任务发给回调函数，回调函数会将它以多线程的形式传递给test函数，执行输出。并发的数量取决于prefetch_count=2，这代表同时执行任务的最大数量。

#### 协程
代码：
```bash
import pika
import time
import gevent
from gevent import monkey;monkey.patch_all()

connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def test(ch,method,body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def callback(ch, method, properties, body):
    gevent.spawn(test,ch,method,body) #协程启动，没有调用join，因为rabbitmq本身是阻塞的,可以不用join

channel.basic_qos(prefetch_count=2) #并发的数量
channel.basic_consume(callback, queue='hello')
channel.start_consuming()
```
#### 多进程
代码：（只能在linux下使用）
```bash
import pika
import time
from multiprocessing import Process

connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.1.2'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def test(ch,method,body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def callback(ch, method, properties, body):
    t=Process(target=test,args=(ch,method,body))
    t.start()

channel.basic_qos(prefetch_count=2) #并发的进程数量
channel.basic_consume(callback, queue='hello')
channel.start_consuming()
```

*本文所写内容，均为本人测试后所得，如有错误，欢迎指正，谢谢！*







