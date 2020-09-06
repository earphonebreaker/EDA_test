#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Param_lib import *
from SFQ_lib import *
import sys
import re



def floor_to_decimal(num): #把bBox误差出来的小数都去掉
    index=layout_unit_len
    return int(round(num/index))*index #返回一个整数型的值



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


# In[10]:


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


# In[11]:


def connect_info_process(connection): #重新整理netlist reader输出的互联信息
    len_connect=len(connection)
    connection_info=[]
    for i in range(0,len_connect):
        connection_info.append(connection[i].split(","))#从netlist reader输出的字符串型信息拆分成 起始点inst，起始点net，终点inst，终点net
    return connection_info


# In[12]:


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


# In[13]:


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


# In[14]:
def get_abs_coord(orient,origin,relative_coord,index):#根据端口的相对坐标、版图原点和方向来确定端口在整个空间的绝对坐标
    # 方向种类："R0","R90","R180","R270","MX","MY","MXR90","MYR90"
    if(orient=="R0"):
        absolute_coord=[origin[0]+relative_coord[0],origin[1]+relative_coord[1]]
        abs_index=index
    elif(orient=="R90"):
        absolute_coord=[origin[0]-relative_coord[1],origin[1]+relative_coord[0]]
        if(index==4):
            abs_index=1
        else:
            abs_index=index+1
    elif(orient=="R180"):
        absolute_coord=[origin[0]-relative_coord[0],origin[1]-relative_coord[1]]
        if(index==1 or index==2):
            abs_index=index+2
        else:
            abs_index=index-2
    elif(orient=="R270"):
        absolute_coord=[origin[0]+relative_coord[1],origin[1]-relative_coord[0]]
        if(index==1):
            abs_index=4
        else:
            abs_index=index-1
    elif(orient=="MX"):
        absolute_coord=[origin[0]+relative_coord[0],origin[1]-relative_coord[1]]
        if(index==2):
            abs_index=4
        elif(index==4):
            abs_index=2
        else:
            abs_index=index
    elif(orient=="MY"):
        absolute_coord=[origin[0]-relative_coord[0],origin[1]+relative_coord[1]]
        if(index==1):
            abs_index=3
        elif(index==3):
            abs_index=1
        else:
            abs_index=index
    elif(orient=="MXR90"):
        absolute_coord=[origin[0]+relative_coord[1],origin[1]+relative_coord[0]]
        if(index==1):
            abs_index=2
        elif(index==2):
            abs_index=1
        elif(index==3):
            abs_index=4
        else:
            abs_index=3
    elif(orient=="MYR90"):
        absolute_coord=[origin[0]-relative_coord[1],origin[1]-relative_coord[0]]
        if(index==1):
            abs_index=4
        elif(index==2):
            abs_index=3
        elif(index==3):
            abs_index=2
        else:
            abs_index=1
    else:
        raise Error("Undefined orientation")
    return [absolute_coord,abs_index]

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


# In[15]:


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


# In[16]:


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


# In[17]:


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


# In[18]:


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


# In[19]:


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


# In[20]:



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

def origin_to_blockpoint_enlarged(area,origin,orient):#根据每个SFQmodel的面积，原点，方向，生成一系列在map上的block点（line不能穿过的地方）
    x=area[0]+2
    y=area[1]+2
    if(orient=="R0"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len-1+i),int(origin[1]/layout_unit_len-1+j)])

    elif(orient=="R90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j+1),int(origin[1]/layout_unit_len+i-1)])

    elif(orient=="R180"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i+1),int((origin[1]-layout_unit_len)/layout_unit_len-j+1)])

    elif(orient=="R270"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+j-1),int((origin[1]-layout_unit_len)/layout_unit_len-i+1)])


    elif(orient=="MX"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+i-1),int((origin[1]-layout_unit_len)/layout_unit_len-j+1)])


    elif(orient=="MXR90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int(origin[0]/layout_unit_len+j-1),int(origin[1]/layout_unit_len+i-1)])


    elif(orient=="MY"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i+1),int(origin[1]/layout_unit_len+j-1)])

    elif(orient=="MYR90"):
        rel_block_point=[]
        for i in range(0,x):
            for j in range(0,y):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j+1),int((origin[1]-layout_unit_len)/layout_unit_len-i+1)])

    return rel_block_point

