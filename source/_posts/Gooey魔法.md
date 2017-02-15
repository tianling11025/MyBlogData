---
title: Gooey魔法
date: 2017-02-15 18:47:08
tags: Gooey
categories: 编程之道
---
　　Gooey是python的一个扩展模块，能够使用一条命令，将命令行程序变成一个 GUI 程序。它能够解析argparse模块的命令行参数，将之变成wxpython的GUI控件。当然，Gooey本身也带有命令行解析的函数---GooeyParser。下面就简单介绍Gooey的用法，以及优缺点。

### 安装Gooey
最简单的安装方法：
```bash
pip install Gooey
```
或者：
```bash
git clone https://github.com/chriskiehl/Gooey.git
```
然后运行setup.py :
```bash
python setup.py install
```
相关依赖：
wxpython
安装：pip install wxpython (windows下需要去官网下载安装包)

### 使用Gooey转化argparse
最简单的例子，将argparse参数转化为GUI控件：
```bash
#! -*- coding:utf-8 -*-

from gooey import Gooey
import argparse

@Gooey()
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("test",help="this is a test" )
	args=parser.parse_args()
	print args

if __name__=="__main__":
	main()
```
运行截图：
![](/upload_image/20170215/1.png)

说明：可以看到Gooey作为装饰器使用，Gooey()可以设置参数。

参数：
```bash
@Gooey(advanced=Boolean,          # toggle whether to show advanced config or not 
       language=language_string,  # Translations configurable via json
       show_config=True,          # skip config screens all together
       program_name='name',       # Defaults to script name
       program_description,       # Defaults to ArgParse Description
       default_size=(610, 530),   # starting size of the GUI
       required_cols=1,           # number of columns in the "Required" section
       optional_cols=2,           # number of columbs in the "Optional" section
       dump_build_config=False,   # Dump the JSON Gooey uses to configure itself
       load_build_config=None,    # Loads a JSON Gooey-generated configuration
       monospace_display=False)   # Uses a mono-spaced font in the output screen
       image_dir                  # Path to the diretory in which Gooey should look for custom inmages
       language_dir               # Path to the diretory in which Gooey should look for custom languages
)
```
参数中最常用的有program_name（标题，默认为文件名），default_size(界面大小)，image_dir(ico图标地址，可以相对地址，windows下注意用反斜杠)
```bash
@Gooey(program_name=u'这是一个测试脚本',default_size=(500,500))
def main():
	parser = argparse.ArgumentParser(description=u"测试描述内容")
	parser.add_argument("test",help="this is a test" )
	args=parser.parse_args()
	print args

if __name__=="__main__":
	main()
```
运行截图：
![](/upload_image/20170215/2.png)

### 使用GooeyParse
简单例子：
```bash
from gooey import Gooey, GooeyParser

@Gooey(program_name="test",image_dir=".\image") ##注意斜杠
def main():
    parser=GooeyParser(description=u"测试")
    ##文本输入框
    parser.add_argument("test",help="this is a test")
    ##选择框
    parser.add_argument(
     "test2",
     metavar='Should I exlode?',   ##描述内容
     help="this is test2",         ##帮助内容
     choices=["Yes","No"],         ##选择框
     default="Yes"                 ##默认值
     )
    ##复选框
    parser.add_argument(
       '-f','--foo',
       metavar="some flag",
       action="store_true",        ##参数类型
       help="")
    ##文本选择按钮
    parser.add_argument('filename', metavar=u"文件选择",help="name of the file to process", widget='FileChooser') #文本选择按钮
    parser.add_argument('datetime', metavar=u"时间选择",help="date to process",widget='DateChooser',default="2017-02-15") #时间选择按钮
    args=parser.parse_args()
    print args

if __name__=="__main__":
     main()
```
运行截图：
![](/upload_image/20170215/3.png)
说明：image_dir设置为当前目录下image目录，则程序会去image目录下寻找相应的图片来覆盖默认的图片，因此覆盖的图片名字必须为默认的图片名;可以看到运行界面上分为Required Arguments与Optional Arguments参数，代码中'test'对应前者，'-test'对应后者；metavar表示描述信息；action表示控件类型；help为帮助信息；widget为小工具；default为默认内容。

image目录下图片文件名，分别用来覆盖界面上的图片：
* program_icon.ico  　　ico图标
* success_icon.png  　　运行成功的图标
* running_icon.png  　　正在运行时的图标
* loading_icon.gif  　　加载时的图标
* config_icon.png   　　配置图片
* error_icon.png    　　出错时的图片

action内容表示参数类型，分别对应着wxpython相应的控件：

* store 　　TextCtrl
* store_const 　　CheckBox
* store_true  　　CheckBox
* store_False 　　CheckBox
* append      　　TextCtrl
* count       　　DropDown
* Mutually Exclusive Group  　　RadioGroup
* chooice     　　DropDown

除了action之外，Gooey还提供了一些小工具（Widgets）
* DirChooser   　　目录选择按钮工具
* FileChooser  　　文件选择按钮工具
* DateChooser  　　时间选择按钮工具

### 优缺点
　　说说个人使用的一点总结，优点是方便，无需太多的代码，也免去了界面设计。缺点是不太适合操作非常复杂的程序，且目前支持的控件不多。额外一点，在打包程序时，会有很多Bug，有待解决。


参考文档：
GitHub地址:[https://github.com/chriskiehl/Gooey](https://github.com/chriskiehl/Gooey)
官方例子：[https://github.com/chriskiehl/GooeyExamples/tree/master/examples](https://github.com/chriskiehl/GooeyExamples/tree/master/examples)
官方文档：[https://github.com/chriskiehl/Gooey#how-does-it-work](https://github.com/chriskiehl/Gooey#how-does-it-work)








