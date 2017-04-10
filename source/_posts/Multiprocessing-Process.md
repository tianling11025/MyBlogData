---
title: 【Multiprocessing系列】Process
date: 2016-11-24 09:11:50
comments: true
tags: 
- python
- Multiprocessing
- 多进程
categories: 编程之道
---

　　利用multiprocessing.Process对象可以创建一个进程，该Process对象与Thread对象的用法相同，也有start(), run(), join()等方法。Process类适合简单的进程创建，如需资源共享可以结合multiprocessing.Queue使用；如果想要控制进程数量，则建议使用进程池[Pool](http://thief.one/2016/11/24/Multiprocessing-Pool)类。
#### Process介绍

##### 构造方法：
* Process([group [, target [, name [, args [, kwargs]]]]])
* group: 线程组，目前还没有实现，库引用中提示必须是None；
* target: 要执行的方法；
* name: 进程名；
* args/kwargs: 要传入方法的参数。

##### 实例方法：
* is_alive()：返回进程是否在运行。
* join([timeout])：阻塞当前上下文环境的进程程，直到调用此方法的进程终止或到达指定的timeout（可选参数）。
* start()：进程准备就绪，等待CPU调度。
* run()：strat()调用run方法，如果实例进程时未制定传入target，这star执行t默认run()方法。
* terminate()：不管任务是否完成，立即停止工作进程。

##### 属性：
* authkey
* daemon：和线程的setDeamon功能一样（将父进程设置为守护进程，当父进程结束时，子进程也结束）。
* exitcode(进程在运行时为None、如果为–N，表示被信号N结束）。
* name：进程名字。
* pid：进程号。


#### 创建多进程的两种方法

Process类中，可以使用两种方法创建子进程。

##### 使用Process创建子进程

说明：用法与Threading相似

```bash
from multiprocessing import Process  #导入Process模块 
import os  

def test(name):
	'''
	函数输出当前进程ID，以及其父进程ID。
	此代码应在Linux下运行，因为windows下os模块不支持getppid()
	'''
    print "Process ID： %s" % (os.getpid())  
    print "Parent Process ID： %s" % (os.getppid())  


if __name__ == "__main__": 
	'''
	windows下，创建进程的代码一下要放在main函数里面
	''' 
    proc = Process(target=test, args=('nmask',))  
    proc.start()  
    proc.join()  
```

##### 使用Process类继承创建子进程

说明：通过继承Process类，修改run函数代码。

```bash
from multiprocessing import Process
import time

class MyProcess(Process):
'''
继承Process类，类似threading.Thread
'''
    def __init__(self, arg):
        super(MyProcess, self).__init__()
        #multiprocessing.Process.__init__(self)
        self.arg = arg

    def run(self):
    '''
    重构run函数
    '''
        print 'nMask', self.arg
        time.sleep(1)

if __name__ == '__main__':
    for i in range(10):
        p = MyProcess(i)
        p.start()
    for i in range(10):
    	p.join()
```

### 传送门

>[【Multiprocessing系列】共享资源](http://thief.one/2016/11/24/Multiprocessing%E5%85%B1%E4%BA%AB%E8%B5%84%E6%BA%90/)
[【Multiprocessing系列】子进程返回值](http://thief.one/2016/11/24/Multiprocessing%E5%AD%90%E8%BF%9B%E7%A8%8B%E8%BF%94%E5%9B%9E%E5%80%BC/)
[【Multiprocessing系列】Pool](http://thief.one/2016/11/24/Multiprocessing-Pool/)
[【Multiprocessing系列】Process](http://thief.one/2016/11/24/Multiprocessing-Process/)
[【Multiprocessing系列】Multiprocessing基础](http://thief.one/2016/11/23/Python-multiprocessing/)