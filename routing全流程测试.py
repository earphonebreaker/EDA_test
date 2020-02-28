#!/usr/bin/env python
# coding: utf-8

# In[1]:


#2020/2/27 杨树澄
#整合测试文件


# In[2]:


import time
from SFQ_lib import *
from Astar_lib import *
from Layout_lib import *
from Netlist_lib import *


# In[3]:


#读网表信息
File_dir="whatever.v"#这里的网表路径，要从skill中获得
netlist_test=read_netlist(File_dir)
print(netlist_test)


# In[4]:


#网表第一个module转dictionary
dict_info=inmod_inst_to_wire(netlist_test[3][0])
print(dict_info)


# In[5]:


#查找互联
connection=read_connection(netlist_test,dict_info)
print(connection)


# In[6]:


#处理互联信息
connection_info=connect_info_process(connection)
print(connection_info)


# In[7]:


#读layout信息
file_list=["routing_name.txt","routing_orient.txt","routing_bbox.txt", "routing_xy.txt","routing_inst.txt"]
layout_info=layout_info_summary(file_list)
print(layout_info)


# In[8]:


#读layout信息写入list
list_layout_info=read_layout(file_list)
print(list_layout_info)


# In[9]:


#读layout信息写入dictionary
dict_layout=layout_to_dict(layout_info)
print(dict_layout)


# In[10]:


#获取connection信息对应的，两个inst的坐标和index
coord_info=get_route_coord(connection_info,dict_layout)
print(coord_info)


# In[11]:


#获取版图的最大上下值 来自list_layout_info

x_0=[x[0] for x in list_layout_info[2]]
x_2=[x[2] for x in list_layout_info[2]]
y_1=[y[1] for y in list_layout_info[2]]
y_3=[y[3] for y in list_layout_info[2]]
x_max=max([max(x_0),max(x_2)])
y_max=max([max(y_1),max(y_3)])
x_min=min([min(x_0),min(x_2)])
y_min=min([min(y_1),min(y_3)])
print(x_max,x_min)
print(y_max,y_min)


# In[12]:


#设置寻路的地图大小
width=int((x_max-x_min)/30+4)
height=int((y_max-y_min)/30+4)
origin=[x_min,y_min]
print(width,height)
print(origin)
map_origin=[int(x_min/30-2),int(y_min/30-2)]#获得一个原点为00的，map相对于layout的坐标（这里2和上面的4以后要调整）
print(map_origin)


# In[15]:


#创立map
layout_map=Map(width,height)
#layout_map.showMap()
len_layout=len(layout_info)
for i in range(0,len_layout):
    #print(layout_info[i].area)
    block_point=origin_to_blockpoint(layout_info[i].area,layout_info[i].xy,layout_info[i].orient)
    #print(block_point)
    abs_point=get_abs_block_point(map_origin,block_point)
    #print(abs_point)
    layout_map.setBlock(abs_point)
    #layout_map.showMap()
#layout_map.showMap()
#开始寻路
#print(coord_info)#提示一下要连线的路径
coord_len=len(coord_info)
text=open("./creatinst.il",'w+')
cellid='''cellID=dbOpenCellViewByType("ysc_layout" "auto_route" "layout" "maskLayout")'''#这里以后改，dbopen函数
print(cellid,file=text)
for i in range(0,coord_len):#????coord怎么和layout def里面的不一样
    #print(coord_info[i])
    port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
    #print(port_1_temp)
    port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
    #print(port_1)
    port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
    #print(port_2_temp)
    port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
    #print(port_2)
    source=(port_2[0],port_2[1])#获取出发点
    dest=(port_1[0],port_1[1])#获取终点
    path=AStarSearch(layout_map,source,dest)#A星算path
    print(path)
    layout_map.showMap()
    layout_map.setBlock(path)#把这条path添加到库中
    temp=[coord_info[i][1],coord_info[i][0]]#只能用temp来重新排一下coord_info了
    #print(temp)
    new_path=[]
    len_path=len(path)
    for k in range(0,len_path):
        new_path.append([path[k][0]+map_origin[0],path[k][1]+map_origin[1]])#把还原的path坐标写入new path中
    print(new_path)
    script=path_to_inst(new_path,temp,i+1)#输入path 获取dbcreate脚本
    len_script=len(script)
    for j in range(0,len_script):
        print(script[j],file=text)#将dbcreate脚本字符串写进text中输出
text.close()


# In[ ]:





# In[ ]:




