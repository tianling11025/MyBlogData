---
title: 区块链系列·python实现的区块链
copyright: true
permalink: 1
top: 0
date: 2018-05-25 15:55:41
tags:
- 区块链
categories: 区块链安全
password:
---
<blockquote class="blockquote-center">地是床 天是被 流星是眼泪
有时醒 有时醉 大雁飞一个来回</blockquote>
　　听说现在会点区块链技术的工资都高破天了，抱着对高工资的幻想，我决定也开始学一学区块链吧。那么我想接触区块链的第一步必须得是去交易平台注册个帐号，然后充点钱买0.00001个BTC了。（2333，~!~现在我穷得只剩下币了）
<!--more-->

　　老实说区块链技术还是有点难理解的，为此我搜了搜区块链的实现代码，想着结合代码看获许会简单一点，于是我发现有人用python实现了简单的区块链，于是再原作者基础上，我稍微修改了点内容，在此粘贴一下，以供学习。原项目地址：https://github.com/xilibi2003/blockchain

```bash
#! -*- coding:utf-8 -*-


import hashlib
import json
from time import time


class Blockchain(object):
    ''' 区块链 
    
    一个区块结构（每个区块的字典顺序必须一致）：

    block = {
        'index': 1, # 区块索引
        'timestamp': 1506057125.900785, # 时间戳
        'transactions': [ # 交易列表
            {
                'sender': "8527147fe1f5426f9dd545de4b27ee00",
                'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
                'amount': 5,
            }
        ],
        'proof': 324984774000, # 工作量证明
        'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    }

    '''

    def __init__(self):

        self.chain = [] # 区块列表
        self.current_transactions = [] # 交易列表
        self.nodes = set() # 节点列表(避免重复)

        self.new_block(previous_hash=1, proof=100) # 创造创世区块


    def register_node(self,address):
        ''' 注册节点 

        Add a new node to the list of nodes
        :param address: <str> 节点地址 '192.168.0.1:5000'
        :return: None

        '''

        self.nodes.add(address)

    def valid_chain(self,chain):
        ''' 验证区块链的有效性 

        :param chain: <list> 一个完整的区块链
        :return: <bool> True if valid, False if not

        '''

        previous_block = chain[0] # 前一个区块
        current_index = 1 # 当前区块索引

        while current_index < len(chain):
            block = chain[current_index] # 当前区块

            if block['previous_hash'] != self.hash(previous_block):
                ''' hash值验证 '''
                return False

            if not self.valid_proof(previous_block['proof'],block['proof']):
                ''' 工作量证明验证 '''
                return False

            previous_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        ''' 共识算法解决不同节点账本不相同的冲突 

        使用网络中最长的有效区块链
        :return: <bool> True 如果链被取代, 否则为False
        '''

        neighbours = self.nodes # 网络中所有节点列表
        new_chain = None

        max_length = len(self.chain) # 当前节点的区块链长度

        for node in neighbours: # 遍历所有网络节点，若有比本节点有效区块链长的，则替换掉本地区块链
            
            # 通过api获取
            length = 100 # 某节点区块链长度
            chain = [] # 某节点区块链列表

            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False



    def new_block(self,proof,previous_hash=None):
        ''' 创建新的区块，添加到区块链中 
        
        生成新块
        :param proof: <int> 工作量证明
        :param previous_hash: 前一个区块的hash值
        :return: <dict> 新区块

        '''

        block = {

            'index': len(self.chain) + 1, # 确保索引在区块链尾部
            'timestamp': time(),
            'transactions': self.current_transactions, # 交易列表
            'proof': proof, # 工作量证明
            'previous_hash': previous_hash or self.hash(self.chain[-1]), # 此区块前一个区块的hash
        }

        # 对交易的详细内容可以进行操作，比如说增加金币，或者减少金币等等。

        self.current_transactions = [] # 重置交易列表

        self.chain.append(block) # 将新的区块添加到区块链中

        return block


    def new_transactions(self,sender,recipient,amount):
        ''' 添加新的交易到交易列表中 

        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: <str> 发送者地址
        :param recipient: <str> 接收着地址
        :param amount: <int> 金额或者数量
        :return: <int> 返回这笔交易的区块链索引（将这笔交易添加到区块链最后面）

        '''

        self.current_transactions.append({

            "sender":sender,
            'recipient':recipient,
            'amount':amount,

            })

        return self.last_block['index'] + 1
        
    @staticmethod
    def hash(block):
        ''' 计算一个区块的hash值 
        
        生成块的 SHA-256 hash值
        :param block: <dict> Block
        :return: <str>

        '''
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        ''' 区块链中最后一个区块 '''

        return self.chain[-1] # 返回区块链中最后一个区块


    def proof_of_work(self, last_proof):
        '''
        简单的工作量证明:
         - 查找一个 p' 使得 hash(pp') 以4个0开头
         - p 是上一个块的证明,  p' 是当前的证明
        :param last_proof: <int>
        :return: <int>
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof,proof):
        '''
        验证证明: 是否hash(last_proof, proof)以4个0开头?
        :param last_proof: <int> 前一个区块的hash
        :param proof: <int> 当前区块的hash
        :return: <bool> True or False
        '''

        guess = (str(last_proof)+str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"




if __name__=="__main__":

    # 运行这一段脚本就是一个区块链节点，而节点之间可以通过api的方式互相传递信息

    # 每个节点都每隔10分钟运行一次

    blockchain = Blockchain()

    for i in range(2):

        # 同步一下区块

        # 开始挖矿
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof) 

        # 挖矿成功后，生成新的交易（奖励交易）
        blockchain.new_transactions(sender="0",recipient="000002",amount=1)

        # 添加新的交易(不是奖励交易，而是普通交易)
        blockchain.new_transactions(sender="0000001",recipient="000002",amount=1)

        # 输出当前交易列表
        print "current_transactions lists is: \n",blockchain.current_transactions

        # 挖矿成功后，生成新的区块（包含奖励交易信息、新增的交易信息），只有挖矿成功后，才能创造出新的区块。
        block = blockchain.new_block(proof)

        # 输出当前区块链
        print "current chain lists is: \n",blockchain.chain
```

`从本篇开始，我将继续学习一些区块链的技术以及区块链安全相关的技术，并会总结成系列文章在博客发布，技术有限请多包涵！`


