#! -*- coding:utf-8 -*-

import requests
import hashlib
import base64
from multiprocessing.dummy import Pool

class http_request:

  def __init__(self,port="8080"):
    self.url="http://localhost:"+port
  
  def getwebbody(self,domain):
    '''
    获取网页源代码
    '''
    base_domain=base64.b64encode(domain)
    md5_domain=hashlib.md5(base_domain).hexdigest()
    payload={domain:md5_domain}

    try:
      response=requests.post(self.url,data=payload,timeout=30).content
      return response
    except requests.exceptions.ConnectionError:
      print "requests connection error"
    except Exception,e:
      print e
    return

if __name__=="__main__":
  port="8080"
  cur=http_request(port)
  domain_list=["http://thief.one"]*10

  def test(domain):
    print "Result_url is ",cur.getwebbody(domain)

  pool = Pool(processes=10)
  for domain in domain_list:
    pool.apply_async(test, args=(domain,))   #维持执行的进程总数为10，当一个进程执行完后添加新进程.
  pool.close()
  pool.join()