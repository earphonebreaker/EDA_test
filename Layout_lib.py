#!/usr/bin/env python
# coding: utf-8

# In[2]:


#2020/2/27 杨树澄
#整合layout相关的函数库


# In[3]:


from pylab import *
from SFQ_lib import *
from Param_lib import *
import sys
import re


# In[4]:


def floor_to_decimal(num): #把bBox误差出来的小数都去掉
    index=layout_unit_len
    return int(round(num/index))*index #返回一个整数型的值


# In[5]:


def read_layout(filename): #io接口，用来读取SKILL输出的版图信息
    instance_info=[]#module名
    orient_info=[]#方向
    inst_name_info=[]#例化名
    with open(filename[0]) as f:#记录instance的model类型，例jtl1j_a_1x1_ai1ao3
        for line in f.readlines():
            line=line.rstrip('\n')
            instance_info.append(line.rstrip('\n'))  
    with open(filename[1]) as f:#记录版图的方向类型，例R0，R90，R180
        for line in f.readlines():
            line=line.rstrip('\n')
            orient_info.append(line.rstrip('\n'))
    length=len(instance_info)
    bBox_info_pre=[]
    with open(filename[2]) as f:#记录版图的bBox信息，其实后面基本没用到，还是原点+面积来算比较靠谱
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
    with open(filename[3]) as f:#记录版图的原点，和方向，model类型（面积）结合后面有函数可以得出版图的位置范围
        for line in f.readlines():
            line=line.rstrip('\n')
            xy_info_pre.append(line.rstrip('\n')) 
    for i in range(0,length):
        xy_info_pre[i]=xy_info_pre[i].replace("(","")
        xy_info_pre[i]=xy_info_pre[i].replace(")","")
        xy_info[i]=xy_info_pre[i].split(" ")
        for k in range(0,2):
            xy_info[i][k]=floor_to_decimal(float(xy_info[i][k]))
    with open(filename[4]) as f:#获取版图的instname，用于查找互联关系
        for line in f.readlines():
            line=line.rstrip('\n')
            inst_name_info.append(line.rstrip('\n'))              
    return [instance_info, orient_info, bBox_info,xy_info,inst_name_info]


# In[6]:


def layout_info_summary(filename):#数据顺序：model，方向，bBox，起始点,汇总到一个info变量里，每一个model的前述所有信息写入对应的class
    basic_info=read_layout(filename)
    len_layout_inst=len(basic_info[0])
    layout_info_out=[[] for i in range(int(len_layout_inst))]
    for i in range(0,len_layout_inst):
        layout_info_out[i]=layout_to_model(basic_info[0][i],basic_info[4][i])#layout_to_model:包含在本lib中（目前在SFQlib中）
        layout_info_out[i].orient=basic_info[1][i]#方向写入对应model
        layout_info_out[i].xy=basic_info[3][i]#原点写入对应model
        #layout_info_out[i].append(basic_info[3][i])
    return layout_info_out


# In[7]:


def connect_info_process(connection): #重新整理netlist reader输出的互联信息
    len_connect=len(connection)
    connection_info=[]
    for i in range(0,len_connect):
        connection_info.append(connection[i].split(","))#从netlist reader输出的字符串型信息拆分成 起始点inst，起始点net，终点inst，终点net
    return connection_info


# In[8]:


def port_rearrangement(SFQmodel):#重新整理SFQ model中的port顺序（按照SFQ lib 里给出的port sequence）
    model_dir=dir(SFQmodel)#获取当前model的所有数据名
    len_dir=len(model_dir)
    seq_port=port_sequence()#出自SFQlib，规定好的顺序
    len_seq=len(seq_port)
    wire_name=[]
    for i in range(0,len_seq):#根据端口命名顺序来重新排序
        if "wire"+seq_port[i] in model_dir:
            wire_name.append("wire"+seq_port[i])
    return wire_name


# In[9]:


def layout_to_dict(layout_info):#把layout中的信息整理到dictionary中，以便于查找两个互联器件的信息
    len_layout_info=len(layout_info)
    dict_inst_to_wire={}#建立一个空dict
    for i in range(0,len_layout_info):
        inst_name=layout_info[i].instname #从model中获取instname
        wire_name=port_rearrangement(layout_info[i]) #model的wire重新排布
        #print(inst_name)
        #print(wire_name)
        len_wire_name=len(wire_name)
        info={} #建立一个空dict
        for j in range(0,len_wire_name):#按顺序把当前model的wire对应的信息写入dict
            info_temp={wire_name[j]:layout_info[i].port_type[j],"area":layout_info[i].area,"orient":layout_info[i].orient,"origin":layout_info[i].xy}
            #print(info_temp)
            info.update(info_temp)
        dict_temp={layout_info[i].instname:info} #字典套娃
        #print(info)
        #print(dict_temp)
        dict_inst_to_wire.update(dict_temp) #再套
    return dict_inst_to_wire


# In[10]:


def get_route_coord(connection_info,dict_inst_to_wire):#获取port到port的绝对坐标
    len_connection=len(connection_info)
    routing_coord=[] #空list
    for i in range(0,len_connection):
        #print(connection_info[i][0])
        dict_of_first_inst=dict_inst_to_wire[connection_info[i][0]] #第一个单元的dict信息，包含这个model的方向端口面积等等
        dict_of_second_inst=dict_inst_to_wire[connection_info[i][2]]#第二个单元的dict信息
        start_wire=connection_info[i][1] #获取connection info 中的起始端口名
        end_wire=connection_info[i][3]#获取 终点端口名
        start_port=dict_of_first_inst[start_wire] #从dict中查找端口
        end_port=dict_of_second_inst[end_wire] 
        first_inst_area=dict_of_first_inst["area"] #从dict中查找面积
        second_inst_area=dict_of_second_inst["area"]        
        start_relative_coord=port_location(start_port,first_inst_area)[0] #port_location：一个根据port的序号和model的面积信息来得出port相对于origin的坐标
        start_index=port_location(start_port,first_inst_area)[1] #获取port位于方形的哪一个位面（十字方向，左1下2右3上4）
        end_relative_coord=port_location(end_port,second_inst_area)[0]
        end_index=port_location(end_port,second_inst_area)[1]
        first_inst_orient=dict_of_first_inst["orient"] #dict中获取orient信息 方向（R0，MX等）
        second_inst_orient=dict_of_second_inst["orient"] 
        first_inst_origin=dict_of_first_inst["origin"] #dict中获取origin信息 原点
        second_inst_origin=dict_of_second_inst["origin"]
        first_abs_coord=get_abs_coord(first_inst_orient,first_inst_origin,start_relative_coord,start_index)#get_abs_coord函数：根据上述信息获得端口的绝对坐标
        second_abs_coord=get_abs_coord(second_inst_orient,second_inst_origin,end_relative_coord,end_index)#以及同时传递端口的位面
        routing_coord.append([first_abs_coord,second_abs_coord])#得到输出口和输出口的绝对坐标、位面
    return routing_coord


# In[11]:


def to_dbCreate(model,instname,coord,orient):#dbCreate生成模块
    '''cellID=dbOpenCellViewByType("ysc_layout" "layouttest" "layout" "maskLayout" "w")
    dbCreateParamInstByMasterName(cellID
    "ysc03_lib" "jtl_crs22_2x2_bi1ai2bo3ao5" "layout" "inst1" list(120 120) "R0")
    jtl1j_a_1x1ai1ao3
    '''
    dbcreate= "dbCreateParamInstByMasterName(cellID \"{5}\" \"{0}\" \"layout\" \"{1}\" list({2} {3}) \"{4}\")".format(model,instname,coord[0],coord[1],orient,route_lib)
    #print(dbcreate)
    #这里例化的库，以后做成global parameter写入参数表
    return dbcreate


# In[12]:


def route_direction(first_location,second_location):#根据例化前后两个layout_unit_len单位单元的信息来确定path的方向
    #按照“十”来看，跟inst_index相同的顺序排1234
    x_delta=second_location[0]-first_location[0]#获取横坐标差来判断前后两个单元是什么方向的
    y_delta=second_location[1]-first_location[1]#获取纵坐标差来判断前后两个单元是什么方向的
    if(x_delta==1 and y_delta==0):
        fir_to_sec=3
    elif(x_delta==-1 and y_delta==0):
        fir_to_sec=1
    elif(x_delta==0 and y_delta==1):
        fir_to_sec=4
    elif(x_delta==0 and y_delta==-1):
        fir_to_sec=2
    else:
        raise Exception("Wrong routing strategy: undefined direction -1") #理论上只有1234四个方向，如果多出来说明程序有bug
    return fir_to_sec


# In[13]:


def last_check_index(index):#替换掉目标port的位置信息
    if(index==1):#这个函数是为了弥补之前程序设计不合理，把终点端口的位面换成和排线方向一致的值
        last_index=3 #（相对于上一个单元来说，如果终点端口位于1上一个line单元必须是3方向输出）
    elif(index==2):
        last_index=4;
    elif(index==3):
        last_index=1;
    elif(index==4):
        last_index=2;
    return last_index


# In[14]:


def direction_to_inst(input_direction,output_direction,layer):#根据前后path的方向来确定输出到dbcreate中的模型，方向，相对原点等信息
    if(input_direction==1):#注：这里jtl1j_a之类的，以后要换成ptl？
        if(output_direction==1):
            model=layer_straight_line[layer]
            orient="MY"
            origin=[-1,0]
        elif(output_direction==2):
            model=layer_corner_line[layer]
            orient="R180"
            origin=[-1,1]
        elif(output_direction==4):
            model=layer_corner_line[layer]
            orient="MY"
            origin=[1,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==2):
        if(output_direction==1):
            model=layer_corner_line[layer]
            orient="MYR90"
            origin=[1,1]
        elif(output_direction==2):
            model=layer_straight_line[layer]
            orient="R270"
            origin=[0,1]
        elif(output_direction==3):
            model=layer_corner_line[layer]
            orient="R270"
            origin=[0,1]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==3):
        if(output_direction==2):
            model=layer_corner_line[layer]
            orient="MX"
            origin=[0,1]
        elif(output_direction==3):
            model=layer_straight_line[layer]
            orient="R0"
            origin=[0,0]
        elif(output_direction==4):
            model=layer_corner_line[layer]
            orient="R0"
            origin=[0,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    elif(input_direction==4):
        if(output_direction==1):
            model=layer_corner_line[layer]
            orient="R90"
            origin=[1,0]
        elif(output_direction==3):
            model=layer_corner_line[layer]
            orient="MXR90"
            origin=[0,0]
        elif(output_direction==4):
            model=layer_straight_line[layer]
            orient="R90"
            origin=[1,0]
        else:
            raise Error("Wrong routing strategy: undefined direction -2")
    else:
        raise Error("Wrong routing strategy: undefined direction -3")
    return [model,orient,origin]


# In[15]:


def path_to_inst(path,coord_info,index,name,layer):#根据path和两个版图之间的信息来建立il-dbcreate所需的字符串
    script=[]
    len_path=len(path)
    first_check=route_direction(path[0],path[1])
    check_list=[first_check]
    inst_to_first=direction_to_inst(coord_info[0][1],first_check,layer)
    xy_1=[(path[0][0]+inst_to_first[2][0])*layout_unit_len,(path[0][1]+inst_to_first[2][1])*layout_unit_len]
    first_one=to_dbCreate(inst_to_first[0],"{0}_{1}".format(name,index),xy_1,inst_to_first[1])#以上，先获取第一个line模块的信息
    script.append(first_one)
    for i in range(1,len_path-1):
        #print(path[i])
        check_index=route_direction(path[i],path[i+1])
        #print(check_index)
        check_list.append(check_index)
        inst_to_line=direction_to_inst(check_list[i-1],check_index,layer)
        #print(inst_to_line)
        xy_seq=[(path[i][0]+inst_to_line[2][0])*layout_unit_len,(path[i][1]+inst_to_line[2][1])*layout_unit_len]
        #print(xy_seq)
        create_inst=to_dbCreate(inst_to_line[0],"{0}_{1}".format(name,index+i),xy_seq,inst_to_line[1])
        script.append(create_inst)#以上，获取中间模块的信息
    len_check=len(check_list)
    last_check=check_list[len_check-1]
    inst_to_last=direction_to_inst(last_check,last_check_index(coord_info[1][1]),layer)
    xy_end=[(path[len_path-1][0]+inst_to_last[2][0])*layout_unit_len,(path[len_path-1][1]+inst_to_last[2][1])*layout_unit_len]
    last_one=to_dbCreate(inst_to_last[0],"{0}_{1}".format(name,index+len_path-1),xy_end,inst_to_last[1])#以上，获取最后一个模块的信息
    script.append(last_one)
    return script


# In[16]:


def origin_to_blockpoint(area,origin,orient):#根据每个SFQmodel的面积，原点，方向，生成一系列在map上的block点（line不能穿过的地方）
    x=area[0]+2
    y=area[1]+2
    if(orient=="R0"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len-1+i),int(origin[1]/layout_unit_len-1+j)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int(origin[1]/layout_unit_len-1+y-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int(origin[1]/layout_unit_len-1+y-1)])

    elif(orient=="R90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j+1),int(origin[1]/layout_unit_len+i-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int(origin[1]/layout_unit_len-1+y-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int(origin[1]/layout_unit_len-1+y-1)])


    elif(orient=="R180"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i+1),int((origin[1]-layout_unit_len)/layout_unit_len-j+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])

    elif(orient=="R270"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+j-1),int((origin[1]-layout_unit_len)/layout_unit_len-i+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])


    elif(orient=="MX"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+i-1),int((origin[1]-layout_unit_len)/layout_unit_len-j+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])


    elif(orient=="MXR90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+j-1),int(origin[1]/layout_unit_len+i-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1),int(origin[1]/layout_unit_len-1+y-1)])
        rel_block_point.remove([int(origin[0]/layout_unit_len-1+x-1),int(origin[1]/layout_unit_len-1+y-1)])


    elif(orient=="MY"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i+1),int(origin[1]/layout_unit_len+j-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int(origin[1]/layout_unit_len-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int(origin[1]/layout_unit_len-1+y-1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int(origin[1]/layout_unit_len-1+y-1)])


    elif(orient=="MYR90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j+1),int((origin[1]-layout_unit_len)/layout_unit_len-i+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int((origin[1]-layout_unit_len)/layout_unit_len+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])
        rel_block_point.remove([int((origin[0]-layout_unit_len)/layout_unit_len+1-x+1),int((origin[1]-layout_unit_len)/layout_unit_len+1-y+1)])


    return rel_block_point


# In[15]:


def get_abs_block_point(layout_origin,block_point):#把block点的相对坐标转化到map中的绝对位置
    len_block_point=len(block_point)
    abs_point=[]
    for i in range(0,len_block_point):
        #print(block_point[i])
        abs_point_temp=[block_point[i][0]-layout_origin[0],block_point[i][1]-layout_origin[1]]
        abs_point.append(abs_point_temp)
    #print(abs_point)
    return abs_point


# In[ ]:




