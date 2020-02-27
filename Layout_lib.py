#!/usr/bin/env python
# coding: utf-8

# In[1]:


#2020/2/27 杨树澄
#整合layout相关的函数库


# In[2]:


from pylab import *
from SFQ_lib import *
import sys
import re


# In[3]:


def floor_to_decimal(num): #把bBox误差出来的小数都去掉
    index=30
    return int(round(num/index))*index


# In[4]:


def read_layout(filename): #io接口，用来读取SKILL输出的版图信息
    instance_info=[]#module名
    orient_info=[]#方向
    inst_name_info=[]#例化名
    with open(filename[0]) as f:
        for line in f.readlines():
            line=line.rstrip('\n')
            instance_info.append(line.rstrip('\n'))  
    with open(filename[1]) as f:
        for line in f.readlines():
            line=line.rstrip('\n')
            orient_info.append(line.rstrip('\n'))
    length=len(instance_info)
    bBox_info_pre=[]
    with open(filename[2]) as f:
        for line in f.readlines():
            line=line.rstrip('\n')
            bBox_info_pre.append(line.rstrip('\n')) 
    bBox_info=[[] for i in range(int(length))]
    for i in range(0,length):
        bBox_info_pre[i]=bBox_info_pre[i].replace("(","")
        bBox_info_pre[i]=bBox_info_pre[i].replace(")","")
        bBox_info[i]=bBox_info_pre[i].split(" ")
        for k in range(0,4):
            bBox_info[i][k]=floor_to_decimal(float(bBox_info[i][k]))
    xy_info=[[] for i in range(int(length))]
    xy_info_pre=[]
    with open(filename[3]) as f:
        for line in f.readlines():
            line=line.rstrip('\n')
            xy_info_pre.append(line.rstrip('\n')) 
    for i in range(0,length):
        xy_info_pre[i]=xy_info_pre[i].replace("(","")
        xy_info_pre[i]=xy_info_pre[i].replace(")","")
        xy_info[i]=xy_info_pre[i].split(" ")
        for k in range(0,2):
            xy_info[i][k]=floor_to_decimal(float(xy_info[i][k]))
    with open(filename[4]) as f:
        for line in f.readlines():
            line=line.rstrip('\n')
            inst_name_info.append(line.rstrip('\n'))              
    return [instance_info, orient_info, bBox_info,xy_info,inst_name_info]


# In[5]:


def layout_info_summary(filename):#数据顺序：model，方向，bBox，起始点,汇总到一个info变量里
    basic_info=read_layout(filename)
    len_layout_inst=len(basic_info[0])
    layout_info_out=[[] for i in range(int(len_layout_inst))]
    for i in range(0,len_layout_inst):
        layout_info_out[i]=layout_to_model(basic_info[0][i],basic_info[4][i])
        layout_info_out[i].orient=basic_info[1][i]
        layout_info_out[i].xy=basic_info[3][i]
        #layout_info_out[i].append(basic_info[3][i])
    return layout_info_out


# In[6]:


def connect_info_process(connection): #重新整理netlist reader输出的互联信息
    len_connect=len(connection)
    connection_info=[]
    for i in range(0,len_connect):
        connection_info.append(connection[i].split(","))
    return connection_info


# In[7]:


def port_rearrangement(SFQmodel):#重新整理SFQ model中的port顺序（按照SFQ lib 里给出的port sequence）
    model_dir=dir(SFQmodel)
    len_dir=len(model_dir)
    seq_port=port_sequence()
    len_seq=len(seq_port)
    wire_name=[]
    for i in range(0,len_seq):
        if "wire"+seq_port[i] in model_dir:
            wire_name.append("wire"+seq_port[i])
    return wire_name


# In[8]:


def layout_to_dict(layout_info):#把layout中的信息整理到dictionary中，以便于查找两个互联器件的信息
    len_layout_info=len(layout_info)
    dict_inst_to_wire={}
    for i in range(0,len_layout_info):
        inst_name=layout_info[i].instname
        wire_name=port_rearrangement(layout_info[i])
        #print(inst_name)
        #print(wire_name)
        len_wire_name=len(wire_name)
        info={}
        for j in range(0,len_wire_name):
            info_temp={wire_name[j]:layout_info[i].port_type[j],"area":layout_info[i].area,"orient":layout_info[i].orient,"origin":layout_info[i].xy}
            #print(info_temp)
            info.update(info_temp)
        dict_temp={layout_info[i].instname:info}
        #print(info)
        #print(dict_temp)
        dict_inst_to_wire.update(dict_temp)
    return dict_inst_to_wire