def origin_to_blockpoint_prev(area,origin,orient):#原版的block函数
    if(orient=="R0"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/layout_unit_len+i),int(origin[1]/layout_unit_len+j)])
    elif(orient=="R90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j),int(origin[1]/layout_unit_len+i)])
    elif(orient=="R180"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i),int((origin[1]-layout_unit_len)/layout_unit_len-j)])
    elif(orient=="R270"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/layout_unit_len+j),int((origin[1]-layout_unit_len)/layout_unit_len-i)])
    elif(orient=="MX"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/layout_unit_len+i),int((origin[1]-layout_unit_len)/layout_unit_len-j)])
    elif(orient=="MXR90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int(origin[0]/layout_unit_len+j),int(origin[1]/layout_unit_len+i)])
    elif(orient=="MY"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-i),int(origin[1]/layout_unit_len+j)])
    elif(orient=="MYR90"):
        rel_block_point=[]
        for i in range(0,area[0]):
            for j in range(0,area[1]):
                rel_block_point.append([int((origin[0]-layout_unit_len)/layout_unit_len-j),int((origin[1]-layout_unit_len)/layout_unit_len-i)])
    return rel_block_point

# In[21]:


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


def get_index_sequence(path,first_index,last_index):
    len_path=len(path)
    sequence=[first_index]
    for i in range(0,len_path-1):
        index=route_direction(path[i],path[i+1])
        sequence.append(index)
    sequence.append(last_index)
    return sequence

def get_route_type(index_sequence):
    len_index=len(index_sequence)
    rtype=[]
    for i in range(0,len_index-1):
        if(not index_sequence[i]== index_sequence[i+1]):
            rtype.append("c")#corner
        else:
            rtype.append("p")#path
    return rtype

def process_path_coord(coord_source,coord_dest,in_index,out_index,drv_out,wire_width,end_extend_type):
    itface_width=(wire_width-drv_out)/2+enlarge_coef
    path_extend=layout_unit_len-itface_width
    cross_extend=(layout_unit_len-(wire_width+2))/2
    if(in_index==1):
        source=[coord_source[0]+path_extend,coord_source[1]]
    elif(in_index==2):
        source=[coord_source[0],coord_source[1]+path_extend]
    elif(in_index==3):
        source=[coord_source[0]-path_extend,coord_source[1]]
    elif(in_index==4):
        source=[coord_source[0],coord_source[1]-path_extend]
    if(end_extend_type=="itface"):
        if(out_index==1):
            dest=[coord_dest[0]-path_extend,coord_dest[1]]
        elif(out_index==2):
            dest=[coord_dest[0],coord_dest[1]-path_extend]
        elif(out_index==3):
            dest=[coord_dest[0]+path_extend,coord_dest[1]]
        elif(out_index==4):
            dest=[coord_dest[0],coord_dest[1]+path_extend]
    elif(end_extend_type=="cross"):
        if(out_index==1):
            dest=[coord_dest[0]-cross_extend,coord_dest[1]]
        elif(out_index==2):
            dest=[coord_dest[0],coord_dest[1]-cross_extend]
        elif(out_index==3):
            dest=[coord_dest[0]+cross_extend,coord_dest[1]]
        elif(out_index==4):
            dest=[coord_dest[0],coord_dest[1]+cross_extend]
    else:
        dest=coord_dest
    return [source,dest]

def pcell_coord(coord,in_index):
    if(in_index==1):
        origin=[coord[0]+layout_unit_len,coord[1]+layout_unit_len/2]
    elif(in_index==2):
        origin=[coord[0]+layout_unit_len/2,coord[1]+layout_unit_len]
    elif(in_index==3):
        origin=[coord[0],coord[1]+layout_unit_len/2]
    elif(in_index==4):
        origin=[coord[0]+layout_unit_len/2,coord[1]]    
    return origin
        
def index_to_layer(num):
    if(num==2 or num==1):
        return "mp1"
    else:
        return "mn0"

def get_descend(index,source,dest):
    if(index==1 or index==3):
        if(source[1]-dest[1]>0):
            descend=1
        else:
            descend=0
    elif(index==2 or index==4):
        if(source[0]-dest[0]>0):
            descend=1
        else:
            descend=0
    return descend

def analyze_path(path_coord,path_type,index_seq,rtype_seq,std_path_coord):
    info=[]
    #drv_itface
    group_A=[1,2]
    group_B=[3,4]
    if(path_type[1] in group_B):
        info.append([path_coord[0],index_seq[0],"mn0"])
    elif(path_type[1] in group_A):
        info.append([path_coord[0],index_seq[0],"mp1"])
    
    #path corner cross
    len_path=len(path_coord)
    k=1
    rtype_seq_temp=[]
    for r in rtype_seq:
        rtype_seq_temp.append(r)
    #print(rtype_seq)
    for i in range(1,len_path-1):
        if(i!=len_path-2 and i!=2):
            double_corner=rtype_seq_temp[i]=="p" and rtype_seq_temp[i+1]=="c" and rtype_seq_temp[i+2]=="c" and rtype_seq_temp[i-1]=="c" and rtype_seq_temp[i-2]=="c"

        if(double_corner):
            rtype_seq[i]="c"
            #print(i)        
        elif(rtype_seq_temp[i]=="c" and rtype_seq_temp[i-1]=="p" and rtype_seq_temp[i+1]=="p"):
            #print(i)
            rtype_seq[i-1]="c"
            rtype_seq[i+1]="c"
    #print(rtype_seq)
    for i in range(1,len_path-1):    
        if(i!=len_path-2 and i!=2):
            if(rtype_seq[i-1]=="p" and rtype_seq[i]=="c" and rtype_seq[i+1]=="c" and rtype_seq[i+2]=="p" and rtype_seq[i-2]=="p"):
                rtype_seq[i-1]="c"
            elif(rtype_seq[i-1]=="p" and rtype_seq[i]=="c" and rtype_seq[i+1]=="c" and rtype_seq[i+2]=="p" and rtype_seq[i-2]=="c"):
                rtype_seq[i+2]="c"
 
    #print(rtype_seq)
    #print(path_type)
    for i in range(1,len_path-1):
        curr_path_type=path_type[k]
        layer_unchange = (path_type[i+1] in group_A) == (path_type[i] in group_A)
        rtype_unchange = rtype_seq[i]==rtype_seq[i+1]
        info_temp=[curr_path_type,rtype_seq[k],k]
        if(i==len_path-2):#最后一个单元
            info_temp=[curr_path_type,rtype_seq[i],k]
            #print(info_temp)
            k=i 
            info_temp.append(k)
            info.append(info_temp)
            k=k+1
        elif(layer_unchange):
            if(rtype_unchange):
                pass
            else:
                #print("rtype_change at {}".format(i))
                k=i+1
                info_temp.append(k)
                info.append(info_temp)
        else:
            #print("layer_change at {}".format(i))
            k=i+1
            info_temp.append(k)
            info.append(info_temp)            
            
    #rec_itface
    if(path_type[-2] in group_B):
        info.append([path_coord[-1],last_check_index(index_seq[-1]),"mn0"])
    elif(path_type[-2] in group_A):
        info.append([path_coord[-1],last_check_index(index_seq[-1]),"mp1"])


    len_info=len(info)
    #print(info)

    for i in range(2,len_info-2):
        group_C=[1,3]
        group_D=[2,4]
        if(info[i][1]=="c"):
            #print(info[i])
            start=info[i][2]
            end=info[i][3]-1
            start_index=index_seq[start]
            end_index=index_seq[end+1]
            start_std_coord=std_path_coord[start]
            end_std_coord=std_path_coord[end]
            x_delta=abs(start_std_coord[0]-end_std_coord[0])
            y_delta=abs(start_std_coord[1]-end_std_coord[1])
            prev_path_length=abs(info[i-1][2]-info[i-1][3])
            next_path_length=abs(info[i+1][2]-info[i+1][3])
            if(x_delta>y_delta):     
                if(start_index in group_D and end_index in group_C):
                    info[i][3]=info[i][3]-1
                    info[i+1][2]=info[i+1][2]-1
                elif(start_index in group_C and end_index in group_D):
                    info[i][2]=info[i][2]+1
                    info[i-1][3]=info[i-1][3]+1
                elif(start_index in group_C and end_index in group_C):
                    if(info[i-1][0] in group_B):
                        info[i][3]=info[i][3]-1
                        info[i+1][2]=info[i+1][2]-1
                    elif(info[i+1][0] in group_B):
                        info[i][2]=info[i][2]+1
                        info[i-1][3]=info[i-1][3]+1
                    elif(prev_path_length>next_path_length):
                        info[i][2]=info[i][2]+1
                        info[i-1][3]=info[i-1][3]+1
                    else:
                        info[i][3]=info[i][3]-1
                        info[i+1][2]=info[i+1][2]-1
                elif(start_index in group_D and end_index in group_D):
                    if(info[i-1][0] in group_B):
                        info[i][3]=info[i][3]+1
                        info[i+1][2]=info[i+1][2]+1
                    elif(info[i+1][0] in group_B):
                        info[i][2]=info[i][2]-1
                        info[i-1][3]=info[i-1][3]-1
                    elif(prev_path_length>next_path_length):
                        info[i][2]=info[i][2]-1
                        info[i-1][3]=info[i-1][3]-1
                    else:
                        info[i][3]=info[i][3]+1
                        info[i+1][2]=info[i+1][2]+1
                
            elif(x_delta<y_delta):
                if(start_index in group_C and end_index in group_D):
                    info[i][3]=info[i][3]-1
                    info[i+1][2]=info[i+1][2]-1
                elif(start_index in group_D and end_index in group_C):
                    info[i][2]=info[i][2]+1
                    info[i-1][3]=info[i-1][3]+1
                elif(start_index in group_C and end_index in group_C):
                    if(info[i-1][0] in group_B):
                        info[i][3]=info[i][3]+1
                        info[i+1][2]=info[i+1][2]+1
                    elif(info[i+1][0] in group_B):
                        info[i][2]=info[i][2]-1
                        info[i-1][3]=info[i-1][3]-1
                    elif(prev_path_length>next_path_length):
                        info[i][2]=info[i][2]-1
                        info[i-1][3]=info[i-1][3]-1
                    else:
                        info[i][3]=info[i][3]+1
                        info[i+1][2]=info[i+1][2]+1
                elif(start_index in group_D and end_index in group_D):
                    if(info[i-1][0] in group_B):
                        info[i][3]=info[i][3]-1
                        info[i+1][2]=info[i+1][2]-1
                    elif(info[i+1][0] in group_B):
                        info[i][2]=info[i][2]+1
                        info[i-1][3]=info[i-1][3]+1
                    elif(prev_path_length>next_path_length):
                        info[i][2]=info[i][2]+1
                        info[i-1][3]=info[i-1][3]+1
                    else:
                        info[i][3]=info[i][3]-1
                        info[i+1][2]=info[i+1][2]-1
    #print(info)
    return info

def extend_port_path(source,dest,index):
    rsource=source
    if(index==1):
        rdest=[dest[0]-layout_unit_len,dest[1]]
    elif(index==2):
        rdest=[dest[0],dest[1]-layout_unit_len]
    elif(index==3):
        rdest=[dest[0]+layout_unit_len,dest[1]]
    elif(index==4):
        rdest=[dest[0],dest[1]+layout_unit_len]
    return [rsource,rdest]

def shorten_path(last_pts,last_index):
    if(last_index==1):
        pts=[last_pts[0]-layout_unit_len,last_pts[1]]
    elif(last_index==2):
        pts=[last_pts[0],last_pts[1]-layout_unit_len]
    elif(last_index==3):
        pts=[last_pts[0]+layout_unit_len,last_pts[1]]
    elif(last_index==4):
        pts=[last_pts[0],last_pts[1]+layout_unit_len]
    return pts          


def path_to_pcell(info,path_coord,index_seq):
    #print(info)
    group_A=[1,2]
    group_B=[3,4]
    len_info=len(info)
    #print(len_info)
    script=[]
    first_itface=interface(drv_out,wire_width,info[0][0],info[0][1],info[0][2])
    script.append(first_itface)
      
    
    for i in range(1,len_info-1):
        if(len_info==3):
            #print("yes")
            source_t=path_coord[info[1][2]]
            dest_t=path_coord[info[1][3]]
            [source,dest]=extend_port_path(source_t,dest_t,last_check_index(info[1][0]))
            path_i=path(source,dest,wire_width,index_to_layer(info[1][0]))
            script.append(path_i)             
        elif(info[i][1]=="p"):
            if((info[i+1][1]=="c" and info[i-1][1]=="c") and info[i][0] in group_B and info[i+1][0] in group_B and info[i-1][0] in group_A):
                #print("Yes",i)
                source=path_coord[info[i-1][3]]
                dest=path_coord[info[i+1][2]-1]
            elif((info[i+1][1]=="c" and info[i-1][1]=="c") and info[i][0] in group_B and info[i+1][0] in group_A and info[i-1][0] in group_A):
                #print(i)
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i+1][2]-1]
            elif((info[i+1][1]=="c" and info[i-1][1]=="c") and info[i][0] in group_B):
                #print(i)
                source=path_coord[info[i][2]]
                dest=path_coord[info[i+1][2]]

            elif((info[i+1][1]=="c" and info[i-1][1]=="c") and info[i][0] in group_A):#存在吗？mp1和mn0的链接必须有cross？（path）
                #print(i)
                source=path_coord[info[i-1][3]]
                dest=path_coord[info[i+1][2]]
                
            elif(i==1 and info[i][0] in group_B and info[i+1][0] in group_A):
                source=path_coord[info[i][2]]
                dest=path_coord[info[i+1][2]-1]

            elif(i==1 and info[i][0] in group_B and info[i+1][0] in group_B):
                source=path_coord[info[i][2]]
                dest=path_coord[info[i+1][2]]
                
            elif(i==len_info-2 and info[i][0] in group_B and info[i-1][0] in group_A):
                [source,dest]=extend_port_path(path_coord[info[i][2]+1],path_coord[info[i][3]],index_seq[-1])
                
            elif(i==len_info-2 and info[i][0] in group_A and info[i-1][0] in group_A):
                [source,dest]=[path_coord[info[i][2]],shorten_path(info[-1][0],info[-1][1])]
                
            elif(i==len_info-2 and info[i][0] in group_A and info[i-1][0] in group_B):
                [source,dest]=extend_port_path(path_coord[info[i][2]],path_coord[info[i][3]],index_seq[-1])
                
            elif(i==len_info-2 and info[i][0] in group_B and info[i-1][0] in group_B):
                #source=path_coord[info[i][2]]
                #dest=path_coord[info[i][3]]                
                [source,dest]=[path_coord[info[i][2]],shorten_path(info[-1][0],info[-1][1])]
                #[source,dest]=extend_port_path(path_coord[info[i][2]],path_coord[info[i][3]],index_seq[-1])
                
            elif(info[i-1][1]=="c" and info[i][0] in group_B and info[i+1][0] in group_A and info[i-1][0] in group_B):
                #print("yes")
                source=path_coord[info[i][2]]
                dest=path_coord[info[i][3]-1]

            elif(info[i-1][1]=="c" and info[i][0] in group_A and info[i+1][0] in group_B and info[i-1][0] in group_A):
                #print("yes")
                source=path_coord[info[i][2]]
                dest=path_coord[info[i][3]]
                
            elif(info[i+1][1]=="c" and info[i][0] in group_B and info[i-1][0] in group_A and info[i+1][0] in group_B):
                #print("yes")
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i][3]]

            elif(info[i-1][1]=="c" and info[i][0] in group_B and info[i-1][0] in group_A and info[i+1][0] in group_A):
                #print("yes")
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i][3]-1]
                
            elif(info[i-1][1]=="c" and info[i][0] in group_B and info[i+1][0] in group_A):
                #print("yes")
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i][3]+1]
                
            elif(info[i-1][1]=="c" and info[i][0] in group_A):
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i][3]+1]
                
            elif(info[i][0] in group_B and info[i+1][0] in group_A and info[i-1][0] in group_A):
                #print("yes")
                source=path_coord[info[i][2]+1]
                dest=path_coord[info[i+1][2]-1]
                
            elif(info[i][0] in group_A and info[i+1][0] in group_B ):
                source=path_coord[info[i][2]]
                dest=path_coord[info[i][3]]  
                
            elif(info[i][0] in group_A and (info[i+1][0] in group_B and info[i-1][0] in group_B)):
                source=path_coord[info[i][2]]
                dest=path_coord[info[i][3]+1]
              
            else:
                source=path_coord[info[i][2]]
                dest=path_coord[info[i][3]]

                

            if((info[i][0] in group_B ) and ((info[i+1][0] in group_A ) and (info[i-1][0] in group_A))):
                cross_i=cross(wire_width,path_coord[info[i][2]],index_seq[info[i][2]],last_check_index(index_seq[info[i][2]]))
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                cross_ip1=cross(wire_width,path_coord[info[i][3]-1],index_seq[info[i][3]],index_seq[info[i][3]])
                script.append(cross_i)
                script.append(path_i)
                script.append(cross_ip1)
            elif(i==1 and info[i][0] in group_B and info[i+1][0] in group_A):
                cross_i=cross(wire_width,path_coord[info[i+1][2]-1],index_seq[info[i][2]],index_seq[info[i][2]])
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                script.append(cross_i)
                script.append(path_i)
                
            elif(i==1 and info[i][0] in group_B and info[i+1][0] in group_B):
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                script.append(path_i)       
                
            elif((info[i][0] in group_B ) and (info[i-1][0] in group_A)):
                cross_i=cross(wire_width,path_coord[info[i][2]],index_seq[info[i][2]],last_check_index(index_seq[info[i][2]]))
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                script.append(cross_i)
                script.append(path_i)
            elif((info[i][0] in group_B ) and (info[i+1][0] in group_A)):
                cross_i=cross(wire_width,path_coord[info[i][3]-1],index_seq[info[i][3]],index_seq[info[i][3]])
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                script.append(cross_i)
                script.append(path_i)
            elif(info[i][0] in group_A):
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))
                script.append(path_i)
            else:
                #print(i)
                path_i=path(source,dest,wire_width,index_to_layer(info[i][0]))       
                script.append(path_i)

        elif(info[i][1]=="c"):
            #print(info[i])
            #print(info[i-1])
            #print(info[i+1])
            group_C=[1,3]
            group_D=[2,4]
            same_index= (index_seq[info[i][3]] in group_C) == (index_seq[info[i][2]] in group_C)
            #print(same_index)
            #print(index_seq[info[i][3]],index_seq[info[i][2]])


            #print(path_coord[info[i][2]][0])
            if(i==len_info-2):
                index_temp=info[i][3]
            else:
                index_temp=info[i][3]-1
            same_index= (index_seq[index_temp] in group_C) == (index_seq[info[i][2]] in group_C)

            if(index_seq[info[i][2]]==1):
                if(same_index):
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len)/layout_unit_len
                else:
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len/2)/layout_unit_len

            elif(index_seq[info[i][2]]==2):
                if(same_index):
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len)/layout_unit_len
                else:
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+3*layout_unit_len/2)/layout_unit_len
            elif(index_seq[info[i][2]]==3):
                if(same_index):
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len)/layout_unit_len
                else:
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len/2)/layout_unit_len
            elif(index_seq[info[i][2]]==4):
                if(same_index):
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+layout_unit_len)/layout_unit_len
                else:
                    corner_width=(abs(path_coord[index_temp][0]-path_coord[info[i][2]][0])+3*layout_unit_len/2)/layout_unit_len
            '''if(i==len_info-2):
                if(same_index):
                    corner_width=abs(path_coord[info[i][3]][0]-path_coord[info[i][2]][0]+layout_unit_len)/layout_unit_len
                else:
                    corner_width=(abs(path_coord[info[i][3]][0]-path_coord[info[i][2]][0])+3*layout_unit_len/2)/layout_unit_len
            else:
                if(same_index):
                    corner_width=abs(path_coord[info[i+1][2]][0]-path_coord[info[i][2]][0])/layout_unit_len
                else:
                    corner_width=(abs(path_coord[info[i+1][2]][0]-path_coord[info[i][2]][0])+layout_unit_len/2)/layout_unit_len'''

            #print(corner_width)
            wire_type=index_to_layer(info[i][0])
            origin=path_coord[info[i][2]]
            in_index=index_seq[info[i][2]]
            out_index=index_seq[info[i][3]+1]
            descend=get_descend(in_index,path_coord[info[i][2]],path_coord[info[i][3]])
            corner_i=corner(wire_width,corner_width,wire_type,origin,in_index,out_index,descend)
            script.append(corner_i)
                    
    last_itface=interface(rec_out,wire_width,info[-1][0],info[-1][1],info[-1][2])
    script.append(last_itface)
    return script

