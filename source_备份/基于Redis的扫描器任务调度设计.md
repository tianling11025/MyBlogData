---
title: 基于Redis的扫描器任务调度设计方案
copyright: true
permalink: 1
top: 0
date: 2018-08-15 14:54:07
tags:
- 扫描器
- redis
categories: 编程之道
password:
---
<blockquote class="blockquote-center">这是我父亲 日记里的文字
这是他的生命 留下来的散文诗</blockquote>
　　最近在研究扫描器任务调度相关的东西，几番折腾后有些个人心得，心想需记录下来，避免遗忘，也当作是一种积累。之前我开发过几款扫描器（甲方内部使用），架构一直沿用：mysql（DB）+ rabbitmq（QUEUE）+ celery（调度）+ supervisor（进程监控）+ python（编程语言）。在经过一段时间的使用测试后，深感rabbitmq作为队列其架构还是过于厚重，不太适合扫描器一类的项目。当然并不是说rabbitmq就完全不适合作为扫描器的队列，而是我们应当寻求更简便的方案。
<!-- more -->
　　在研究了几款开源队列产品后，我决定在最新版的扫描器中放弃沿用之前的架构，转而使用redis作为队列存储。原因主要有几点：1、redis使用简单 2、redis比较轻量 3、redis可以满足功能需求。熟悉redis的朋友可能知道它是一款开源的key-value存储系统，常常用作数据缓存服务，那么如何使它在扫描器架构中提供一个队列服务呢？

　　首先需要思考一下，扫描器架构中的队列服务或者说任务调度服务，需要满足哪些功能？第一：控制扫描QPS，第二：任务优先级控制，第三：任务状态ACK确认（丢失重扫），第四：任务指定Agent扫描。

　　简单解释一下，如果您的扫描器针对甲方，那么控制扫描QPS是非常重要的，因为有些业务有qps要求，胡乱扫描可能会被怼。控制任务优先级就不用多说了，比如针对某个最新漏洞的应急扫描，此任务必须优先，因为需要赶在漏洞被利用之前发现并修复（时间就是kpi）。任务状态ACK也好理解，比如某个节点在扫描过程中异常，导致扫描数据丢失，那么需要将此任务重新放回队列扫描。任务指定扫描agent需求，这个可能比较模糊我解释一下，在甲方公司，资产覆盖办公网、生产网、外网边界等，各个机房的网络还可能不通，因此扫描Agent需要覆盖到各类环境，比如办公服务器、生产网服务器，甚至各个机房服务器都需要部署。那么在添加一个扫描任务时，就需要指定这个任务需要在哪个网络环境下的节点进行扫描，因此任务指定Agent扫描需求也是必须要实现的。

　　需求设计好了，那么如何实现呢？我们知道redis是一款key-value形式的存储系统，如果需要提供像rabbitmq那样的队列服务，就需要使用redis的一个特殊数据结构--列表。redis中的列表可以实现任务的插入、取出，可简单实现队列存储功能，其次列表可以左、右插入，也可以左、右取出，据此可以实现任务优先级控制。那么如何实现控制QPS、实现任务状态ACK、实现指定Agent扫描？这些功能比较复杂，不单单是靠redis就可以实现的，因此接下来我要重点谈谈如何实现以上这三个功能。

#### 任务调度架构
任务调度部分整体架构，包含：Mysql、控制中心、REDIS、API、Agent
![](/upload_image/20180815/1.png)
上图中的描述写得比较粗糙，可以直接往下看。

重点内容！！！：*一个agent在redis中对应唯一一个agent列表，用来存放任务公共信息；一个task在redis中对应唯一一个task列表用来存在任务扫描数据，以及对应唯一一个task ack列表，用来存放将要ack确认的数据（包含时间戳）。*

##### MYSQL+控制中心+REDIS
来看下MYSQL+控制中心+REDIS这一部分：
![](/upload_image/20180815/2.png)
说明：这一部分实现的功能主要是：1)循环监听数据库中最新添加的任务，将其插入到指定的redis列表中；2）循环监听redis task列表，若task列表以及task_ack列表都为空，则删除agent列表中对应的任务公共信息；3）遍历task_ack列表，获取数据（包含时间戳），判断是否ack超时，若超时则将该数据重新插入task列表（这里可以设置超时次数阈值，超过上限则丢弃数据）。

###### 执行流程
控制中心将最新任务插入redis过程：

* 控制中心遍历mysql的task表，获取最新的任务信息，该任务信息包含任务ID以及任务环境等参数，可用其对应agent表中的一批Agent（比如任务网络环境为办公网，则该任务可分配给所有办公网agent；若任务指定了agent个数，则可选择分配给部分agent，这也就是实现了控制QPS）。
* 控制中心获取任务数据以及对应的agent数据后，将任务数据中的公共信息插入redis中对应的agent列表（一个任务公共信息可能插入多个agent列表，由此来控制此任务由哪些agent扫描）；将任务扫描数据插入redis中对应的task列表。

控制中心将任务从redis中删除过程：

* 控制中心遍历redis中的task表，若task表为空，则判断对应的task_ack表状态，若也为空，则删除所有agent列表中包含该任务的公共信息。

##### REDIS+API+AGENT
来看下REDIS+API+AGENT这一部分架构：
![](/upload_image/20180815/3.png)
说明：这一部分实现的功能主要是：1）agent通过api获取对应的任务数据，任务数据包含：1、任务公共信息2、任务扫描数据；2）agent通过api进行任务ack确认。

###### 执行流程
Agent_01请求API获取任务信息过程：

* agent请求API的时候，带上了自己的agent_id，比如：01
* api从REDIS中的agent_01_list列表中获取一个任务的公共信息（注意这里是获取任务公共信息，并不是pop，即数据不会从列表中删除）
* api从任务公共信息中获取该任务的任务ID，比如：001
* api通过任务ID从对应的任务列表task_001_list中pop出扫描数据，与此同时将该扫描数据插入任务ack列表task_ack_001_list中。

Agent_01请求API进行任务ACK确认过程：

* agent请求API的时候，带上了任务ID，比如：001；以及任务扫描数据，比如：thief.one
* api从对应的任务ack列表task_ack_001中删除该扫描数据，thief.one。

#### 实现控制QPS
　　回顾一下前文中描述的，控制中心将任务信息插入到redis列表中的过程，即可以根据任务参数选择对应的agent数量，每个agent的扫描qps相对是固定的，因此用控制单个任务的agent数量，来控制此任务的扫描QPS。

#### 实现任务状态ACK
　　回顾一下前文中描述的，agent请求api获取任务信息，以及进行任务ack确认过程，即api从任务列表中取出（pop）一个数据的同时，将该数据插入任务ack列表中。当任务扫描完成后，再通过api将此数据从任务ack列表中删除。控制中心认为任务列表以及任务ack列表都为空时，此任务才算正真扫描完，事实也应该如此。

#### 实现指定Agent扫描
　　回顾一下前文中描述的，控制中心将任务信息插入到redis列表中的过程，任务在添加到mysql中时可以附带很多参数，比如网络环境、qps数量、扫描插件等等，那么网络环境参数就决定了此任务只能分配给对应网络环境的agent进行扫描。

#### 后文
　　前文介绍了一些基于redis实现的扫描器调度设计方案，当然这只是个人根据实践得出的方案，尚不够成熟，并且很多实现过程中的细节无法一一详细描述。只能说，很多时候需要靠实践中摸索出一条通往光明的道路。


*啦啦啦，如果对本文介绍的执行过程或者设计方案不明确，可回过头看下我强调的重点内容（自己找找），结合起来思考一下*















