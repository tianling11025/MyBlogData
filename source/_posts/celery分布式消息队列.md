---
title: celery分布式消息队列
copyright: true
permalink: 1
top: 0
date: 2017-08-25 17:58:59
tags:
- celery
categories: 编程之道 
password:
---
<blockquote class="blockquote-center">Quitters never win and winners never quit
退缩者永无胜利，胜利者永不退缩。</blockquote>
　　之前在分布式消息队列上我一直使用rabbitmq+pika组合，然而由于对rabbitmq与pika理解不深，因此使用过程中遇到了很多坑。直到最近我决定重新研究下分布式消息队列，当然这次抛弃了pika，而选用celery。
　　回想之前我对pika与celery有过一些疑问，两者有何区别？又有何相同点？经过几天的研究，目前总算是清晰了一点，因此在此对celery+rabbitmq做个记录。
<!--more-->

### 安装celery
```bash
pip install celery
```
说明：celery只支持python2.7及以上版本，建议在虚拟环境中安装，如何构造虚拟环境可参考：[python虚拟环境](https://thief.one/2017/08/24/2/)

### Celery是如何工作的？
我在此模拟几个角色来解释下celery+rabbitmq是如何工作的，脑洞来自网络，这里借鉴扩展一番。

假设目前D公司要开半年度工作会议，会议上要指定下半年工作计划，参会人员有老板（下发任务者）、部门主管（celery分配任务者）、部门员工（工作者）、老板秘书（沟通协调者，rabbitmq）。

#### 工作内容是什么？
　　那么这场会议首先需要确定的是下半年的具体工作内容，这里就称之为“任务内容”。比如老板说我们下半年要开发出一个大数据平台，部门主管举手称赞，表示赞同，于是便愉快地定下了我们具体的工作任务（task），当然开发一个平台算是这个项目的总任务，其中可以细分成很多小的任务，比如大数据算法怎么写？界面怎么设计等。

#### 工作者在哪里？
　　在确定了具体工作任务后，老板便把这个项目交给了部门主管（celery），而部门主管此时要确定谁去完成这项任务，它可以指定某个人（worker），也可以多个人。

#### 发布工作者在哪里？
　　毫无疑问发布工作任务的人是老板（下发任务者），他指定了部门主管（celery）什么时候去完成哪些任务，并要求获取反馈信息。但有一点需要注意，老板只管布置任务，但不参与具体的任务分配，那这个任务分配的功能交给谁，没错就是部门主管，即celery。

#### 老板与员工如何沟通项目？
　　项目之初，老板通过电话将任务传递给部门主管，部门主管通过部门会议将任务分配给员工，过段时间再将任务结果反馈给老板。然而随着任务越来越多，部门主管就发现了一个问题，任务太多了，每个任务还要反馈结果，记不住，也容易弄乱，导致效率下降。
　　在召开会议商量了一番后，老板秘书站起来说：“我有个提议，老板每天将布置的任务写成一张纸条放到我这，然后部门主管每天早上来取并交给员工，至于纸条上的任务如何分配，部门主管决定就行，但是要将结果同样写一张纸条反馈给我，我再交给老板。这样老板只负责下发任务，我只负责保管任务纸条，部门主管只负责分配任务并获取反馈，员工只负责按任务工作。大家职责都很明确，效率肯定会更高。”至此，老板与员工的沟通问题也解决了。

### 演示代码
celery_con.py
```bash
from celery import Celery
import time

app = Celery(backend='amqp', broker='amqp://guest:guest@127.0.0.1:5672')
```
说明：celery_con.py的作用是连接rabbitmq，注意这里是利用celery连接的rabbitmq。映射到场景中，就是秘书与主管，秘书与老板之间传递信息的通道。

task.py（任务内容）
```bash
from celery_con import app

@app.task
def test(x, y):
    time.sleep(5)
    return x + y


@app.task
def scan(x,y):
    time.sleep(1)
    return x-y

```
说明：task.py的功能是定制具体的任务，即“任务内容”，映射到场景中便是“开发一个大数据平台”，其中算法要怎么写？界面要如何设计等等。

celery（部门主管）
```bash
celery -A task worker -c 2
```
说明：此命令为开启work，分配任务；task就是task.py脚本的名称，表示work为task任务服务；-c 2表示同时开启2个work。映射到场景中，便是部门主管实时向秘书获取纸条，并分配给员工。

run.py（老板）
```bash
from task import test,scan

res=test.delay(2,2)
print res.get()
```
说明：run.py的作用是下发消息到rabbitmq队列中，映射到场景中即老板将任务写在纸条上交给秘书。

运行：
```bash
python run.py
```

而这里的秘书指的就是rabbitmq。

### celery与pika的区别
　　简单来说，pika其实就是用来连接rabbitmq服务的一个python客户端模块，而rabbitmq本身只有消息存储功能，并没有任务的分配调度。当然在用pika连接rabbitmq的过程也可以任务分配，这需要利用pika模块自己写一个调度代码，也就是相当于自己写一个celery模块。
　　celery就是用来分配任务的，主要是做异步任务队列的，但是celery不具备存储的功能，因此需要一种介质去存储消息，所以常常与rabbitmq一起用。

### celery高级用法
```bash
from task import scan

r=scan.s(2,2)
res=r.delay()
print res.get()
```
#### 并发下发任务
并发的下发任务，也可以使用for循环。这里指的并发，并不是所有任务一起执行，而是所有任务都下发到队列，而执行的并发数量，取决于work的数量。
```bash
from celery import group
from task import scan
g=group( scan.s(i,i) for i in range(10)).delay()
print g.get()
```
#### 指定下发的队列
有时候我们会遇到多个任务，而每个任务的执行对象不一样，因此需要创建不同的队列去存储任务，这时就需要我们在创建任务、消费任务时指定队列的名称。
##### 配置celery
celery_con.py
```bash
from celery import Celery

RABBITMQ_IP="127.0.0.1"
RABBITMQ_PORT="5672"
RABBITMQ_USER=""
RABBITMQ_PASS=""

app = Celery(
    backend='amqp', 
    broker='amqp://{}:{}@{}:{}'.format(
        RABBITMQ_USER,
        RABBITMQ_PASS,
        RABBITMQ_IP,
        RABBITMQ_PORT,
        ),
    CELERY_ROUTES = {
    'worker.test1': {'queue': 'test1'},
    'worker.test2': {'queue': 'test2'},
    'worker.test3': {'queue': 'test3'},
    },
    )

```
##### 指定任务内容
task.py
```bash
from celery_con import app
@app.task
def test(x, y):
    time.sleep(5)
    return x + y
@app.task
def scan(x,y):
    time.sleep(1)
    return x-y
```
##### 下发任务
push_task.py
```bash
from celery import group
from task import scan
g=group( scan.s(i,i) for i in range(10)).apply_async(queue='test1')
print g.get()
```
说明：下发任务时，将会把任务存入rabbitmq的test1队列中。

##### 启动work处理任务
celery_start_work.sh
```bash
celery -A task worker --queue=test1
```
说明：worker工作者将会从rabbitmq的test1队列中获取数据。


*以上内容是个人理解的celery用法以及一些原理，如有谬误，欢迎指正，谢谢！*













