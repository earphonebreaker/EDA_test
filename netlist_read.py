#!/usr/bin/env python
# coding: utf-8

# In[8]:


#网表读取模块
#2020/2/6 杨树澄
import time
from SFQ_lib import *
import string


# In[9]:


print("还没想好怎么写 留着当抬头吧")


# In[35]:


#判断函数，用来查看当前行是什么类型的（module定义，input/output，还是例化语句？）
def arbiter(line):
    line_type=None
    if(("module " in line) and (not("endmodule" in line))):
        line_type="module"
    elif("endmodule" in line):
        line_type="endmodule"
    elif("endspecify" in line):
        line_type="endspecify"
    elif("specify " in line):
        line_type="specify"
    elif("specparam " in line):
        line_type="specparam"        
    elif("output " in line):
        line_type="output"
    elif("input " in line):
        line_type="input"
    elif("inout " in line):
        line_type="inout"
    elif(line[0]=="/" and line[1]=="/"):
        line_type="comment"
    elif(line[0]=="`" and line[-1]!=";"):
        line_type="macro definition"
    elif("wire " in line):
        line_type="wire"
    #elif("reg " in line): #网表存在reg变量吗？no
    #    line_type="reg"
    else:
        line_type="instanlization"
    return line_type
#废弃的函数，暂时没用
def finishing_detector(line):
    finished=None
    if(line[-1]==";"):
        finished=True
    else:
        finished=False
    return finished
def remove_space(string): #去除字符串中的空格
    return string.replace(' ','')

def read_info(line):#用于读取例化语句的信息，并返回例化信息
    line=line.lstrip()
    index_1=line.find(" ")#查找第一个空格确定module名
    module_name=line[0:index_1]#获取module名
    temp_line_1=line[index_1:]#删掉module名
    temp_line_2=remove_space(temp_line_1)#去掉多余的空格
    index_2=temp_line_2.find('(')#确定instance名的位置
    instance_name=temp_line_2[0:index_2]#获取instance名
    temp_line_loop=temp_line_2[index_2+1:]
    port_num=temp_line_2.count('.')#确定port个数
    #print(port_num)
    port=[]#端口集
    wire=[]#连线集
    #print(temp_line_loop)
    for i in range(0,port_num):
        #print(temp_line_loop)
        index_3=temp_line_loop.find('.')#查找端口标识
        index_4=temp_line_loop.find('(')#查找连线左边界
        index_5=temp_line_loop.find(')')#查找连线右边界
        port.append(temp_line_loop[index_3+1:index_4])#确定端口名
        wire.append(temp_line_loop[index_4+1:index_5])#确定连线名
        temp_line_loop=temp_line_loop[index_5+2:]#去掉已添加端口
        #print(temp_line_loop)
    #print(temp_line_loop)
    #print(port)
    #print(wire)
    return [module_name,instance_name,port,wire]
#line='s2j2o_b  I53 ( .AOA(net099), .AOB(net0104), .AI(net8));'
#print(read_info(line))
def read_module_name(line):#读取module名
    line=line.lstrip()#去空格
    index_1=line.find(" ")#找空格
    temp_line_1=line[index_1:]#截取module字串
    temp_line_2=remove_space(temp_line_1)#去所有空格
    index_2=temp_line_2.find('(')#找到第一个左括号
    return temp_line_2[:index_2]#返回module名
def read_port(line):#读取端口信息
    line=line.lstrip()
    if("[" in line):
        index_0=line.find(":")
        index_2=line.find("[")
        index_3=line.find("]")
        bit=abs(int(line[index_2+1:index_0])-int(line[index_0+1:index_3]))+1
        line=line[index_0+3:]
    else:
        bit=1
        index_1=line.find(" ")
        line=line[index_1:]
    temp_line_loop=remove_space(line)    
    #print(temp_line_1)
    port_num=temp_line_loop.count(',')+1#确定port个数
    port=[bit]
    for i in range(0,port_num):
        index_2=temp_line_loop.find(",")
        port.append(temp_line_loop[:index_2])
        temp_line_loop=temp_line_loop[index_2+1:]
    return port
#line='output [16:1] CO, SO,TO,BO,AO    ,DO;'
#
#read_port(line)


# In[36]:

def read_netlist(filename):
    netlist=[]
    #打开网表，把网表的内容储存在netlist变量里
    with open(filename) as f:
          for line in f.readlines():
                if(line=="\n"):
                    continue
                else:
                    line=line.rstrip('\n')
                    netlist.append(line.rstrip('\n'))
    len_netlist=len(netlist)
    #删除placement和routing optimization中不需要的timescale和文件抬头，顺带保护一下end类语句
    del_list=[]
    for i in range(0,len_netlist-1):
        if(arbiter(netlist[i])=="comment"):
            del_list.append(netlist[i])
        elif(arbiter(netlist[i])=="macro definition"):
            del_list.append(netlist[i])
        elif(arbiter(netlist[i])=="endspecify"):
            netlist[i]=netlist[i]+";"
        elif(arbiter(netlist[i])=="endmodule"):
            netlist[i]=netlist[i]+";"
    len_del=len(del_list)
    for i in range(0,len_del):
        netlist.remove(del_list[i])
    len_netlist=len(netlist)
    for i in range(0,len_netlist):#去除回车
        netlist[i]=netlist[i].replace('\n','')
    #将处理好的网表打成一条字符串（为了去掉换行），顺带再以分号为界分开。       
    new="".join(netlist).split(';')
    len_new=len(new)
    #上一步中分界的时候去掉了分号，现在再加上(除了end类)
    for i in range(0,len_new):
        if(arbiter(new[i])!="endmodule" and arbiter(new[i])!="endspecify" ):
            new[i]=new[i]+";"
            
    #以下获取信息模块
    module_top_info=[]
    k=0
    flag=0 #flag为1的时候开始查找例化语句
    len_new=len(new)
    for i in range(0,len_new):
        if(arbiter(new[i])=="module"):
            module_top_info.append(read_module_name(new[i]))
            k=k+1
    inst_info=[[] for i in range(k)]
    input_info=[[] for i in range(k)]
    output_info=[[] for i in range(k)]

    k=0
    for i in range(0,len_new):
        if(arbiter(new[i])=="module" and flag==0):
            flag=1
        elif(arbiter(new[i])=="endmodule" and flag==1):
            flag=0
            k=k+1
        elif(arbiter(new[i])=="instanlization" and flag==1):
            inst_info[k].append(read_instance(read_info(new[i])))
        elif(arbiter(new[i])=="input" and flag==1):
            input_info[k].append((read_port(new[i])))
        elif(arbiter(new[i])=="output" and flag==1):
            output_info[k].append((read_port(new[i])))
    return [module_top_info,input_info,output_info,inst_info]


# In[ ]:





# In[ ]:





# In[ ]:




