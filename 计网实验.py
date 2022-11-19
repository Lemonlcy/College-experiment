from scapy.all import *
from random import randint
import time,ipaddress,threading
from optparse import OptionParser

def TraceRouteTTL(addr):
    print("Tracing route to [%s]" % addr)
    print("over a maximum of 30 hops",end="\n\n")
    print(" TTL\tFirst\tSecond\tThird\tIP\t")
    NumofFound=0                                                                    #记录找到的路由器个数
    NumofNotFound=0                                                                 #记录未找到的路由器个数
    for TTL in range(1,31):                                                         #ttl，每次接收到回复增加一
        if TTL<10:
            print("[ 0%s ]\t" % TTL,end="")
        else:
            print("[ %s ]\t" % TTL,end="")
        
        for i in range(1,4):                                                        #记录三次延迟时间
            Port=randint(33434,33534)                                               #生成16位随机编码作为端口号
            Tstart=time.perf_counter()                                              #记录开始时间
            Truler=Tstart                                                           #防止程序卡死
            UDP = IP(dst=addr, ttl=TTL, id=Port) / ICMP(id=Port, seq=Port)          #构造ICMP数据包(UDP)
            ErrorMessageRespon = sr1(UDP,timeout=3,verbose=0)                       #从差错报文里获取IP地址
            if ErrorMessageRespon != None:
                Tend=time.perf_counter()                                            #记录结束时间
                print('%s ms\t' % round((Tend - Tstart)*1000),end='')               #输出延时
            elif (time.perf_counter() - Truler)>500000:                             #超时跳出
                print('NULL\t',end='')
            else:
                print('NULL\t',end='')                                              #无法找到路由跳出


        if ErrorMessageRespon != None:
            ip_src = str(ErrorMessageRespon[IP].src)                                #收到的节点地址
            if ip_src != addr:                                                      #判断是否为终点节点
                print("{}\t".format(str(ErrorMessageRespon[IP].src)))               #返回中间节点ip地址
                NumofFound=NumofFound+1
            else:
                print("{}\t".format(str(ErrorMessageRespon[IP].src)),end='\n\n')    #返回终点节点ip地址
                NumofFound=NumofFound+1
                print("Trace complete")
                print("totally %s routers found and %d routers not found" % (NumofFound,NumofNotFound))
                return 1
        else:
            print("TimeOut\t")                                                      #无回应
            NumofNotFound=NumofNotFound+1
        time.sleep(1)                                                               #发送间隔

if __name__== "__main__":
    print("Designed by 自动化2班林崇越")
    print("本程序仿制Windows的tracert命令")
    print("个人能力有限，无法做到输入网址获取IPv4地址，请使用前手动获取",end='\n\n')
    parser = OptionParser()                                                         #创建一个选项接口
    parser.add_option("-a","--addr",dest="addr")                                    #给接口添加属性：IP地址
    (options,args) = parser.parse_args()                                            #把接口从parser给到args，可以通过args使用
    TraceRouteTTL(str(options.addr))                                                #核心指令