def regulate_route(coord,index,map_origin):
    if(index==1):
        regulate_p1=[coord[0],coord[1]+1]
        regulate_p2=[coord[0],coord[1]-1]
        regulate_p3=[coord[0]-1,coord[1]+1]
        regulate_p4=[coord[0]-1,coord[1]-1]
        regulate_p5=[coord[0],coord[1]+2]
        regulate_p6=[coord[0],coord[1]-2]
        regulate_p7=[coord[0],coord[1]+3]
        regulate_p8=[coord[0],coord[1]-3]
        regulate_p9=[coord[0]-1,coord[1]+2]
        regulate_p10=[coord[0]-1,coord[1]-2]
        regulate_p11=[coord[0]-1,coord[1]+3]
        regulate_p12=[coord[0]-1,coord[1]-3]

    elif(index==2):
        regulate_p1=[coord[0]+1,coord[1]]
        regulate_p2=[coord[0]-1,coord[1]]
        regulate_p3=[coord[0]+1,coord[1]-1]
        regulate_p4=[coord[0]-1,coord[1]-1]
        regulate_p5=[coord[0]+2,coord[1]]
        regulate_p6=[coord[0]-2,coord[1]]
        regulate_p7=[coord[0]+3,coord[1]]
        regulate_p8=[coord[0]-3,coord[1]]
        regulate_p9=[coord[0]+2,coord[1]-1]
        regulate_p10=[coord[0]-2,coord[1]-1]
        regulate_p11=[coord[0]+3,coord[1]-1]
        regulate_p12=[coord[0]-3,coord[1]-1]
    elif(index==3):
        regulate_p1=[coord[0],coord[1]+1]
        regulate_p2=[coord[0],coord[1]-1]
        regulate_p3=[coord[0]+1,coord[1]+1]
        regulate_p4=[coord[0]+1,coord[1]-1]
        regulate_p5=[coord[0],coord[1]+2]
        regulate_p6=[coord[0],coord[1]-2]
        regulate_p7=[coord[0],coord[1]+3]
        regulate_p8=[coord[0],coord[1]-3]
        regulate_p9=[coord[0]+1,coord[1]+2]
        regulate_p10=[coord[0]+1,coord[1]-2]
        regulate_p11=[coord[0]+1,coord[1]+3]
        regulate_p12=[coord[0]+1,coord[1]-3]

    elif(index==4):
        regulate_p1=[coord[0]+1,coord[1]]
        regulate_p2=[coord[0]-1,coord[1]]
        regulate_p3=[coord[0]+1,coord[1]+1]
        regulate_p4=[coord[0]-1,coord[1]+1]
        regulate_p5=[coord[0]+2,coord[1]]
        regulate_p6=[coord[0]-2,coord[1]]
        regulate_p7=[coord[0]+3,coord[1]]
        regulate_p8=[coord[0]-3,coord[1]]
        regulate_p9=[coord[0]+2,coord[1]+1]
        regulate_p10=[coord[0]-2,coord[1]+1]
        regulate_p11=[coord[0]+3,coord[1]+1]
        regulate_p12=[coord[0]-3,coord[1]+1]
    #print(regulate_p1)
    #print(regulate_p2)
    #print(regulate_p3)
    #print(regulate_p4)
    abs_list=[regulate_p1,regulate_p2,regulate_p3,regulate_p4,regulate_p5,regulate_p6,regulate_p7,regulate_p8,regulate_p9,regulate_p10,regulate_p11,regulate_p12]
    return abs_list

def regulate_route_new(coord,index,num):
    abs_list=[]
    if(index==1):
        for i in range(0,num):
            for j in range(1,4):
                regulate_p1=[coord[0]-i,coord[1]+j]
                regulate_p2=[coord[0]-i,coord[1]-j]
                abs_list.append(regulate_p1)
                abs_list.append(regulate_p2)
    elif(index==2):
        for i in range(0,num):
            for j in range(1,4):
                regulate_p1=[coord[0]+j,coord[1]-i]
                regulate_p2=[coord[0]-j,coord[1]-i]
                abs_list.append(regulate_p1)
                abs_list.append(regulate_p2)
    elif(index==3):
        for i in range(0,num):
            for j in range(1,4):
                regulate_p1=[coord[0]+i,coord[1]+j]
                regulate_p2=[coord[0]+i,coord[1]-j]
                abs_list.append(regulate_p1)
                abs_list.append(regulate_p2)

    elif(index==4):
        for i in range(0,num):
            for j in range(1,4):
                regulate_p1=[coord[0]+j,coord[1]+i]
                regulate_p2=[coord[0]-j,coord[1]+i]
                abs_list.append(regulate_p1)
                abs_list.append(regulate_p2)
    return abs_list