# In[9]:


def get_route_coord(connection_info,dict_inst_to_wire):#获取port到port的绝对坐标
    len_connection=len(connection_info)
    routing_coord=[]
    for i in range(0,len_connection):
        #print(connection_info[i][0])
        dict_of_first_inst=dict_inst_to_wire[connection_info[i][0]]
        dict_of_second_inst=dict_inst_to_wire[connection_info[i][2]]
        start_wire=connection_info[i][1]
        end_wire=connection_info[i][3]
        start_port=dict_of_first_inst[start_wire]
        end_port=dict_of_second_inst[end_wire]
        first_inst_area=dict_of_first_inst["area"]
        second_inst_area=dict_of_second_inst["area"]        
        start_relative_coord=port_location(start_port,first_inst_area)[0]
        start_index=port_location(start_port,first_inst_area)[1]
        end_relative_coord=port_location(end_port,second_inst_area)[0]
        end_index=port_location(end_port,second_inst_area)[1]
        first_inst_orient=dict_of_first_inst["orient"]
        second_inst_orient=dict_of_second_inst["orient"] 
        first_inst_origin=dict_of_first_inst["origin"]
        second_inst_origin=dict_of_second_inst["origin"]
        first_abs_coord=get_abs_coord(first_inst_orient,first_inst_origin,start_relative_coord,start_index)
        second_abs_coord=get_abs_coord(second_inst_orient,second_inst_origin,end_relative_coord,end_index)
        routing_coord.append([first_abs_coord,second_abs_coord])
    return routing_coord


# In[10]:


def to_dbCreate(model,instname,coord,orient):#dbCreate生成模块
    '''cellID=dbOpenCellViewByType("ysc_layout" "layouttest" "layout" "maskLayout" "w")
    dbCreateParamInstByMasterName(cellID
    "ysc03_lib" "jtl_crs22_2x2_bi1ai2bo3ao5" "layout" "inst1" list(120 120) "R0")
    jtl1j_a_1x1ai1ao3
    '''
    dbcreate= "dbCreateParamInstByMasterName(cellID \"ysc03_lib\" \"{0}\" \"layout\" \"{1}\" list({2} {3}) \"{4}\")".format(model,instname,coord[0],coord[1],orient)
    #print(dbcreate)
    return dbcreate


# In[11]:


def route_direction(first_location,second_location):#根据例化前后两个30单位单元的信息来确定path的方向
    #按照“十”来看，跟inst_index相同的顺序排1234
    x_delta=second_location[0]-first_location[0]
    y_delta=second_location[1]-first_location[1]
    if(x_delta==1 and y_delta==0):
        fir_to_sec=3
    elif(x_delta==-1 and y_delta==0):
        fir_to_sec=1
    elif(x_delta==0 and y_delta==1):
        fir_to_sec=4
    elif(x_delta==0 and y_delta==-1):
        fir_to_sec=2
    else:
        raise Error("Wrong routing strategy: undefined direction -1")
    return fir_to_sec


# In[12]:


def last_check_index(index):#替换掉目标port的位置信息
    if(index==1):
        last_index=3
    elif(index==2):
        last_index=4;
    elif(index==3):
        last_index=1;
    elif(index==4):
        last_index=2;
    return last_index


# In[13]:


def direction_to_inst(input_direction,output_direction):#根据前后path的方向来确定输出到dbcreate中的模型，方向，相对原点等信息
    if(input_direction==1):
        if(output_direction==1):
            model="jtl1j_a_1x1ai1ao3"
            orient="MY"
            origin=[-1,0]
        elif(output_direction==2):
            model="jtl1j_a_1x1ai1ao4"
            orient="R180"
            origin=[-1,1]
        elif(output_direction==4):
            model="jtl1j_a_1x1ai1ao4"
            orient="MY"
            origin=[-1,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==2):
        if(output_direction==1):
            model="jtl1j_a_1x1ai1ao4"
            orient="MYR90"
            origin=[1,1]
        elif(output_direction==2):
            model="jtl1j_a_1x1ai1ao3"
            orient="R270"
            origin=[0,1]
        elif(output_direction==3):
            model="jtl1j_a_1x1ai1ao4"
            orient="R270"
            origin=[0,1]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==3):
        if(output_direction==2):
            model="jtl1j_a_1x1ai1ao4"
            orient="MX"
            origin=[0,1]
        elif(output_direction==3):
            model="jtl1j_a_1x1ai1ao3"
            orient="R0"
            origin=[0,0]
        elif(output_direction==4):
            model="jtl1j_a_1x1ai1ao4"
            orient="R0"
            origin=[0,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==4):
        if(output_direction==1):
            model="jtl1j_a_1x1ai1ao4"
            orient="R90"
            origin=[-1,0]
        elif(output_direction==3):
            model="jtl1j_a_1x1ai1ao4"
            orient="MXR90"
            origin=[0,0]
        elif(output_direction==4):
            model="jtl1j_a_1x1ai1ao3"
            orient="R90"
            origin=[1,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    else:
        raise Error("Wrong routing strategy: undefined direction -3")
    return [model,orient,origin]


# In[14]:


def path_to_inst(path,coord_info,index):#根据path和两个版图之间的信息来建立il-dbcreate所需的字符串
    script=[]
    len_path=len(path)
    first_check=route_direction(path[0],path[1])
    check_list=[first_check]
    inst_to_first=direction_to_inst(coord_info[0][1],first_check)
    xy_1=[(path[0][0]+inst_to_first[2][0])*30,(path[0][1]+inst_to_first[2][1])*30]
    first_one=to_dbCreate(inst_to_first[0],"inst{0}".format(int((index-1)*100)),xy_1,inst_to_first[1])
    script.append(first_one)
    for i in range(1,len_path-1):
        #print(path[i])
        check_index=route_direction(path[i],path[i+1])
        #print(check_index)
        check_list.append(check_index)
        inst_to_line=direction_to_inst(check_list[i-1],check_index)
        #print(inst_to_line)
        xy_seq=[(path[i][0]+inst_to_line[2][0])*30,(path[i][1]+inst_to_line[2][1])*30]
        #print(xy_seq)
        create_inst=to_dbCreate(inst_to_line[0],"inst{0}".format(int((index-1)*100+i)),xy_seq,inst_to_line[1])
        script.append(create_inst)
    len_check=len(check_list)
    last_check=check_list[len_check-1]
    inst_to_last=direction_to_inst(last_check,last_check_index(coord_info[1][1]))
    xy_end=[(path[len_path-1][0]+inst_to_last[2][0])*30,(path[len_path-1][1]+inst_to_last[2][1])*30]
    last_one=to_dbCreate(inst_to_last[0],"inst{0}".format(int((index-1)*100+len_path-1)),xy_end,inst_to_last[1])   
    script.append(last_one)
    return script

# In[15]:


def origin_to_blockpoint(area,origin,orient):
    if(orient=="R0"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30+i),int(origin[1]/30+j)])
    elif(orient=="R90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30-j),int(origin[1]/30+i)])
    elif(orient=="R180"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30-i),int(origin[1]/30-j)])
    elif(orient=="R270"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30+j),int(origin[1]/30-i)])
    elif(orient=="MX"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30+i),int(origin[1]/30-j)])
    elif(orient=="MXR90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30+j),int(origin[1]/30+i)])
    elif(orient=="MY"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30-i),int(origin[1]/30+j)])
    elif(orient=="MYR90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/30-j),int(origin[1]/30-i)])
    return rel_block_point


# In[16]:


def get_abs_block_point(layout_origin,block_point):
    len_block_point=len(block_point)
    abs_point=[]
    for i in range(0,len_block_point):
        #print(block_point[i])
        abs_point_temp=[block_point[i][0]-layout_origin[0],block_point[i][1]-layout_origin[1]]
        abs_point.append(abs_point_temp)
    #print(abs_point)
    return abs_point


# In[ ]:




