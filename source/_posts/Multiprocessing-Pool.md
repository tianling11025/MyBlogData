---
title: 【Multiprocessing系列】Pool
date: 2016-11-24 09:44:56
comments: true
tags: 
- python
- Multiprocessing
- 多进程
categories: 编程之道
password:
copyright: true
---

　　Multiprocessing.Pool可以提供指定数量的进程供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来执行它。在共享资源时，只能使用Multiprocessing.Manager类，而不能使用Queue或者Array。

#### Pool介绍

##### 用途
Pool类用于需要执行的目标很多，而手动限制进程数量又太繁琐时，如果目标少且不用控制进程数量则可以用[Process](http://thief.one/2016/11/24/Multiprocessing-Process)类。

##### 构造方法
* Pool([processes[, initializer[, initargs[, maxtasksperchild[, context]]]]])
* processes ：使用的工作进程的数量，如果processes是None那么使用 os.cpu_count()返回的数量。
* initializer： 如果initializer是None，那么每一个工作进程在开始的时候会调用initializer(*initargs)。
* maxtasksperchild：工作进程退出之前可以完成的任务数，完成后用一个新的工作进程来替代原进程，来让闲置的资源被释放。maxtasksperchild默认是None，意味着只要Pool存在工作进程就会一直存活。
* context: 用在制定工作进程启动时的上下文，一般使用 multiprocessing.Pool() 或者一个context对象的Pool()方法来创建一个池，两种方法都适当的设置了context。

##### 实例方法
* apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞。
* apply(func[, args[, kwds]])是阻塞的。
* close()    关闭pool，使其不在接受新的任务。
* terminate()    关闭pool，结束工作进程，不在处理未完成的任务。
* join()    主进程阻塞，等待子进程的退出， join方法要在close或terminate之后使用。

#### Pool使用方法

##### Pool+map函数

说明：此写法缺点在于只能通过map向函数传递一个参数。

```bash
from multiprocessing import Pool

def test(i):
    print i

if __name__=="__main__":
	lists=[1,2,3]
	pool=Pool(processes=2) #定义最大的进程数
	pool.map(test,lists)        #p必须是一个可迭代变量。
	pool.close()
	pool.join()
```

##### 异步进程池（非阻塞）

```bash
from multiprocessing import Pool

def test(i):
    print i

if __name__=="__main__":
	pool = Pool(processes=10)
	for i  in xrange(500):
		'''
		For循环中执行步骤：
		（1）循环遍历，将500个子进程添加到进程池（相对父进程会阻塞）
		（2）每次执行10个子进程，等一个子进程执行完后，立马启动新的子进程。（相对父进程不阻塞）
		
		apply_async为异步进程池写法。
		异步指的是启动子进程的过程，与父进程本身的执行（print）是异步的，而For循环中往进程池添加子进程的过程，与父进程本身的执行却是同步的。
		'''
	    pool.apply_async(test, args=(i,)) #维持执行的进程总数为10，当一个进程执行完后启动一个新进程.       

	print “test”
	pool.close()
	pool.join()
```

执行顺序：For循环内执行了2个步骤，第一步：将500个对象放入进程池（阻塞）。第二步：同时执行10个子进程（非阻塞），有结束的就立即添加，维持10个子进程运行。（apply_async方法的会在执行完for循环的添加步骤后，直接执行后面的print语句，而apply方法会等所有进程池中的子进程运行完以后再执行后面的print语句）

注意：调用join之前，先调用close或者terminate方法，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束。


##### 同步进程池（阻塞）

```bash
from multiprocessing import Pool

def test(p):
       print p
       time.sleep(3)

if __name__=="__main__":
	pool = Pool(processes=10)
	for i  in xrange(500):
	'''
	实际测试发现，for循环内部执行步骤：
	（1）遍历500个可迭代对象，往进程池放一个子进程
	（2）执行这个子进程，等子进程执行完毕，再往进程池放一个子进程，再执行。（同时只执行一个子进程）
	for循环执行完毕，再执行print函数。
	'''
	    pool.apply(test, args=(i,))   #维持执行的进程总数为10，当一个进程执行完后启动一个新进程.

	print “test”
	pool.close()
	pool.join()
```

说明：for循环内执行的步骤顺序，往进程池中添加一个子进程，执行子进程，等待执行完毕再添加一个子进程.....等500个子进程都执行完了，再执行print "test"。（从结果来看，并没有多进程并发）


### 传送门

>[【Multiprocessing系列】共享资源](http://thief.one/2016/11/24/Multiprocessing%E5%85%B1%E4%BA%AB%E8%B5%84%E6%BA%90/)
[【Multiprocessing系列】子进程返回值](http://thief.one/2016/11/24/Multiprocessing%E5%AD%90%E8%BF%9B%E7%A8%8B%E8%BF%94%E5%9B%9E%E5%80%BC/)
[【Multiprocessing系列】Pool](http://thief.one/2016/11/24/Multiprocessing-Pool/)
[【Multiprocessing系列】Process](http://thief.one/2016/11/24/Multiprocessing-Process/)
[【Multiprocessing系列】Multiprocessing基础](http://thief.one/2016/11/23/Python-multiprocessing/)