---
title: Python魔术方法
copyright: true
permalink: 1
top: 0
date: 2017-11-22 17:31:01
tags:
- python
categories: 编程之道
password:
---
<blockquote class="blockquote-center">一杯敬朝阳，一杯敬月光</blockquote>
　　所谓魔术方法，就是在自定义类中定义一些"不一般"的方法，使类的封装更完善功能更健全，是一种python特有的方法。它们的方法名一般是`__xx__`这样的格式，比如最常见的`__init__`，就是一种魔术方法。下面我介绍一些在定义类中常见的魔术方法，并附上测试代码，请各位自行体验一下其美妙的魔术魅力吧。
<!--more-->
## 魔术方法
```bash
#! -*- coding:utf-8 -*-

class ClassTest(object):
   
    def __new__(cls,*args,**kwargs):
        ''' 初始化操作，类实例化时第一个被调用的方法

        与__init__方法一起构成构造函数
        

        '''
        return object.__new__(cls)
   
    
    def __init__(self, _list=["1","2","3","4","5"] , _dict={"a":1,"b":2}):
        ''' 初始化操作 '''

        self._list = _list
        self._dict = _dict


    def __del__(self):
        ''' 删除变量 '''

        del self._list
        del self._dict

    def __call__(self, item):
        '''
        Usage:
            >>>>func=ClassTest()
            >>>>print func("nmask")
            >>>>nmask
        '''

        return item
 
    def __len__(self):
        ''' 返回对象的长度 
        
        Usage:
            >>>>print len(ClassTest())
            >>>>5

        '''

        return len(self._list)
 
    def __getitem__(self, key):
        ''' 通过下标取出对象的值 

        Usage:
            >>>print ClassTest()["a"]
            >>>1
        '''
        if key not in self._dict:

            return self.__missing__(key)

        return self._dict[key]

    def __missing__(self,key):
        ''' 当key不在dict中被调用 '''

        return "%s is not in dict" % key
 
    def __setitem__(self, key, value):
        ''' 设置对象的值 
        
        Usage:
            ClassTest()['a']='12345'
        '''

        self._dict[key] = value
 
    def __delitem__(self, key):
        ''' 删除对象 '''

        del self._dict[key]

    def __getattr__(self, item):
        '''当访问对象不存在的属性时，调用此类

        Usage:
            >>>ClassTest().abc

        '''

        return "class is not exists %s method" % item

    def __contains__(self, item):
        ''' not in or in 判断元素是否在其中

        Usage:
            >>>if "1" in ClassTest()
            >>>
        '''

        return item in self._list


    def __iter__(self):
        ''' 创建一个迭代器 

        Usage:
            >>>for i in ClassTest():
            >>>     print i
        '''

        return iter(self._list)
 
    def __reversed__(self):
        ''' 反转列表 
        
        Usage:
            >>>for i in reversed(ClassTest()):
            >>>     print i
        '''

        return reversed(self._list)

    def __str__(self):
        '''用于处理打印实例本身的时候的输出内容,默认为对象名称和内存地址

        Usage:
            >>>print ClassTest()
        '''

        return "This is a Test Class for Python Magic Method"

    def __repr__(self):
        ''' 序列化对象 

        Usage:
            >>>repr(ClassTest())

        '''

        return repr(self._dict)


    def run(self):

        return self._dict


if __name__=="__main__":

    if "1" in ClassTest():
        print "调用了类的__contains__方法：1 is in _list"

    print "调用了类的__missing__方法：",ClassTest()["aaa"]

    for i in reversed(ClassTest()):
        print "调用了类的__iter__方法：",i

    print "调用了类的__getattr__方法：",ClassTest().abc

    print "调用了类的__repr__方法：",repr(ClassTest())

    print "调用了类的__str__方法：",ClassTest()

    print "调用了类的__len__方法：",len(ClassTest())

    print "调用了类的__setitem__方法：ClassTest()['a']='12345'"

    ClassTest()["a"]="12345"

    print "调用了类的__getitem__方法：",ClassTest()["a"]
    
    for i in ClassTest():
        print "调用了类的__iter__方法：",i

```
运行结果：
```bash
调用了类的__contains__方法：1 is in _list
调用了类的__missing__方法： aaa is not in dict
调用了类的__iter__方法： 5
调用了类的__iter__方法： 4
调用了类的__iter__方法： 3
调用了类的__iter__方法： 2
调用了类的__iter__方法： 1
调用了类的__getattr__方法： class is not exists abc method
调用了类的__repr__方法： {'a': 1, 'b': 2}
调用了类的__str__方法： This is a Test Class for Python Magic Method
调用了类的__len__方法： 5
调用了类的__setitem__方法：ClassTest()['a']='12345'
调用了类的__getitem__方法： 12345
调用了类的__iter__方法： 1
调用了类的__iter__方法： 2
调用了类的__iter__方法： 3
调用了类的__iter__方法： 4
调用了类的__iter__方法： 5
```
更多魔术方法，参考：http://python.jobbole.com/88367/