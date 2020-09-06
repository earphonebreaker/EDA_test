#!/usr/bin/env python
import time
from SFQ_lib import *
import string
import sys
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
    #elif("reg " in line): #no reg statement in netlist
    #    line_type="reg"
    else:
        line_type="instanlization"
    return line_type



def remove_space(string): 
    return string.replace(' ','')

def read_info(line):
    line=line.lstrip()
    index_1=line.find(" ")
    module_name=line[0:index_1]
    temp_line_1=line[index_1:]
    temp_line_2=remove_space(temp_line_1)
    index_2=temp_line_2.find('(')
    instance_name=temp_line_2[0:index_2]
    temp_line_loop=temp_line_2[index_2+1:]
    port_num=temp_line_2.count('.')
    #print(port_num)
    port=[]
    wire=[]
    #print(temp_line_loop)
    for i in range(0,port_num):
        #print(temp_line_loop)
        index_3=temp_line_loop.find('.')
        index_4=temp_line_loop.find('(')
        index_5=temp_line_loop.find(')')
        port.append(temp_line_loop[index_3+1:index_4])
        wire.append(temp_line_loop[index_4+1:index_5])
        temp_line_loop=temp_line_loop[index_5+2:]
        #print(temp_line_loop)
    #print(temp_line_loop)
    #print(port)
    #print(wire)
    return [module_name,instance_name,port,wire]


# In[15]:


def read_module_name(line):
    line=line.lstrip()
    index_1=line.find(" ")
    temp_line_1=line[index_1:]
    temp_line_2=remove_space(temp_line_1)
    index_2=temp_line_2.find('(')
    return temp_line_2[:index_2]
def read_port(line):
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
    port_num=temp_line_loop.count(',')+1
    port=[bit]
    for i in range(0,port_num):
        index_2=temp_line_loop.find(",")
        port.append(temp_line_loop[:index_2])
        temp_line_loop=temp_line_loop[index_2+1:]
    return port
def read_netlist(filename):
    netlist=[]

    with open(filename) as f:
          for line in f.readlines():
                if(line=="\n"):
                    continue
                else:
                    line=line.rstrip('\n')
                    netlist.append(line.rstrip('\n'))
    len_netlist=len(netlist)
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
    for i in range(0,len_netlist):
        netlist[i]=netlist[i].replace('\n','')
    new="".join(netlist).split(';')
    len_new=len(new)
    for i in range(0,len_new):
        if(arbiter(new[i])!="endmodule" and arbiter(new[i])!="endspecify" ):
            new[i]=new[i]+";"
            
    module_top_info=[]
    k=0
    flag=0 
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

def read_wire_name(SFQclass):
    class_dir=dir(SFQclass)
    class_len=len(class_dir)
    class_vars=vars(SFQclass)
    wire_type=[]
    for i in range(0,class_len):
        if 'wire' in class_dir[i]:
            wire_type.append(class_dir[i])
    return wire_type

def inmod_inst_to_wire(module):
    len_inmod=len(module)
    dict_model={}
    for i in range(0,len_inmod):
        wire_name=read_wire_name(module[i])
        class_vars=vars(module[i])
        len_wire_name=len(wire_name)
        for j in range(0,len_wire_name):
            dict_model.update({wire_name[j]+"_"+class_vars[wire_name[j]]:module[i].instname})
    return dict_model

def read_connection(model_info,dict_info):
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

