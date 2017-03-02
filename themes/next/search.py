#! -*- coding:utf-8 -*-

import os



def search(paths):
	if os.path.isdir(paths):  #如果是目录
		files=os.listdir(paths)  #列出目录中所有的文件
		for i in files:
			i=os.path.join(paths,i)  #构造文件路径
			search(i)           #递归
	elif os.path.isfile(paths): #如果是文件
		# print paths
		file_content=open(paths,"r").read()
		if "Mist" in file_content:
			print paths

search("./")

