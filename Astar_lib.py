#!/usr/bin/env python
# coding: utf-8

# In[1]:


#2020/2/27 杨树澄
#优化好的A star算法库
import time
from SFQ_lib import *
from Layout_lib import *
from Netlist_lib import *
from Param_lib import *


# In[1]:


from random import randint
class SearchEntry():
    def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
        self.x = x
        self.y = y
        # cost move form start entry to this entry
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pre_entry = pre_entry

    def getPos(self):
        return (self.x, self.y)

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def setBlock(self,block_list): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            self.map[y][x] = 1;

    def setBlock_multi(self,block_list): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        x_first=block_list[0][0]
        y_first=block_list[0][1]
        self.map[y_first][x_first]=1
        x_last=block_list[block_list_len-1][0]
        y_last=block_list[block_list_len-1][1]
        self.map[y_last][x_last]=1
        for i in range(1,block_list_len-1):
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            x=block_list[i][0]
            y=block_list[i][1]
            if(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1):
                self.map[y][x]=1
            elif(self.map[y_prev][x_prev]==2):
                self.map[y][x]=1
            else:
                self.map[y][x]=2

    def setBlock_cross(self,block_list):
        flag=0
        block_list_len=len(block_list)
        x_first=block_list[0][0]
        y_first=block_list[0][1]
        self.map[y_first][x_first]=1
        x_last=block_list[block_list_len-1][0]
        y_last=block_list[block_list_len-1][1]
        self.map[y_last][x_last]=1
        for i in range(1,block_list_len-1):
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            x=block_list[i][0]
            y=block_list[i][1]
            if(self.map[y][x]==2):
                #print("rule 1 {0},{1}".format(x,y))
                self.map[y][x]=3
                if(abs(x_prev-x_next)==2):
                    self.map[y_prev][x_prev]=3
                    self.map[y_next][x_next]=3
                elif(abs(y_prev-y_next)==2):
                    self.map[y_prev][x_prev]=3
                    self.map[y_next][x_next]=3
            elif(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1 and self.map[y_prev][x_prev]==3):
                self.map[y][x]=4
            elif(self.map[y_prev][x_prev]==4):
                self.map[y][x]=3
                flag=1
            elif(abs(y_prev-y)==1 and self.map[y_prev][x_prev-1]==1 and self.map[y_prev][x_prev+1]==1 and self.map[y_prev][x_prev]==3):
                self.map[y][x]=3
                #print("rule 2 {0},{1}".format(x,y))
            elif(abs(x_prev-x)==1 and self.map[y_prev-1][x_prev]==1 and self.map[y_prev+1][x_prev]==1 and self.map[y_prev][x_prev]==3):
                self.map[y][x]=3
                #print("rule 3 {0},{1}".format(x,y))

            elif(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1):
                #print("rule 4 {0},{1}".format(x,y))
                self.map[y][x]=1
            elif(self.map[y_prev][x_prev]==2):
                #print("rule 5 {0},{1}".format(x,y))
                self.map[y][x]=1
            elif(flag==1):
                self.map[y][x]=3
                flag=0
            else:
                #print("rule 7 {0},{1}".format(x,y))
                self.map[y][x]=2
        for i in range(1,block_list_len-1):
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            x=block_list[i][0]
            y=block_list[i][1]
            if(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1 and (self.map[y][x]==3 or self.map[y][x]==4)):
                self.map[y_prev][x_prev]=3
    def read_path_type(self,path):
        len_path=len(path)
        line_info=[]
        for i in range(0,len_path):
            x=path[i][0]
            y=path[i][1]
            line_info.append(self.map[y][x])
            if(self.map[y][x]==3 or self.map[y][x]==4):
                self.map[y][x]=1
        return line_info
    
    
    def clrBlock(self,block_list): #清除block list
        block_list_len=len(block_list)
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            self.map[y][x] = 0;
    def get_blocked_point(self,block_list):
        block_list_len=len(block_list)
        prev_block=[]
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]

            print(x,y)
            if(self.map[y][x]==1):
                prev_block.append([x,y])
        return prev_block
        
    def showMap(self):
        print("+" * (3 * self.width + 2))
        len_row=len(self.map)
        #print(len_row)
        for i in range(len_row):
            s = '+'
            len_col=len(self.map[len_row-i-1])
            #print(self.map[len_row-i-1])
            for j in range(len_col):
                s +=' '+ str(self.map[len_row-i-1][j]) + ' '
            s +='+'
            print(s)

        print("+" * (3 * self.width + 2))


def AStarSearch(map, source, dest):
    def getNewPosition(map, locatioin, offset):
        x,y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1:
            return None
        return (x, y)

    def getPositions(map, location):#这里设置寻路类型，使用曼哈顿或折线距离
        # use four ways or eight ways to move 
        offsets = [(-1,0), (0, -1), (1, 0), (0, 1)]
        #offsets = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]
        poslist = []
        for offset in offsets:
            pos = getNewPosition(map, location, offset)
            if pos is not None:
                poslist.append(pos)
        return poslist

    # imporve the heuristic distance more precisely in future
    def calHeuristic(pos, dest):
        return abs(dest.x - pos[0]) + abs(dest.y - pos[1])
        
    def getMoveCost(location, pos):
        if location.x != pos[0] and location.y != pos[1]:
            return 1.4
        else:
            return 1

    # check if the position is in list
    def isInList(list, pos):
        if pos in list:
            return list[pos]
        return None
    
    # add available adjacent positions
    def addAdjacentPositions(map, location, dest, openlist, closedlist):
        poslist = getPositions(map, location)
        for pos in poslist:
            # if position is already in closedlist, do nothing
            if isInList(closedlist, pos) is None:
                findEntry = isInList(openlist, pos)
                h_cost = calHeuristic(pos, dest)
                g_cost = location.g_cost + getMoveCost(location, pos)
                if findEntry is None :
                    # if position is not in openlist, add it to openlist
                    openlist[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost+h_cost, location)
                elif findEntry.g_cost > g_cost:
                    # if position is in openlist and cost is larger than current one,
                    # then update cost and previous position
                    findEntry.g_cost = g_cost
                    findEntry.f_cost = g_cost + h_cost
                    findEntry.pre_entry = location

    # find a least cost position in openlist, return None if openlist is empty
    def getFastPosition(openlist):
        fast = None
        for entry in openlist.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast

    openlist = {}
    closedlist = {}
    location = SearchEntry(source[0], source[1], 0.0)
    dest = SearchEntry(dest[0], dest[1], 0.0)
    openlist[source] = location
    while True:
        location = getFastPosition(openlist)
        if location is None:
            # not found valid path
            print("can't find valid path")
            break;
        
        if location.x == dest.x and location.y == dest.y:
            break

        closedlist[location.getPos()] = location
        openlist.pop(location.getPos())
        addAdjacentPositions(map, location, dest, openlist, closedlist)

    #mark the found path at the map
    path_temp=[]
    while location is not None:
        #print(location.x,location.y)
        path_temp.append([location.x,location.y])
        location = location.pre_entry
    path=path_temp[::-1]
    return path


# In[3]:


