#!/usr/bin/env python
# coding: utf-8

# In[11]:


#2020/2/27 杨树澄
#整合netlist相关的函数库


# In[12]:


import time
from SFQ_lib import *
import string
import sys


# In[13]:


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


# In[14]:


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


# In[15]:


def read_module_name(line):#读取module名
    line=line.lstrip()#去空格
    index_1=line.find(" ")#找空格
    temp_line_1=line[index_1:]#截取module字串
    temp_line_2=remove_space(temp_line_1)#去所有空格
    index_2=temp_line_2.find('(')#找到第一个左括号
    return temp_line_2[:index_2]#返回module名


# In[16]:


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


# In[17]:


def read_netlist(filename):#读取netlist中的module名，输入输出端口，例化信息
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
    for i in range(0,len_new):#逐句判断处理好的netlist为什么类型的语句，并作出相应的信息提取操作
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


# In[18]:


def read_wire_name(SFQclass):#用来读取当前的SFQ model中包含哪些种类的wire
    class_dir=dir(SFQclass)
    class_len=len(class_dir)
    class_vars=vars(SFQclass)
    wire_type=[]
    for i in range(0,class_len):
        if 'wire' in class_dir[i]:
            wire_type.append(class_dir[i])
    return wire_type


# In[19]:


def inmod_inst_to_wire(module):#输入一整个module，得到module中每个inst的名字对应wire对应net的dictionary
    len_inmod=len(module)
    dict_model={}
    for i in range(0,len_inmod):
        wire_name=read_wire_name(module[i])
        class_vars=vars(module[i])
        len_wire_name=len(wire_name)
        for j in range(0,len_wire_name):
            dict_model.update({wire_name[j]+"_"+class_vars[wire_name[j]]:module[i].instname})
    return dict_model


# In[20]:


def read_connection(model_info,dict_info):#遍历整个module，查看每个inst的net与哪些端口连接，（调用上面的函数），并汇总到一起
    module_num=len(model_info[0])
    port_seq=port_sequence()
    seq_num=len(port_seq)
    #print(port_seq)
    #print(model_info[0])
    connection=[]
    for i in range(0,module_num):
        #print(model_info[3][i])
        dict_info=inmod_inst_to_wire(model_info[3][i])
        #print(dict_info)
        len_inst=len(model_info[3][i])
        #print(len_inst)
        for j in range(0,len_inst):
            wire_name=read_wire_name(model_info[3][i][j])
            var_model=vars(model_info[3][i][j])
            inst_name=model_info[3][i][j].instname
            #print(inst_name)
            len_wire=len(wire_name)
            #print(wire_name)
            for m in range(0,len_wire):
                if(not port_direction(wire_name[m])):
                    net_name=var_model[wire_name[m]]
                    #print(net_name)
                    for n in range(0,seq_num):
                        if "wire"+port_seq[n]+"_"+net_name in dict_info and inst_name!=dict_info["wire"+port_seq[n]+"_"+net_name]:
                            #print(net_name+inst_name+dict_info["wire"+port_seq[n]+"_"+net_name])
                            connect_info=inst_name+","+wire_name[m]+","+dict_info["wire"+port_seq[n]+"_"+net_name]+",wire"+port_seq[n]
                            #I0,wireABO,I2,wireBI
                            connection.append(connect_info)
        return connection


# In[ ]:




