---
title: CTF加密与解密
date: 2017-06-13 11:22:25
comments: true
tags:
- CTF
- 加密与解密
- 隐写术
categories: 技术研究
permalink: 01
---
<blockquote class="blockquote-center">科技的精灵已经从瓶中跑了出来，但我们还不知道真正降临的时刻</blockquote>
　　今日在翻看笔记的时候，无意看到了之前为参加CTF时做的准备工作，主要包括了各种加密解密，web安全，PWN溢出等内容的练习题以及解决脚本。由于内容部分来自本人参加ctf时所做的题以及部分来自互联网，因此准备在此分享记录一番。本篇主要介绍几种CTF中常见加密算法的解密脚本，关于加密原理会适当提及，但不会深入。
<!--more -->
### DES解密
原理不多说了，直接放脚本源码
```bash
# -*- coding:utf-8 -*-
#Des算法一般密钥长度为8位（可以是8的倍数），且加密与解密算法相同。（私有密钥，对称加密方式）
from pyDes import *
import threading
import Queue
import os
import sys
import time
from multiprocessing import Process,Pool,Manager
import multiprocessing

class maskdes:
    '''
    DES加密算法
    des(key,[mode],[IV],[pad],[padmode])
    @key:密钥(8位长度)
    @mode：模式，支持CBC与ECB
    @IV：
    @pad：
    @padmode：
    @data：明文
    @data_en：密文
    '''
    def __init__(self):
        pass

    def maskencrypt(self,data,key):
        '''
        明文加密
        @data:明文
        @key:密钥
        '''
        k = des(key,CBC,"\0\0\0\0\0\0\0\0",pad=None,padmode=PAD_PKCS5) #des对象
        data_en = k.encrypt(data)       #进行des加密，返回密文
        
        # print u"密文: %r" % data_en

        return data_en

    def maskdecrypt(self,data,key):
        '''
        密文解密
        @data:密文
        @key:密钥
        '''
        k = des(key,CBC,"\0\0\0\0\0\0\0\0",pad=None,padmode=PAD_PKCS5) #des对象
        data_de = k.decrypt(data)   #进行des解密，返回明文

        # print u"明文: %r" % data_de

        return data_de




def des_run(key,cur,data_en):
    '''
    破解des密码函数
    '''
    #print key
    
    data_de=cur.maskdecrypt(data_en,str(key))
    if data_de=="Hello World":
        print data_de
        return True
    else:
        return False
        
        
if __name__=="__main__":

    '''
    已知一个明文，以及密钥，求密文？
    '''
    key="10036934"
    data = "Hello World" #明文

    cur=maskdes()
    data_en=cur.maskencrypt(data,key)
    print u"密文: %r" % data_en
    with open("result.txt","w") as w:
        w.write(data_en)

    '''
    已知一个密文文件，已知长度为8位的密钥(纯数字)，求明文？
    解密时，直接将文本中的内容读取复制给一个变量，进行解密即可
    '''
    #-------------------------多进程---------------------------
    cur=maskdes()
    data_en=open("result.txt","r").read()  ##从文件中读取密文
    
    start=time.time()
    result=Queue.Queue()
    pool = Pool()

    def pool_th():
        for key in xrange(10000000,11111111): ##密钥范围
            try:
                result.put(pool.apply_async(des_run,args=(key,cur,data_en)))   #维持执行的进程总数为10，当一个进程执行完后添加新进程.
            except:
                break

    def result_th():
        while 1:
            a=result.get().get()
            if a:
                pool.terminate()
                break

    t1=threading.Thread(target=pool_th)
    t2=threading.Thread(target=result_th)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print "add Process end"
    pool.join()
    end=time.time()
    print 'time is ',end-start
```
### AES解密
Aes解密脚本源码：
```bash
# -*- encoding:utf-8 -*-
'''
AES算法，密钥（key）长度一般为16,24,32位，密文一般为128位，192位，256位。
'''
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(data, password):
    '''
    AES加密算法
    '''
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    iv = Random.new().read(bs)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    return data

def decrypt(data, password):
    '''
    DES解密算法
    '''
    bs = AES.block_size
    if len(data) <= bs:
        return data
    unpad = lambda s : s[0:-ord(s[-1])]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data  = unpad(cipher.decrypt(data[bs:]))
    return data 
    
if __name__ == '__main__':
    data = 'flagadadh121lsf9adad' #要加密的数据
    password = '123456789abcdefg' #16,24,32位长的密码
    encrypt_data = encrypt(data, password)  ##获取加密后的字符串
    print 'encrypt_data:', encrypt_data  #<str>
    
    decrypt_data = decrypt(encrypt_data, password)
    print 'decrypt_data:', decrypt_data  #<str>
```

### RSA解密
关于RSA相关内容，我之前有总结过，可移步：[RSA加密算法解析](http://thief.one/2016/09/06/RSA%E5%8A%A0%E5%AF%86%E7%AE%97%E6%B3%95%E8%A7%A3%E6%9E%90/)

### 栅栏加密
```bash
# -*- coding:utf-8 -*-
'''
***栅栏加密方法***
加密方法自行百度，解密方法如下：
例子：adaufdns p
先计算密文的长度，如长度为10(空格也算)，因为每行的字符串数量一样，因此这里要么是分为5行，要么就是2行。
假设是分为2行，则每5个为一行分开：
adauf（前5）
dns p（后5）
再将每行首字符合并：
答案：addnasu fp
多行的话也是一样
@By nmask   2016.12.6
'''
string="tn c0afsiwal kes,hwit1r  g,npt  ttessfu}ua u  hmqik e {m,  n huiouosarwCniibecesnren."
string=list(string)
print 'String len is :',len(string)    ##字符串总长度
result=[]
answer=""
i=17 ##因为长度为85，因此这里写17或者5
def split_list(st):
    '''
    将密文字符串分隔成多行，每行的数量一样。
    '''
    st1=st[0:i]
    result.append(st1)
    for j in range(len(st)/i-1):
        sts=st[i*(j+1):i*(j+2)]
        result.append(sts)
    return result

if __name__=="__main__":
    result=split_list(string)
    '''
    将每行的首字符相组合
    '''
    for m in range(i):
        sums=""
        for n in result:
            sums=sums+n[m]
        answer+=sums
    print answer
```

### 培根加密算法
培根算法对照表如下：
A aaaaa
B aaaab
C aaaba
D aaabb
E aabaa
F aabab
G aabba
H aabbb
I abaaa
J abaab
K ababa
L ababb
M abbaa
N abbab
O abbba
P abbbb
Q baaaa
R baaab
S baaba
T baabb
U babaa
V babab
W babba
X babbb
Y bbaaa
Z bbaab

解密源代码：
```bash
# -*- coding:utf-8 -*-
'''
@培根加密算法
'''
string="ABAAAABABBABAAAABABAAABAAAAAABAAAAAAAABAABBBAABBAB"
dicts={'aabbb': 'H', 'aabba': 'G', 'baaab': 'R', 'baaaa': 'Q', 'bbaab': 'Z', 'bbaaa': 'Y', 'abbab': 'N', 'abbaa': 'M', 'babaa': 'U', 'babab': 'V', 'abaaa': 'I', 'abaab': 'J', 'aabab': 'F', 'aabaa': 'E', 'aaaaa': 'A', 'aaaab': 'B', 'baabb': 'T', 'baaba': 'S', 'aaaba': 'C', 'aaabb': 'D', 'abbbb': 'P', 'abbba': 'O', 'ababa': 'K', 'ababb': 'L', 'babba': 'W', 'babbb': 'X'}
sums=len(string)
j=5   ##每5个为一组
for i in range(sums/j):
    result=string[j*i:j*(i+1)].lower()
    print dicts[result],
```

### 凯撒密码
得知是凯撒加密以后，可以用127次轮转爆破的方式解密
```bash
# -*- coding:utf-8 -*-
'''
@凯撒加密
'''
lstr='''U8Y]:8KdJHTXRI>XU#?!K_ecJH]kJG*bRH7YJH7YSH]*=93dVZ3^S8*$:8"&:9U]RH;g=8Y!U92'=j*$KH]ZSj&[S#!gU#*dK9\.'''

for p in range(127):  
    str1 = ''  
    for i in lstr:  
        temp = chr((ord(i)+p)%127)  
        if 32<ord(temp)<127 :  
            str1 = str1 + temp   
            feel = 1  
        else:  
            feel = 0  
            break  
    if feel == 1:
        print str1 
```

### 变异md5加密
33位md5解密代码：
```bash
# -*- coding:utf-8 -*-
'''
CMD5加密
@By nMask 2016.12.6
一般md5的密文为16或者32位长度的字符串。
本脚本为，从33位加密的密文中，遍历删除一位长度，然后用md5解密。
@解密网站：http://www.cmd5.com/b.aspx
'''
string="cca9cc444e64c8116a30la00559c042b4"
string=list(string)
for i in range(len(string)):
    '''
    遍历删除一位，然后将字符串放入cmd5网站，批量解密。
    '''
    result=string[:] ##复制一个列表，不会改变原列表。
    result.pop(i)
    
    print "".join(result)
```

### brainfuck
brainfuck语言是比较难编写的一门语言，只有8个字符标识，需要写解释器，解释出用该语言编写的内容
其标识符含义如下：
* *>*指针加一
* <指针减一
* +指针指向的字节的值加一
* -指针指向的字节的值减一
* .输出指针指向的单元内容（ASCⅡ码）
* ,输入内容到指针指向的单元（ASCⅡ码）
* [如果指针指向的单元值为零，向后跳转到对应的]指令的次一指令处
* ]如果指针指向的单元值不为零，向前跳转到对应的[指令的次一指令处

解释器代码如下：
```bash
# -*- coding:utf-8 -*-
import os
'''
brainfuck语言解释器
用法：将brainfuck内容存入文本中，保存为.bf格式，然后运行run函数
'''
def mainloop(program, bracket_map):  
    pc = 0  
    tape = Tape()  
    while pc < len(program):  
        code = program[pc]  
        if code == ">":  
            tape.advance()  
        elif code == "<":  
            tape.devance()  
        elif code == "+":  
            tape.inc()  
        elif code == "-":  
            tape.dec()  
        elif code == ".":  
            os.write(1, chr(tape.get()))  
        elif code == ",":   
            tape.set(ord(os.read(0, 1)[0]))  
        elif code == "[" and tape.get() == 0:   
            pc = bracket_map[pc]  
        elif code == "]" and tape.get() != 0:  
            pc = bracket_map[pc]  
        pc += 1

class Tape(object):  
    def __init__(self):  
        self.thetape = [0]  
        self.position = 0  
    def get(self):  
        return self.thetape[self.position]  
    def set(self, val):  
        self.thetape[self.position] = val  
    def inc(self):  
        self.thetape[self.position] += 1  
    def dec(self):  
        self.thetape[self.position] -= 1  
    def advance(self):  
        self.position += 1  
        if len(self.thetape) <= self.position:  
            self.thetape.append(0)  
    def devance(self):  
        self.position -= 1

def parse(program):  
    parsed = []  
    bracket_map = {}  
    leftstack = []  
    pc = 0  
    for char in program:  
        if char in ('[', ']', '<', '>', '+', '-', ',', '.'):  
            parsed.append(char)  
            if char == '[':  
                leftstack.append(pc)  
            elif char == ']':  
                left = leftstack.pop()  
                right = pc  
                bracket_map[left] = right  
                bracket_map[right] = left  
            pc += 1  

    return "".join(parsed), bracket_map

def run(fp):  
    program_contents = ""  
    while True:  
        read = os.read(fp, 4096)  
        if len(read) == 0:  
            break  
        program_contents += read  
    os.close(fp)  
    program, bm = parse(program_contents)  
    mainloop(program, bm)  
if __name__=="__main__":
    '''
    传入.bf文件
    '''
    run(os.open("./1.bf", os.O_RDONLY, 0777))
```

### CRC32
```bash
# -*- coding:utf-8 -*-
'''
@crc32算法
crc算法的结果可以转化为16进制。
'''
import binascii
import datetime

def all_date():
    #获取所有日期
    result=[]
    begin=datetime.date(1900,1,1) #从1900年1月1日开始
    end=datetime.date(3000,12,6) #到3000年12月6日结束

    delta=datetime.timedelta(days=1)
    d=begin

    while d<=end:
        date=d.strftime("%Y%m%d")
        d+=delta
        result.append(date)

    return result

def _crc32(content): 
  #crc32解密
  return '%x' % (binascii.crc32(content) & 0xffffffff) #取crc32的八位数据 %x返回16进制

if __name__=="__main__":
    result=all_date()
    for i in result:
        #遍历每一个日期，暴力破解出密文结果
        tag=_crc32(i)
        if tag=="4d1fae0b":  ##16进制密文
            print i
```

### 摩斯密码
* -　　表示往右
* .　　表示往左

对照图：
![](/upload_image/20170613/1.png)

### 猪圈密码
参考图：
![](/upload_image/20170613/2.png)

### 维吉尼亚密码
维吉尼亚密码是凯撒密码的升级版。
```bash
key='abc'
#密文内容如下
ciphertext='csirxeerjsqraeehruamjkxhboaoylgvtsshewqpkbbuarnqhucojvyhpkpeflphvqkfytuhrtdgvbnqgkvwlyprbodpzumsghnkurmjcengiyocfobnswgkrfaipwucmusrprjjruwreibqsdpgxhrqjcglgvdajkiemtebolpkrdvzygnzatavgonwwbqsstvegzaekjxaynebtwszesroflakxrhqodnvxjsesrlwwywiggkkadvrmbvwhztgfugvqrqhrcjfnoldinsntzwmgretfrvrudpcpljlpvzdrpwopneolqsrfrboyowzkefvhpnkrdfdoanopbpygraowqvtbroanopwzruhrewhmtgknchjlsftgkrzciligvdsfhijlnnwtciexiihcoegiedhrwhpvfmsprrsevesztgoezvcxaooazneicweqgrtvmqegkaqbqxvytfrfhpkghpdqgrkiieofkrtvmxobvioyoxfcenfhepgoelzdwpkwyphnvlpnvsngkahnepvdhrhaeacgaxhswgkiremrzrtbvinbqehvqglcrnqtdiuxhrfdocwiinlbvedkjepghnhjrxyppbrlznviaevyvnsxvctjroampwwvwdoylgvrrbziyovsshfdoguidpnqrudakdegkwhuhvypaqkieavlephezvqkrwiphidcplacsuoagejdhrfrtmuleewaoevjczoqwhppcpljduoswiidhelnvqpkdbzjotdmeourwolncrsuhdoqsmtveqxpltkgefzeafwlizutkhpzqanghwffdruxerwsluqysrzdcvvwntmzlnriuaeyoovrwvzpsgrmlsgwmnohhnoonttukixqpilrpabgdvpqrrqcsbjmnxljuuhqrjbrdfcmpghzrqgreykseerppvkrgtdipvwsvdtzdcsivxejkafrlwdjcnwoqngrdfwdszryjpaaghpbtmefwksffegphrucsirxeewdfrhxypcnxcfatecrdjrnosertnoeepgwenrbhrdvjmeprmpaevojgarjlxyztuhrlvkqayvwbqemiosgkaepczeohabfzigeajdymgvleelowajareeevawqeiaagpvrrxyprnqixinwcbqrsahseehreayscrdgkaehhwktoadmzvixhrpegurakzgrwdcgckavqpvrpsldetlvpavlezdrsebhijlrftfzgsnjlhzvdqkseprnbcgvoedzcqrhvniqhsepcxtuhxsfwxytntwoozaxhrpktszslwdohaniwgufuwqrzlznhprndquxsbiajrucfyeexnyqpkiadywefpvhigknzkniaezebahvrwiphegmpxunohmsumxstrqsltnxhrdjwzdpjlwnbuyekxtvqczleckllxlnridsugkafzrhvcaghljngvoplkiffeknhnstpzhsuewdsedfsttfhnoacpigwhsolpcehrzhtbgvaoeehnstvlrfdglqpmnfhwfpkswehrgunpgwsfjhcihwrydsdnxquxaxljuuhvwzrulsxikhsruroawqrcynqnsmqvdruooylgveotriybqxhrkkifheeorrwrtmxituhiphwsenefkermvwiaverrvlvdtnutdotswvqchuhlfcrviipltebolpcegiidhvvglzfinruxwyoxyplvcaclvscylipbqxyprbrflvfkoqrsbgkitsizqejwwxsvgaoylgvsenusepgzovfagbieetmnosepcxhnyaunwlvceqworiyoagkaftleeeaeptsmevojgdieowgpbooedivleezdwpkxlcnvqtztkxtyhyoxhwrwiphelbuxhrpwbqwlvjmnnesmtwmnohsedkrtnpkaabgvfvyaoqymtpfermlkcxeesezydvrwiphczugwucrjozxwycobpstbvmntrjwglwrmlhhclbgvpvohoevqfviajaswqoauwdspdxvcpvollzsyefwecavectcrdnoajiaqpehfwsyprpxrcmpxiqhjhvwctciflsnwotohqzsqecyprvqamqnmtlwkfrpidmeedpzmofesrnspuenwiajahiaxhrfwhrutzwlnutptnwaylysgkekznrviomqjtuhiifkvfzmjllwucoeuhnhnopvcaagtsmqxhruowqhazwlzdkppgvsurnhruwypbehavaqjfgzkdvhgvdfermepgqufkncbpsepsvgeximisuhnguumevszdlwmtxhnqajruaytlrdnzbjirpdqgrvlvcnrfkewivojkeuulrkztuhtcmgwwuhnsnsmxpoapidbcoefkafsrvrdeeseybymtuvkarhjwzrgdltkgfrvqcguhvjplseansvshrujcepecsevjheajisgxipyhwlaoadsxinpefwwhrdrufsrvtsmoysuukczwsipapkaxwtiacsnccumreeuhirpvxhrfdsfkmipcnwcsirxeevelclkrydchpamtefvvdtbrxdlnudslvkrvvwwhvrrwzrgkeocelefvktgkiyzufhwsqelhrgazvyiidtbdfcwijobwioadpznebespzxisgkeggueedapwizvcrdnipsedtvcpyhxtvigoayaffdxzznjltsbjiferczrwwyprfhlqqpxogkavbxwvehrgunpgwsffkcxlwksrbziyofmsuhooagqrviajadwwttudpvnvxfzmhfhamrteezdwpkgrfsrvawqeituhzipkijdaaghpzdebleqharxkseprovwtkrvqjwajgypsulrpkcxtbvjsrcimtoyhnetaelvfawfjmmpngkemidcblwdsqxgypsfdnobqleevqfcumjptuhbljaxueqowawsraitwhpkjisulnspdxraprdrdqpeteharvuiteiajhpzvstuhioeflylrrvhzcuihrgegnstvlrfeuepkwgeljfrpezysohhtvfxosokogrrzesbzntvvlenlnderqgeiajawqeitbuaanuoksagvhppcwoswabfhielcnwwtbjsugdcfvqflenryeciiviazehuryklcnwcsirxeevajrqedldghaaitxynoeqreitzmrvarcgwtnwwangxvlpnutjinsntzehuwlvxaefhsitituhdogwiilnqdvpzaxiehzrbuqffsrzhzncplfdozrhtwcedxeybncoaouhbeimtoyhnetaaoxhjicpsdpngvllbgvblwdszdvtshnuelvfxhrkwhghvksepkaciexeevcwihectcrpaygtmdqoagnqhjeoeledqpglhgebtwlvqazrudejcifdnoihrctkrdwcqvmntgagxwlvsagweczgzenoohudxkselkagmvianohrnbfvnahveeqoihnvlialwypdulmmggxeeqwzybwklnqlnravmlydpdzwireizhawqeibrfkarvmeduyweoiphtvuarbifvtnteoxjcvdrgswgkvzodyhslvfwhroaoihwtwavpiyovlaglpknvxypsgxptlgwtghwdnuxpehnwssmjedryafohieeonoinmvvyvqchbsprjcerqfmvaigkwtydqzygbfhlxvirrlcvgwlvburhndktsqhhpueryeoaylcptgevrvpvrwiraaewylvfinghnggkixlrqhnhpgvefkaqbpijfpbqtszgilvyebtsprjiajclzfwpnljhvqkksejkiemtssrvkbnusjptehecmffepdqgrwlvburhnznjiaewovnwijhhvwecwuisnsncphwjtoarfxwticnuzgxlrxdaagqfmgrsnqzsihrksejkiemtebolpsawiidtuhglzfinnoeqrwlvymrhtdbjikvqcoagulpeawhpywieadbwtxvvoisiincnxtbshsnvizyterdfkgwhrupfngidlrxshciuiosiswgklzdhrddhpkghfkaigwiidagwhpanmguwagggmjdaglsqiexibqswgkejfbwhceinmcrlowaymkpdbuszugqitkpgnbsioeehdewrpaldcozhswnrbtupbymtuwdsdxivyaagtsmtisgrbvruwlmjrftdjwxtuhcozhultcxoyomugeagowawstsabvltdgjlnpebtrwrcehveoiuqayoahfdruseqjeswiwafewzyveeoaylcpwpgenjwwapivesgkenpgwhvuaqnwxypqhheywhlenupggkiezrqhrdbjicnwpcohfvsengeowppygrdoihlvcekhcfbksnruyczsprtngkaebjmsvveacrwjtbyhstveituhdsngmjllywhlbeenohosrqswsizeeniwwegkaqnwfvwoajsewvleqxyvrvwksedxepvkwperidghhkzrroelagxhrgqquhwjqrbppcqusngrnsfrpmptuhmlbvirpkwdghvetnrwhpuqgkgxnhyhwjeoebtsmfycuhogvvfizutktewvlepukehhxxcohqdlbcpiphofrtyvdtfkeccomnnwagbqjzydvqgxwtelfljsihvpehvqglzqynqkafgkihferqoqpgergvzwfpmjdefkecekxhgkahuuireoshxpkwxibqwbqvlvtnguooceisnoeqrwsksetuyapqrwurpoxhwyprgrtsmoscxwqfgoiksezrcvbwvtyhegihvpdaqhvpvvlohjdvrkejyofrrcwyleguesfwskplykidavsrldxchwlfhhrxsplvsbrdnsnoxlctyhiyaelobosvvflksetuyapqriawafextkdsbwhlbvlelfwbcoeplgnpenpcttrupsaossdtruqfifviyoahuhqfnkgxretgenqwdstucgsoagaykgxogkazbewkprdxaozkplrzdwyhectcruenqvisedpvrumenoeuenbnctvvpvrysznebitsmnsbfwafgkidzcxwucbnisvqcggkidmenxttnwpsbxlrhumerwulcsbjigeblvbqhilgfdltkgewnbbcedrzxprqdtvixrvdhqudtkprroegmpahbvpcyhxyptnutdinmcrdphrqhjltelawqpahvfdhuhoelvrrfsmcvtfloopfyjpdbisemcpiajpvrtyvpnfwacbuxhrmqfllwtzmcrsplqjvnuechveetmnostvepuqljuolpcehroikithtuhsvvwiilbolttavleprqfgvxifmchtpzcrdgkaxhgkvtsgkevqpkoskaoewwufrvqgepgtrbfasqlrxdaylcpnkrdfwdogvlvtsfwellkpytukkvqkclrthrepghoepkifhwtzlqvawqeiaagpsyowyprfkesiuroelcvgwsxcojdtdcelaedlwqsetpaagtlsgypnohhuhezcaylcpaesfsvwbqfecwsgkeowtqohvagnfgldagloyzkhipxhchvfvnahvepdgvybqauerajlnqvhpkcrnbwdsysmkxenqwsqniwvwjsfvijltgkeezkelvqyzhgikseudtemtahbgegcoirdefdnontysguwhrvxypkvqgeptsutkdwflrutrrftlvuaeevpcgkihfefwizvkrgnqzhuhhlnhrvsdkqskpkwdghvkheyyeltkgefhrwqhrtpaylcpquxhrqyoyoiufpnvahqvrefvovrdgttdrqtltnckaryyfrzvctuhjfzafokzehuwlvlnvpawakrsvgaoagxypkvqgzzfirfwdsnqmdllfwommrpaphzpnfozytbwhpqtwenwoprisiptuhtcqcpcbqpwaxijehrniyocrddxasarvuprnoinmvsbrjkbrfmktntuuwmcplchngbqwdzrrwhlvcqiyhdwtkxfwenyeepggohupphwectcrgidxwxefwdsvunlogrpeybcrdehbifhwkzlrdvpajiaejqsfzmkstuhktvienqtqsrqswsenutdwxirgkafvgmtflbxsazqgergebtvimpngxawtavesxowajxfsoyghpzvsntxahuhulpeavhzcvwhrubozlpzlrbifhqvlhrudsngfleaylcpquynninovggrwlvqgepgqohwwgwxwklpnfkzneerqvfifwejehrbseitxtbvsoepsmpruhrltkgefvegghvnlkrvhpzwtferioquirxbexssqpkwudphhurjzugwommusmroaoihwrydartlajswruktcoeptntfaclujrbpwzvfijqaphawqeilrdrsfkiidifwecwpxhrewbxwszxatlnpinptuhyielsldhnsppvkrgfikfuhvjpls'
ascii='abcdefghijklmnopqrstuvwxyz'
keylen=len(key)
ctlen=len(ciphertext)
plaintext = ''
i = 0
while i < ctlen:
    j = i % keylen
    k = ascii.index(key[j])
    m = ascii.index(ciphertext[i])
    if m < k:
        m += 26
    plaintext += ascii[m-k]
    i += 1
with open('result.txt','w') as f:
    f.write(plaintext)
```
### jsfuck or jother
以下内容参考：http://www.secbox.cn/hacker/ctf/8078.html
密文例子：
```bash
[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]]((![]+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]+(!![]+[])[+[]]+(![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+[+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]])()
```
解密方法：alert(xxx)、console(xxx)、document.write(xxx)，xxx为密文内容。
在线解密：http://www.jsfuck.com/

### 后记
关于Base64/16进制／URL编码／js编码／HTML编码等转化以及各种混淆技术，这里不再介绍，有很多在线转化工具。
关于CTF更多内容，可参考个人项目：https://github.com/tengzhangchao/CTF-LEARN


*说明：以上脚本若有运行错误或者编写错误可留言告知；若有补充可留言说明；另外本篇有些代码来自早期互联网收集，已遗忘原地址，若有知者望告之，在此表示感谢！*


>转载请说明出处：[CTF加密与解密|nMask'Blog](http://thief.one/2017/06/13/1)
本文地址：http://thief.one/2017/06/13/1