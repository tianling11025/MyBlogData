#! -*- coding:utf-8 -*-
'''
找寻所有的html文件，注释Power,Theme
'''

import os
m=0
def search(paths):
	global m
	if os.path.isdir(paths):  #如果是目录
		files=os.listdir(paths)  #列出目录中所有的文件
		for i in files:
			i=os.path.join(paths,i)  #构造文件路径
			search(i)           #递归
	elif os.path.isfile(paths) and ".html" in paths: #如果是html文件
		f=open(paths,"r")
		file_content=f.readlines()
		n=0
		for i in file_content:
			n+=1
			if '<div class="powered-by">' in i:
				file_content[n-1]="<!--"
				file_content[n+8]="-->"
				m+=1
				print '[*Info]',m
				break
		file_content='\n'.join(file_content)
		f=open(paths,"w")
		f.write(file_content)
		f.close()

search("./public")