def map_info(file_dir): #从routing信息和netlist信息来获取制作map的参数
    netlist_info=read_netlist(file_dir)#读netlist
    dict_info=inmod_inst_to_wire(netlist_info[3][0])#netlist信息写入dict
    connection=read_connection(netlist_info,dict_info)#获取connection信息
    connection_info=connect_info_process(connection)#整理connection信息
    file_list=["routing_name.txt","routing_orient.txt","routing_bbox.txt", "routing_xy.txt","routing_inst.txt"]
    layout_info=layout_info_summary(file_list)#读取layout信息
    list_layout_info=read_layout(file_list)#读取layout信息2
    dict_layout_info=layout_to_dict(layout_info)#整理layout信息写入dict
    coord_info=get_route_coord(connection_info,dict_layout_info)#获取routing的坐标信息
    x_0=[x[0] for x in list_layout_info[2]]#以下：获取layout中的最大xy坐标和最小xy坐标，用于确定map的长宽
    x_2=[x[2] for x in list_layout_info[2]]
    y_1=[y[1] for y in list_layout_info[2]]
    y_3=[y[3] for y in list_layout_info[2]]
    x_max=max([max(x_0),max(x_2)])
    y_max=max([max(y_1),max(y_3)])
    x_min=min([min(x_0),min(x_2)])
    y_min=min([min(y_1),min(y_3)])
    width=int((x_max-x_min)/layout_unit_len+map_enlarge)#设置map的宽度，并读取param_lib里的map_enlarge参数来扩充map
    height=int((y_max-y_min)/layout_unit_len+map_enlarge)#同上，设置高度
    origin=[x_min,y_min]#获取map的初始原点
    #print(width,height)
    #print(origin)
    map_origin=[int(x_min/layout_unit_len-map_offset),int(y_min/layout_unit_len-map_offset)]#获得一个原点为00的，map相对于layout的坐标（这里2和上面的4以后要调整）
    #print(map_origin)
    return [width,height,layout_info,map_origin,coord_info,connection_info]#返回所需信息
#map_info(File_dir)


# In[5]:


def mono_map_search(file_dir,lib,cell,display):
    info=map_info(file_dir)
    width=info[0]
    height=info[1]
    layout_map=Map(width,height)
    #layout_map.showMap()
    layout_info=info[2]
    len_layout=len(layout_info)
    map_origin=info[3]
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
    coord_info=info[4]
    connection_info=info[5]
    coord_len=len(coord_info)
    text=open("./createinst.il",'w+')
    cellid='''cellID=dbOpenCellViewByType("{0}" "{1}" "layout" "maskLayout")'''.format(lib,cell)#这里以后改，dbopen函数
    print(cellid,file=text)
    for i in range(0,coord_len):#封锁端口，先把所有端口都封上，在布每一条线的时候再单独打开（clrBlock函数）
        port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
        port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
        port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
        port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
        block_source=[port_2[0],port_2[1]]#获取出发点
        block_dest=[port_1[0],port_1[1]]#获取终点
        layout_map.setBlock([block_source,block_dest])
    #layout_map.showMap()
    for i in range(0,coord_len):#????coord怎么和layout def里面的不一样
        port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
        port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
        port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
        port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
        layout_map.clrBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])#先清除掉要布线的这条路径的端口block，不然就找不到valid path
        source=(port_2[0],port_2[1])#获取出发点
        dest=(port_1[0],port_1[1])#获取终点
        path=AStarSearch(layout_map,source,dest)#A星算path
        layout_map.setBlock(path)#把这条path添加到库中
        temp=[coord_info[i][1],coord_info[i][0]]#只能用temp来重新排一下coord_info了
        new_path=[]
        len_path=len(path)
        for k in range(0,len_path):
            new_path.append([path[k][0]+map_origin[0],path[k][1]+map_origin[1]])#把还原的path坐标写入new path中
        script=path_to_inst(new_path,temp,0,connection_info[i][0]+'_'+connection_info[i][2],0)#输入path 获取dbcreate脚本
        len_script=len(script)
        for j in range(0,len_script):
            print(script[j],file=text)#将dbcreate脚本字符串写进text中输出
        if(display==1):#显示函数，如果电路规模过大建议display置零
            print("source:{0} to destination:{1}".format(source,dest))
            print("path:{0}".format(new_path))
            layout_map.showMap()
        layout_map.setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
    text.close()
#display=1
#mono_map_search("whatever.v",'ysc_layout2','auto_route',display)


# In[1]:


def multi_map_search(file_dir,lib,cell,display,layer_num):
    info=map_info(file_dir)
    width=info[0]
    height=info[1]
    layout_info=info[2]
    map_origin=info[3]
    coord_info=info[4]
    connection_info=info[5]
    len_layout=len(layout_info)
    coord_len=len(coord_info)
    #创立多map
    map_list=[]
    for i in range(0,layer_num):#将封好的map写入多map列表
        layout_map=Map(width,height)
        for j in range(0,len_layout):#屏蔽inst所在区域
            block_point=origin_to_blockpoint(layout_info[j].area,layout_info[j].xy,layout_info[j].orient)
            abs_point=get_abs_block_point(map_origin,block_point)
            layout_map.setBlock(abs_point)
        for k in range(0,coord_len):#封锁端口
            port_1_temp=port_coord_to_map(coord_info[k][0][0],coord_info[k][0][1])#获取第一个端口坐标 map中的
            port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
            port_2_temp=port_coord_to_map(coord_info[k][1][0],coord_info[k][1][1])#同上
            port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
            block_source=[port_2[0],port_2[1]]#获取出发点
            block_dest=[port_1[0],port_1[1]]#获取终点
            layout_map.setBlock([block_source,block_dest])
        map_list.append(layout_map)
        #map_list[i].showMap()
    #打开createinst.il   
    text=open("./createinst.il",'w+')
    cellid='''cellID=dbOpenCellViewByType("{0}" "{1}" "layout" "maskLayout")'''.format(lib,cell)#这里以后改，dbopen函数
    print(cellid,file=text)
    
    for i in range(0,coord_len):#????coord怎么和layout def里面的不一样
        port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
        port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
        port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
        port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
        source=(port_2[0],port_2[1])#获取出发点
        dest=(port_1[0],port_1[1])#获取终点
        path=[]
        len_path=[]
        for j in range(0,layer_num):#对多个map循环查找最优路径
            map_list[j].clrBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])#先解开端口的block
            path_temp=AStarSearch(map_list[j],source,dest)#A星算path
            if(len(path_temp)==0):#判断一下，如果path找不到，长度应该为0，所以这里赋值正无穷
                len_path_temp=inf
            else:
                len_path_temp=len(path_temp)#记录这个map的path的长度
            path.append(path_temp)#加入到总path中
            len_path.append(len_path_temp)#加入到总len_path中
            map_list[j].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])#把端口封上
            
        min_path_index=len_path.index(min(len_path))#获取几层之中最短的那一层  
        min_path=path[min_path_index]#获取最短的路径
        print("----------------------------------------------------------------")
        #print(path[0])
        #print(min_path_index)
        #print(min_path)
        for j in range(0,layer_num):
            if(j==min_path_index):
                map_list[j].setBlock(min_path)
            else:
                map_list[j].setBlock_multi(min_path)
            print("the {0}th layer".format(j))
            map_list[j].showMap()
        
        temp=[coord_info[i][1],coord_info[i][0]]#只能用temp来重新排一下coord_info了            
        new_path=[]
        len_min_path=len(min_path)
        for k in range(0,len_min_path):
            new_path.append([min_path[k][0]+map_origin[0],min_path[k][1]+map_origin[1]])#把还原的min_path坐标写入new path中
        #print(new_path)
        script=path_to_inst(new_path,temp,0,connection_info[i][0]+'_'+connection_info[i][2],min_path_index)#输入path 获取dbcreate脚本
        len_script=len(script)
        for j in range(0,len_script):
            print(script[j],file=text)#将dbcreate脚本字符串写进text中输出
    text.close()    


# In[6]:


#测试模块
'''map_width=10
map_height=10
map2=Map(map_width,map_height)
map2.setBlock([[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3],[2,5],[2,6],[3,5],[3,6],[8,3],[9,3],[9,4],[8,4]])
source1=(4,2)
dest1=(7,3)
source2=(4,5)
dest2=(7,4)
path1=AStarSearch(map2,source1,dest1)
map2.showMap()
print(path1)
map2.setBlock(path1)
path2=AStarSearch(map2,source2,dest2)
map2.showMap()
print(path2)'''


# In[ ]:




