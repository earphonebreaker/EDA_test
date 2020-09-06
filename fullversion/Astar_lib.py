# -*- coding: utf-8 -*-
from random import randint
import time
from SFQ_lib import *
from Layout_lib import *
from Netlist_lib import *
from Param_lib import *
import sys

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
    def get_map_util(self):
        total_point=self.width*self.height
        used_point=0
        for x in range(self.width):
            for y in range(self.height):
                if(self.map[y][x]!=0):
                    used_point=used_point+1
        util_temp=float(used_point/total_point)*10000
        util=int(util_temp)
        print("Total point:{0}".format(total_point))
        print("Used point:{0}".format(used_point))       
        return util

    def createBlock(self, block_num):
        for i in range(block_num):
            x, y = (randint(0, self.width-1), randint(0, self.height-1))
            self.map[y][x] = 1

    def getValue(self, coord):
        if(coord[1]>=0 and coord[0]>=0):
            value=self.map[coord[1]][coord[0]]
        return value
    def setValue(self, coord, value):#设置某点的值
        if(coord[1]>=0 and coord[0]>=0):
            self.map[coord[1]][coord[0]]=value
    def setValue_mul(self,coord_list,value):#设置list中所有的点为同一个值
        for c in coord_list:
            if(c[1]>=0 and c[0]>=0 and self.map[c[1]][c[0]]!=1):
                self.map[c[1]][c[0]]=value

    def setBlock(self,block_list): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x>=0 and y>=0 and x<self.width and y<self.height):
                self.map[y][x] = 1
    def setBlock_basic(self,block_list,start): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        corner=[]
        cross_extend_list=[]
        for i in range(1,block_list_len-1):
            x=block_list[i][0]
            y=block_list[i][1]
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0):
                continue
            if(self.map[y][x]==2):
                self.map[y][x]=3
                self.map[y_prev][x_prev] = 3
                cross_extend_list.append([x_next,y_next])            
                #self.map[y_next][x_next] = 3   
            elif(self.map[y][x]==3):
                pass
        for c in cross_extend_list:
            self.map[c[1]][c[0]]=3
        for i in range(0,start+3):#屏蔽前后四个单元？可以考虑换成两个
            x_start=block_list[i][0]
            y_start=block_list[i][1]
            x_end=block_list[block_list_len-1-i][0]
            y_end=block_list[block_list_len-1-i][1]
            if(x_start>=0 and y_start>=0 and self.map[y_start][x_start]!=3):
                self.map[y_start][x_start] = 1
            if(x_end>=0 and y_end>=0 and self.map[y_end][x_end]!=3):
                self.map[y_end][x_end] = 1

        for i in range(start+3,block_list_len-start-3):#设置中间单元,其中在交叉处设置连续三个3表示mn0层
            x=block_list[i][0]
            y=block_list[i][1]
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0):
                continue
            #if(self.map[y][x]==2):
                #self.map[y][x]=3
                #self.map[y_prev][x_prev] = 3            
                #self.map[y_next][x_next] = 3                     
            elif(self.map[y][x]==3):
                pass
            elif(self.map[y][x]==0):
                self.map[y][x] = 2;
            elif(self.map[y][x]==1):
                self.map[y][x]=1
            elif(self.map[y][x]==5):
                self.map[y][x]=1
        for i in range(2,block_list_len-2):#寻找corner，屏蔽corner前后
            x_prev=block_list[i-1][0]
            y_prev=block_list[i-1][1]
            x_next=block_list[i+1][0]
            y_next=block_list[i+1][1]
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0):
                continue
            if(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1):
                corner.append(i)
        for c in corner:#屏蔽corner的前后两个单元
            x=block_list[c][0]
            y=block_list[c][1]
            x_prev=block_list[c-1][0]
            y_prev=block_list[c-1][1]
            x_next=block_list[c+1][0]
            y_next=block_list[c+1][1]
            x_prev_2=block_list[c-2][0]
            y_prev_2=block_list[c-2][1]
            x_next_2=block_list[c+2][0]
            y_next_2=block_list[c+2][1]
            if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0 or x_prev_2<0 or y_prev_2<0 or x_next_2<0 or y_next_2<0):
                continue
            if(self.map[y][x]!=3):
                self.map[y][x] = 1            
                self.map[y_prev][x_prev] = 1            
                self.map[y_next][x_next] = 1            
                #self.map[y_prev_2][x_prev_2] = 1            
                #self.map[y_next_2][x_next_2] = 1     

    def set_path_regulator(self,path,parity,start):#根据奇偶性来确定屏蔽点坐标
        len_path=len(path)
        cross_point=[]
        for i in range(start+3,len_path-start-3):#检查奇偶性
            x=path[i][0]
            y=path[i][1]
            x_prev=path[i-1][0]
            y_prev=path[i-1][1]
            x_next=path[i+1][0]
            y_next=path[i+1][1]
            if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0):
                continue
            if(abs(x_next-x_prev)==2):#确定为直线x走向
                if(parity=="odd"and self.map[y][x]==2):
                    if(x%2 == 0):#查找x坐标为奇数点
                        a=1
                    else:
                        cross_point.append([x,y])
                elif(parity=="even"and self.map[y][x]==2):
                    if(x%2 != 0):#查找x坐标为偶数点
                        a=1
                    else:
                        cross_point.append([x,y])
            elif(abs(y_next-y_prev)==2):#确定为直线y走向
                if(parity=="odd" and self.map[y][x]==2):
                    if(y%2 == 0):#确定y坐标为奇数点
                        a=1
                    else:
                        cross_point.append([x,y])
                elif(parity=="even"and self.map[y][x]==2):
                    if(y%2 != 0):#确定y坐标为偶数点
                        a=1
                    else:
                        cross_point.append([x,y])
        return cross_point #返回cross可通行点坐标

    def get_regulate_point(self,path,regulate_cross,start):#根据屏蔽点坐标或者原来是1的地方添加regulator
        len_path=len(path)
        regulate_point=[]
        for i in range(start,len_path-start):
            if(i==0 or i==len_path-1):
                pass

            else:
                x=path[i][0]
                y=path[i][1]
                x_prev=path[i-1][0]
                y_prev=path[i-1][1]
                x_next=path[i+1][0]
                y_next=path[i+1][1]
                if(x<0 or y<0 or x_prev<0 or y_prev<0 or x_next<0 or y_next<0):
                    continue
                if(abs(x_prev-x_next)==2):
                    direction="h"
                elif(abs(y_prev-y_next)==2):
                    direction="v"
                elif(abs(x_prev-x_next)==1 and abs(y_prev-y_next)==1):
                    direction="c"
                else:
                    print(x,y)
                    direction="unknown"#????
                if(direction=="h" and (self.map[y][x]==1 or [x,y] in regulate_cross)):
                    regulate_point.append([x,y-1])
                    regulate_point.append([x,y+1])
                    regulate_point.append([x,y-2])
                    regulate_point.append([x,y+2])
                elif(direction=="v" and (self.map[y][x]==1 or [x,y] in regulate_cross)):
                    regulate_point.append([x+1,y])
                    regulate_point.append([x-1,y])
                    regulate_point.append([x+2,y])
                    regulate_point.append([x-2,y])
                elif(direction=="c"):
                    pass
        return regulate_point

    def read_path_type(self,path):#获取当前的path类别
        len_path=len(path)
        line_info=[]
        for i in range(0,len_path):
            x=path[i][0]
            y=path[i][1]
            if(x<0 or y<0):
                continue
            line_info.append(self.map[y][x])
        return line_info
    
    def clrBlock(self,block_list): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0):
                continue
            self.map[y][x] = 0;

    def get_blocked_point(self,block_list):#用来检查block_list里的点是否原来就是封死的，返回一个原来是封死的list，防止clrblock时把原来的也清掉了
        block_list_len=len(block_list)
        prev_block=[]
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0):
                continue
            if(self.map[y][x]==1):
                prev_block.append([x,y])
        return prev_block
    
    def get_cross_enable(self,block_list):#用来检查block_list里的点是否原来是2
        block_list_len=len(block_list)
        prev_en=[]
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0):
                continue
            if(self.map[y][x]==2):
                prev_en.append([x,y])
        return prev_en
    
    
    def get_regulator_point(self,block_list):#用来检查block_list里的点是否原来是5
        block_list_len=len(block_list)
        prev_en=[]
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0):
                continue
            if(self.map[y][x]==5):
                prev_en.append([x,y])
        return prev_en
    
    def setBlock_to2(self,block_list): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        for i in range(0,block_list_len):
            x=block_list[i][0]
            y=block_list[i][1]
            if(x<0 or y<0):
                continue
            self.map[y][x] = 2;
            
    
    def generatePos(self, rangeX, rangeY):
        x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        while self.map[y][x] == 1:
            x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        return (x , y)
        
    def showMap(self):
        print("+" * (3 * self.width + 2))
        len_row=len(self.map)
        #print(len_row)
        for i in range(len_row):
            s = '+'
            len_col=len(self.map[len_row-i-1])
            #print(self.map[len_row-i-1])
            for j in range(len_col):
                if(self.map[len_row-i-1][j]!=0):
                    s +=' '+ str(self.map[len_row-i-1][j]) + ' '
                else:
                    s +=' '+ ' ' + ' '
            s +='+'
            print(s)

        print("+" * (3 * self.width + 2))

    def clr_port_area(self,x,y,index):
        if(index==1):
            clr_list1=[[x-1,y],[x-2,y],[x-2,y+1],[x-2,y+2],[x-2,y+3],[x-2,y+4],[x-1,y+4],[x,y+4],[x+1,y+4],[x+1,y+3],[x+1,y+2]]
            clr_list2=[[x-2,y-1],[x-2,y-2],[x-2,y-3],[x-2,y-4],[x-1,y-4],[x,y-4],[x+1,y-4],[x+1,y-3],[x+1,y-2]]
            for c in clr_list1:#清除port周边的5
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for c in clr_list2:
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for i in range(0,2):#设置port周边的1和2全部为1
                for j in range(1,6):
                    if(self.map[y+j][x-3-i] == 2 ):
                        self.map[y+j][x-3-i]=1
                    if(self.map[y-j][x-3-i] == 2 ):
                        self.map[y-j][x-3-i]=1
                    if(self.map[y+5+i][x-4+j] == 2 ):
                        self.map[y+5+i][x-4+j] = 1
                    if(self.map[y-5-i][x-4+j] == 2 ):
                        self.map[y-5-i][x-4+j] = 1
            for i in range(0,3):#重新在port附近设置regulator
                for j in range(0,2):
                    if(self.map[y+5+i][x-4+j] in [1,2]):
                        if(self.map[y+5+i][x-3+j]==0):                        
                            self.map[y+5+i][x-3+j]=5
                        if(self.map[y+5+i][x-2+j]==0):                        
                            self.map[y+5+i][x-2+j]=5
                    if(self.map[y-5-i][x-4+j] in [1,2]):
                        if(self.map[y-5-i][x-3+j]==0):                        
                            self.map[y-5-i][x-3+j]=5
                        if(self.map[y-5-i][x-2+j]==0):                        
                            self.map[y-5-i][x-2+j]=5
                    if(self.map[y+5+j][x+2+i] in [1,2]):
                        if(self.map[y+4+j][x+2+i]==0):                        
                            self.map[y+4+j][x+2+i]=5
                        if(self.map[y+3+j][x+2+i]==0):                        
                            self.map[y+3+j][x+2+i]=5
                    if(self.map[y-5-j][x+2+i] in [1,2]):
                        if(self.map[y-4-i][x+2+i]==0):                        
                            self.map[y-4-i][x+2+i]=5
                        if(self.map[y-3-i][x+2+i]==0):                        
                            self.map[y-3-i][x+2+i]=5
        elif(index==2):
            clr_list1=[[x,y-1],[x,y-2],[x+1,y-2],[x+2,y-2],[x+3,y-3],[x+4,y-2],[x+4,y-1],[x+4,y],[x+4,y+1],[x+3,y+1],[x+2,y+1]]
            clr_list2=[[x-1,y-2],[x-2,y-2],[x-3,y-3],[x-4,y-2],[x-4,y-1],[x-4,y],[x-4,y+1],[x-3,y+1],[x-2,y+1]]
            for c in clr_list1:#清除port周边的5
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for c in clr_list2:
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for i in range(0,2):#设置port周边的1和2全部为1
                for j in range(1,6):
                    if(self.map[y-3-i][x+j] == 2 ):
                        self.map[y-3-i][x+j]=1
                    if(self.map[y-3-i][x-j] == 2 ):
                        self.map[y-3-i][x-j]=1
                    if(self.map[y-4+j][x+5+i] == 2 ):
                        self.map[y-4+j][x+5+i] = 1
                    if(self.map[y-4+j][x-5-i] == 2 ):
                        self.map[y-4+j][x-5-i] = 1
            for i in range(0,3):#重新在port附近设置regulator
                for j in range(0,2):
                    if(self.map[y-4+j][x+5+i] in [1,2]):
                        if(self.map[y-3+j][x+5+i]==0):                        
                            self.map[y-3+j][x+5+i]=5
                        if(self.map[y-2+j][x+5+i]==0):                        
                            self.map[y-2+j][x+5+i]=5
                    if(self.map[y-4+j][x-5-i] in [1,2]):
                        if(self.map[y-3+j][x-5-i]==0):                        
                            self.map[y-3+j][x-5-i]=5
                        if(self.map[y-2+j][x-5-i]==0):                        
                            self.map[y-2+j][x-5-i]=5
                    if(self.map[y+2+i][x+5+j] in [1,2]):
                        if(self.map[y+2+i][x+4+j]==0):                        
                            self.map[y+2+i][x+4+j]=5
                        if(self.map[y+2+i][x+3+j]==0):                        
                            self.map[y+2+i][x+3+j]=5
                    if(self.map[y+2+i][x-5-j] in [1,2]):
                        if(self.map[y+2+i][x-4-i]==0):                        
                            self.map[y+2+i][x-4-i]=5
                        if(self.map[y+2+i][x-3-i]==0):                        
                            self.map[y+2+i][x-3-i]=5
        elif(index==3):
            clr_list1=[[x+1,y],[x+2,y],[x+2,y+1],[x+2,y+2],[x+2,y+3],[x+2,y+4],[x+1,y+4],[x,y+4],[x-1,y+4],[x-1,y+3],[x-1,y+2]]
            clr_list2=[[x+2,y-1],[x+2,y-2],[x+2,y-3],[x+2,y-4],[x+1,y-4],[x,y-4],[x-1,y-4],[x-1,y-3],[x-1,y-2]]
            for c in clr_list1:#清除port周边的5
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for c in clr_list2:
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for i in range(0,2):#设置port周边的1和2全部为1
                for j in range(1,6):
                    if(self.map[y+j][x+3+i] == 2 ):
                        self.map[y+j][x+3+i]=1
                    if(self.map[y-j][x+3+i] == 2 ):
                        self.map[y-j][x+3+i]=1
                    if(self.map[y+5+i][x+4-j] == 2 ):
                        self.map[y+5+i][x+4-j] = 1
                    if(self.map[y-5-i][x+4-j] == 2 ):
                        self.map[y-5-i][x+4-j] = 1
            for i in range(0,3):#重新在port附近设置regulator
                for j in range(0,2):
                    if(self.map[y+5+i][x+4-j] in [1,2]):
                        if(self.map[y+5+i][x+3-j]==0):                        
                            self.map[y+5+i][x+3-j]=5
                        if(self.map[y+5+i][x+2-j]==0):                        
                            self.map[y+5+i][x+2-j]=5
                    if(self.map[y-5-i][x+4-j] in [1,2]):
                        if(self.map[y-5-i][x+3-j]==0):                        
                            self.map[y-5-i][x+3-j]=5
                        if(self.map[y-5-i][x+2-j]==0):                        
                            self.map[y-5-i][x+2-j]=5
                    if(self.map[y+5+j][x-2-i] in [1,2]):
                        if(self.map[y+4+j][x-2-i]==0):                        
                            self.map[y+4+j][x-2-i]=5
                        if(self.map[y+3+j][x-2-i]==0):                        
                            self.map[y+3+j][x-2-i]=5
                    if(self.map[y-5-j][x-2-i] in [1,2]):
                        if(self.map[y-4-i][x-2-i]==0):                        
                            self.map[y-4-i][x-2-i]=5
                        if(self.map[y-3-i][x-2-i]==0):                        
                            self.map[y-3-i][x-2-i]=5

        elif(index==4):
            clr_list1=[[x,y+1],[x,y+2],[x+1,y+2],[x+2,y+2],[x+3,y+3],[x+4,y+2],[x+4,y+1],[x+4,y],[x+4,y-1],[x+3,y-1],[x+2,y-1]]
            clr_list2=[[x-1,y+2],[x-2,y+2],[x-3,y+3],[x-4,y+2],[x-4,y+1],[x-4,y],[x-4,y-1],[x-3,y-1],[x-2,y-1]]
            for c in clr_list1:#清除port周边的5
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for c in clr_list2:
                if(self.map[c[1]][c[0]]==5):
                    self.map[c[1]][c[0]]=0
            for i in range(0,2):#设置port周边的1和2全部为1
                for j in range(1,6):
                    if(self.map[y+3+i][x+j] == 2 ):
                        self.map[y+3+i][x+j]=1
                    if(self.map[y+3+i][x-j] == 2 ):
                        self.map[y+3+i][x-j]=1
                    if(self.map[y+4-j][x+5+i] == 2 ):
                        self.map[y+4-j][x+5+i] = 1
                    if(self.map[y+4-j][x-5-i] == 2 ):
                        self.map[y+4-j][x-5-i] = 1
            for i in range(0,3):#重新在port附近设置regulator
                for j in range(0,2):
                    if(self.map[y+4-j][x+5+i] in [1,2]):
                        if(self.map[y+3-j][x+5+i]==0):                        
                            self.map[y+3-j][x+5+i]=5
                        if(self.map[y+2-j][x+5+i]==0):                        
                            self.map[y+2-j][x+5+i]=5
                    if(self.map[y+4-j][x-5-i] in [1,2]):
                        if(self.map[y+3-j][x-5-i]==0):                        
                            self.map[y+3-j][x-5-i]=5
                        if(self.map[y+2-j][x-5-i]==0):                        
                            self.map[y+2-j][x-5-i]=5
                    if(self.map[y-2-i][x+5+j] in [1,2]):
                        if(self.map[y-2-i][x+4+j]==0):                        
                            self.map[y-2-i][x+4+j]=5
                        if(self.map[y-2-i][x+3+j]==0):                        
                            self.map[y-2-i][x+3+j]=5
                    if(self.map[y-2-i][x-5-j] in [1,2]):
                        if(self.map[y-2-i][x-4-i]==0):                        
                            self.map[y-2-i][x-4-i]=5
                        if(self.map[y-2-i][x-3-i]==0):                        
                            self.map[y-2-i][x-3-i]=5


def AStarSearch(map, source, dest):
    def getNewPosition(map, locatioin, offset):
        x,y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1 or map.map[y][x] == 3 or  map.map[y][x] == 4 or  map.map[y][x] == 5:
            return None #这里添加map中的屏蔽点
        return (x, y)

    def getPositions(map, location):#这里设置寻路类型，使用曼哈顿或折线距离 #当前pcell生成函数用曼哈顿距离
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
    def getCorner(last_pos,next_pos,location):
        if(last_pos==None):
            return 0
        else:
            delta_x=abs(last_pos[0]-next_pos[0])
            delta_y=abs(last_pos[1]-next_pos[1])
            #print(last_pos,next_pos,location.getPos())
            if(delta_x==1 and delta_y==1):
                #print("find corner at {0},{1} to {2},{3} via {4}".format(last_pos[0],last_pos[1],next_pos[0],next_pos[1],location.getPos()))
                return 1 
            else:
                return 0
    # check if the position is in list
    def isInList(list, pos):
        if pos in list:
            return list[pos]
        return None
    
    # add available adjacent positions
    def addAdjacentPositions(map, location, dest, openlist, closedlist , last_pos):
        poslist = getPositions(map, location)
        for pos in poslist:
            # if position is already in closedlist, do nothing
            if isInList(closedlist, pos) is None:
                findEntry = isInList(openlist, pos)
                h_cost = calHeuristic(pos, dest)
                c_cost = getCorner(last_pos,pos,location)
                g_cost = location.g_cost + getMoveCost(location, pos)+c_cost
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
            #print("can't find valid path")#这里添加查找失败返回值
            break;
        
        if location.x == dest.x and location.y == dest.y:
            break

        closedlist[location.getPos()] = location
        openlist.pop(location.getPos())
        if(location.pre_entry==None):
            last_pos=None
        else:
            last_pos=[location.pre_entry.x,location.pre_entry.y]
        addAdjacentPositions(map, location, dest, openlist, closedlist,last_pos)

    #mark the found path at the map
    path_temp=[]
    while location is not None:
        #map.map[location.y][location.x] = 2
        #print(location.x,location.y)
        path_temp.append([location.x,location.y])
        location = location.pre_entry
    #print(path_temp)
    #print(path_temp_2)
    path=path_temp[::-1]
    #print(path_temp_3)
    return path
'''def get_path_location(map):#废弃函数
    #print(map)
    len_x=len(map)
    path=[]
    for i in range(len_x):
        len_y=len(map[i])
        for j in range(len_y):
            if(map[j][i]==2):
                path.append([i,j])
    return path'''
def get_group(coord_info,block_margin):
    range_list=[]
    start_time=time.time()
    first_start=coord_info[0][0][0]
    first_end=coord_info[0][1][0]
    first_start_x=first_start[0]
    first_start_y=first_start[1]
    first_end_x=first_end[0]
    first_end_y=first_end[1]
    new_range=[[min(first_start_x,first_end_x)-block_margin,min(first_start_y,first_end_y)-block_margin],\
               [max(first_start_x,first_end_x)+block_margin,max(first_start_y,first_end_y)+block_margin]]
    range_list.append(new_range)
    for r in range(1,len(coord_info)):
        start=coord_info[r][0][0]
        end=coord_info[r][1][0]
        start_x=start[0]
        start_y=start[1]
        end_x=end[0]
        end_y=end[1]
        overlap_list=[]
        for o in range(len(range_list)):
            range_x_min=range_list[o][0][0]
            range_x_max=range_list[o][1][0]
            range_y_min=range_list[o][0][1]
            range_y_max=range_list[o][1][1]
            mod_bottomleft=[min(start_x,end_x)-block_margin,min(start_y,end_y)-block_margin]
            mod_topright=[max(start_x,end_x)+block_margin,max(start_y,end_y)+block_margin]
             
            center_dx=abs((mod_bottomleft[0]+mod_topright[0])/2-(range_x_min+range_x_max)/2)
            center_dy=abs((mod_bottomleft[1]+mod_topright[1])/2-(range_y_min+range_y_max)/2)
            mod_width=abs(mod_topright[0]-mod_bottomleft[0])
            mod_height=abs(mod_topright[1]-mod_bottomleft[1])
            range_width=abs(range_x_max-range_x_min)
            range_height=abs(range_y_max-range_y_min)
             
            condition_loop=(center_dx<=(mod_width+range_width)/2)and(center_dy<=(mod_height+range_height)/2)
             
            if(condition_loop):
                overlap_list.append(o)
            else:
                pass
        if(overlap_list==[]):#说明是新的范围
            new_range=[[min(start_x,end_x)-block_margin,min(start_y,end_y)-block_margin],\
                        [max(start_x,end_x)+block_margin,max(start_y,end_y)+block_margin]]
            range_list.append(new_range)
        elif(len(overlap_list)==1):#只有一个重合了
            index=overlap_list[0]
            new_range=[[min(start_x,end_x)-block_margin,min(start_y,end_y)-block_margin],\
                        [max(start_x,end_x)+block_margin,max(start_y,end_y)+block_margin]]

            range_value=range_list[index]

            range_xmin_list=[new_range[0][0],range_value[0][0]]
            range_xmax_list=[new_range[1][0],range_value[1][0]]
            range_ymin_list=[new_range[0][1],range_value[0][1]]
            range_ymax_list=[new_range[1][1],range_value[1][1]] 
            new_range_sum=[[min(range_xmin_list),min(range_ymin_list)],[max(range_xmax_list),max(range_ymax_list)]]
            range_list[index]=new_range_sum        

        else: #说明几个范围有重合，需要把他们融合在一起
            new_range=[[min(start_x,end_x)-block_margin,min(start_y,end_y)-block_margin],\
                        [max(start_x,end_x)+block_margin,max(start_y,end_y)+block_margin]]
            range_xmin_list=[new_range[0][0]]
            range_xmax_list=[new_range[1][0]]
            range_ymin_list=[new_range[0][1]]
            range_ymax_list=[new_range[1][1]]
            for i in range(0,len(overlap_list)):
                index=overlap_list[i]
                range_value=range_list[index]
                range_xmin_list.append(range_value[0][0])
                range_xmax_list.append(range_value[1][0])
                range_ymin_list.append(range_value[0][1])
                range_ymax_list.append(range_value[1][1])
            new_range_sum=[[min(range_xmin_list),min(range_ymin_list)],[max(range_xmax_list),max(range_ymax_list)]]
            range_list[overlap_list[0]]=new_range_sum
            for i in range(1,len(overlap_list),-1):
                index=overlap_list[i]
                range_list.pop(index)

        
    len_before_arr=len(range_list)
    k=0
    j=1
    rearr_cycle=0
    while True:
        if(k==len(range_list)):
            break
        if((k+j)==len(range_list)):
            k=k+1
            j=1
            continue
        prev_range=range_list[k]
        curr_range=range_list[k+j]
        prev_bottomleft=prev_range[0]
        prev_topright=prev_range[1]
        curr_bottomleft=curr_range[0]
        curr_topright=curr_range[1]
            
        prev_center_x=(prev_bottomleft[0]+prev_topright[0])/2
        prev_center_y=(prev_bottomleft[1]+prev_topright[1])/2
        curr_center_x=(curr_bottomleft[0]+curr_topright[0])/2
        curr_center_y=(curr_bottomleft[1]+curr_topright[1])/2
        center_dx=abs(prev_center_x-curr_center_x)
        center_dy=abs(prev_center_y-curr_center_y)
        prev_width=abs(prev_bottomleft[0]-prev_topright[0])
        prev_height=abs(prev_bottomleft[1]-prev_topright[1])
        curr_width=abs(curr_bottomleft[0]-curr_topright[0])
        curr_height=abs(curr_bottomleft[1]-curr_topright[1])
        condition=(center_dx<=(prev_width+curr_width)/2) and (center_dy<=(prev_height+curr_height)/2)
            
        if(condition):

            new_range=[[min(curr_bottomleft[0],prev_bottomleft[0]),min(curr_bottomleft[1],prev_bottomleft[1])],\
            [max(curr_topright[0],prev_topright[0]),max(curr_topright[1],prev_topright[1])]]
            range_list[k]=new_range
            range_list.pop(k+j)
            k=0
            j=1
        else:
            j=j+1
        rearr_cycle+=1
            
    def in_range(point,range_list):
        px=point[0]
        py=point[1]
        for i in range(len(range_list)):
            range_s_point=range_list[i][0]
            rpsx=range_s_point[0]
            rpsy=range_s_point[1]
            range_e_point=range_list[i][1]
            rpex=range_e_point[0]
            rpey=range_e_point[1]
            x_in=(px>=rpsx) and (px<=rpex)
            y_in=(py>=rpsy) and (py<=rpey)
            if(x_in and y_in):
                return i
    coord_list=[[] for i in range(len(range_list))]
    for r in range(len(coord_info)):
        point=coord_info[r][0][0]
        index=in_range(point,range_list)
        coord_list[index].append(r)

    return range_list,coord_list



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
    block_margin=layout_unit_len*2
    [range_list,index_list]=get_group(coord_info,block_margin)
    info_list=[]
    #print(len(layout_info),len(coord_info))
    for i in range(len(range_list)):
        layout_info_sub=[]
        coord_info_sub=[]
        connection_info_sub=[]
        for index in index_list[i]:
            layout_info_sub.append(layout_info[index])
            coord_info_sub.append(coord_info[index])
            connection_info_sub.append(connection_info[index])
            
        x_s=range_list[i][0][0]
        x_e=range_list[i][1][0]
        y_s=range_list[i][0][1]
        y_e=range_list[i][1][1]
        x_max=x_e-block_margin
        y_max=y_e-block_margin
        x_min=x_s+block_margin
        y_min=y_s+block_margin
        width=int((x_max-x_min)/layout_unit_len+map_enlarge)#设置map的宽度，并读取param_lib里的map_enlarge参数来扩充map
        height=int((y_max-y_min)/layout_unit_len+map_enlarge)#同上，设置高度
        origin=[x_min,y_min]#获取map的初始原点
        map_origin=[int(x_min/layout_unit_len-map_offset),int(y_min/layout_unit_len-map_offset)]#获得一个原点为00的，map相对于layout的坐标（这里2和上面的4以后要调整）

        info_list.append([width,height,layout_info,map_origin,coord_info_sub,connection_info_sub,range_list[i]]) ##temp:use layout info summary --warning: ram insufficient
    return info_list#返回所需信息
#map_info(File_dir)


def cross_map_search(info,lib,cell):
    #布线信息列表
    width=info[0]#获取map最大宽度
    height=info[1]#获取map最大高度
    layout_info=info[2]#获取layout版图信息
    len_layout=len(layout_info)
    map_origin=info[3]#获取layout原点
    coord_info=info[4]#获取互联线坐标
    connection_info=info[5]#获取互联线信息
    #info_coord=open("routing_coord_info","w")
    #print(connection_info,file=info_coord)
    #print(coord_info,file=info_coord)
    coord_len=len(coord_info)
    #map列表
    layout_map_odd=Map(width,height)#奇map
    layout_map_even=Map(width,height)#偶map
    layout_map_nox=Map(width,height)#不允许cross
    layout_map_port=Map(width,height)#记录port位置
    layout_map_reg=Map(width,height)#记录block info

    map_list=[layout_map_odd,layout_map_even,layout_map_nox,layout_map_port] #所有map存在一个list里
    map_for_search_path_num = 3 #前三个map用于寻路
    
    def showMap_all(map_list):#显示所有map函数
        for k in range(0,map_for_search_path_num):
            map_list[k].showMap()
            
    text=open("./createinst.il",'a+')
    cellid='''cellID=dbOpenCellViewByType("{0}" "{1}" "layout" "maskLayout")'''.format(lib,cell)#dbopen函数，指定单元
    print(cellid,file=text)
    #showMap_all(map_list)
    for i in range(0,len_layout):#把版图中的单元作为block放置到map中
        block_point=origin_to_blockpoint_enlarged(layout_info[i].area,layout_info[i].xy,layout_info[i].orient)
        abs_point=get_abs_block_point(map_origin,block_point)
        #print(abs_point)
        for j in range(0,map_for_search_path_num):
            map_list[j].setBlock(abs_point)


    for i in range(0,coord_len):#封锁端口，先把所有端口都封上，在布每一条线的时候再单独打开（clrBlock函数）
        port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
        port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
        port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
        port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
        block_source=[port_2[0],port_2[1]]#获取出发点
        block_dest=[port_1[0],port_1[1]]#获取终点
        for j in range(0,4):#所有map封上端口
            map_list[j].setBlock([block_source,block_dest])

    for x in range(width):#获取一个寄存map，用于在retry过程中恢复所有map至初始状态
        for y in range(height):
            layout_map_reg.setValue([x,y],layout_map_nox.getValue([x,y]))

    script_summary=[]#il文件暂存列表
    failed_path_summary=[]#失败的路径index信息        
    util_summary=[]#每次布线得出的最终map利用率
    log_summary=[]#输出到logger中的信息                
                
    def run_routing(start):#从start到尾的布线函数
        script_all=[]#每次routing时产生的script
        failed_path=[]#每次routing是产生的失败路径
        log_failed_coord=[]
        for i in range(start,coord_len):#注意这里的coord和layout_lib中的某些设置不一样，在后面temp中重新排布
            #print(coord_info[i])
            port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
            port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
            port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
            port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
            source=(port_2[0],port_2[1])#获取出发点
            dest=(port_1[0],port_1[1])#获取终点

            for j in range(0,map_for_search_path_num):
                map_list[j].clrBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])#先清除掉要布线的这条路径的端口block，不然就找不到valid path
            #for j in range(0,map_for_search_path_num-1):#端口清理函数，暂时屏蔽掉，之后重新设计端口清理功能
                #map_list[j].clr_port_area(port_1[0],port_1[1],coord_info[i][0][1])
                #map_list[j].clr_port_area(port_2[0],port_2[1],coord_info[i][1][1])

            #------------get regulator lenth-----------------
            max_port_reg_try=7#暂定，增加这个值会增大布线所用时间
            min_port_reg_try=2#最小必须为2，保证regulator长度为3，confirmed
            x_delta=port_2[0]-port_1[0]#以下程序段获取出发点和终点的坐标差，来确定端口处保持多长的直线路径
            y_delta=port_2[1]-port_1[1]
            horizon_index = coord_info[i][0][1] in [1,3] and coord_info[i][1][1] in [1,3]
            vertical_index = coord_info[i][0][1] in [2,4] and coord_info[i][1][1] in [2,4]
            if(horizon_index):
                max_port_reg_try_temp=abs(int(x_delta/2))-1
            elif(vertical_index):
                max_port_reg_try_temp=abs(int(y_delta/2))-1
            else:
                max_port_reg_try_temp=min([abs(int(x_delta/2))-1,abs(int(y_delta/2))-1])
            if(max_port_reg_try_temp<max_port_reg_try and max_port_reg_try_temp>=3):
                max_port_reg_try=max_port_reg_try_temp
            elif(max_port_reg_try_temp<3):
                max_port_reg_try=3
            #---------------------------------------------
            #先在map3中找最短
            regulate_point_map3_1=regulate_route_new(port_1,coord_info[i][0][1],4)#regulate端口处，source
            regulate_point_map3_2=regulate_route_new(port_2,coord_info[i][1][1],4)#regulate端口处,dest
            prev_block_map3_1=map_list[2].get_blocked_point(regulate_point_map3_1)#获取1屏蔽
            prev_block_map3_2=map_list[2].get_blocked_point(regulate_point_map3_2)
            map_list[2].setBlock(regulate_point_map3_1)#设置regulator
            map_list[2].setBlock(regulate_point_map3_2)
            path_map3=AStarSearch(map_list[2],source,dest)#A星算path
            if(len(path_map3)==0):#当前设置先测试4个长度的regulator，无效再测试3个长度
                map_list[2].clrBlock(regulate_point_map3_1)#以下为恢复port regulator并开始下一步的求路径
                map_list[2].clrBlock(regulate_point_map3_2)
                map_list[2].setBlock(prev_block_map3_1)
                map_list[2].setBlock(prev_block_map3_2)
                map_list[2].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
                regulate_point_map3_1=regulate_route_new(port_1,coord_info[i][0][1],3)#regulate端口处，source
                regulate_point_map3_2=regulate_route_new(port_2,coord_info[i][1][1],3)#regulate端口处,dest
                prev_block_map3_1=map_list[2].get_blocked_point(regulate_point_map3_1)
                prev_block_map3_2=map_list[2].get_blocked_point(regulate_point_map3_2)
                map_list[2].setBlock(regulate_point_map3_1)
                map_list[2].setBlock(regulate_point_map3_2)
                path_map3=AStarSearch(map_list[2],source,dest)#A星算path
                if(len(path_map3)==0):#若找不到路径则把路径长度置为无穷大
                    path_len_map3=inf
                else:
                    path_len_map3=len(path_map3)#记录当前path的长度
            else:#若regulator=4有解则使用regulator=4的情况作为reference
                path_len_map3=len(path_map3)#记录当前path的长度

            #recover activity in map 3
            map_list[2].clrBlock(regulate_point_map3_1)
            map_list[2].clrBlock(regulate_point_map3_2)
            map_list[2].setBlock(prev_block_map3_1)
            map_list[2].setBlock(prev_block_map3_2)
            map_list[2].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
            #--------------------------------------------------------------------------------------------

            for m in range(max_port_reg_try,min_port_reg_try,-1):#iteration开始
                print("iteration {0} at path {1}".format(max_port_reg_try-m+1,i+1))
                regulate_point1=regulate_route_new(port_1,coord_info[i][0][1],m)#regulate端口处，source
                regulate_point2=regulate_route_new(port_2,coord_info[i][1][1],m)#regulate端口处,dest
                #暂存map中原来的数据
                prev_1_source=[]
                prev_2_source=[]
                prev_5_source=[]
                prev_1_dest=[]
                prev_2_dest=[]
                prev_5_dest=[]
                prev_5_source2=[]
                prev_5_dest2=[]
                min_path=[]
                #获取原来的数据，记录下后设置port regulator
                for k in range(0,map_for_search_path_num-1):#每一个map都做regulator
                    prev_block_1=map_list[k].get_blocked_point(regulate_point1)#以下记录原来的map数据
                    prev_block_2=map_list[k].get_blocked_point(regulate_point2)
                    prev_en_1=map_list[k].get_cross_enable(regulate_point1)
                    prev_en_2=map_list[k].get_cross_enable(regulate_point2)
                    prev_reg_1=map_list[k].get_regulator_point(regulate_point1)
                    prev_reg_2=map_list[k].get_regulator_point(regulate_point2)
                    prev_1_source.append(prev_block_1)
                    prev_1_dest.append(prev_block_2)
                    prev_2_source.append(prev_en_1)
                    prev_2_dest.append(prev_en_2)
                    prev_5_source.append(prev_reg_1)
                    prev_5_dest.append(prev_reg_2)
                    map_list[k].setBlock(regulate_point1)
                    map_list[k].setBlock(regulate_point2)
                #print("--------------------port regulator,path:{0}-----------------------".format(i))    
                #showMap_all(map_list)
                path=[]
                path_len=[]
                #showMap_all(map_list)
                #测试 1 2 map是否有path并是否满足要求，如果没有则恢复regulator并跳出
                for k in range(0,map_for_search_path_num-1):#3个map中查找对应的路径
                    path_curr=AStarSearch(map_list[k],source,dest)#A星算path
                    path_len_curr=len(path_curr)#记录当前path的长度
                    if(path_len_curr==0):#如果为0则表示找不到路径，设置长度为无穷大
                        path_len.append(inf)
                    else:#不为0则写入list
                        path_len.append(path_len_curr)
                    path.append(path_curr)
                path.append(path_map3)
                path_len.append(path_len_map3)
                min_path_index=path_len.index(min(path_len))#查找最短的路径index
                #print(path_len)
                #print(min_path_index)
                min_path=path[min_path_index]#记录最短路径
                #print(min_path)
                if(path_len[min_path_index]==inf and m==min_port_reg_try+1):#如果直到最后也没有有效路径，则跳出
                    print("No valid path")
                    for k in range(0,map_for_search_path_num-1):#以下恢复port regulator覆盖的点的初始值，并删除port regulator
                        prev_reg_1=map_list[k].get_regulator_point(regulate_point1)
                        prev_reg_2=map_list[k].get_regulator_point(regulate_point2)
                        prev_5_source2.append(prev_reg_1)
                        prev_5_dest2.append(prev_reg_2)
                        map_list[k].clrBlock(regulate_point1)
                        map_list[k].clrBlock(regulate_point2)
                        map_list[k].setBlock(prev_1_source[k])
                        map_list[k].setBlock(prev_1_dest[k])
                        map_list[k].setBlock_to2(prev_2_source[k])
                        map_list[k].setBlock_to2(prev_2_dest[k])
                        map_list[k].setValue_mul(prev_5_source[k],5)
                        map_list[k].setValue_mul(prev_5_dest[k],5)
                        map_list[k].setValue_mul(prev_5_source2[k],5)
                        map_list[k].setValue_mul(prev_5_dest2[k],5)
                        map_list[k].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
                    continue
                elif( path_len[0]>path_len_map3 and path_len[1]>path_len_map3 and m!=min_port_reg_try+1):#若不满足要求，且index不为2，则进行下一轮iteration
                    for k in range(0,map_for_search_path_num-1):#以下恢复port regulator覆盖的点的初始值，并删除port regulator
                        prev_reg_1=map_list[k].get_regulator_point(regulate_point1)
                        prev_reg_2=map_list[k].get_regulator_point(regulate_point2)
                        prev_5_source2.append(prev_reg_1)
                        prev_5_dest2.append(prev_reg_2)
                        map_list[k].clrBlock(regulate_point1)
                        map_list[k].clrBlock(regulate_point2)
                        map_list[k].setBlock(prev_1_source[k])
                        map_list[k].setBlock(prev_1_dest[k])
                        map_list[k].setBlock_to2(prev_2_source[k])
                        map_list[k].setBlock_to2(prev_2_dest[k])
                        map_list[k].setValue_mul(prev_5_source[k],5)
                        map_list[k].setValue_mul(prev_5_dest[k],5)
                        map_list[k].setValue_mul(prev_5_source2[k],5)
                        map_list[k].setValue_mul(prev_5_dest2[k],5)
                        #map_list[j].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
                    print("failed, try again")
                    #showMap_all(map_list)
                    continue #跳到for m循环起始处，m-1后继续测试
                elif(path_len[min_path_index]>=min_port_reg_try and path_len[min_path_index]!=inf):#如果能直接找到路径则寻找最短 # minimal path len is ?
                    map_list[0].setBlock_basic(min_path,m)#map1和2设置为可交叉
                    map_list[1].setBlock_basic(min_path,m)
                    map_list[2].setBlock(min_path)#第三个map设置为全屏蔽

                    #map_list[2].setBlock(min_path)#第三个map设置为全屏蔽
                    #print("--------------------show map,path:{0}-----------------------".format(i))    
                    #showMap_all(map_list)
                    for k in range(0,map_for_search_path_num-1):#清除port regulator，同上
                        prev_reg_1=map_list[k].get_regulator_point(regulate_point1)
                        prev_reg_2=map_list[k].get_regulator_point(regulate_point2)
                        prev_5_source2.append(prev_reg_1)
                        prev_5_dest2.append(prev_reg_2)
                        map_list[k].clrBlock(regulate_point1)
                        map_list[k].clrBlock(regulate_point2)
                        map_list[k].setBlock(prev_1_source[k])
                        map_list[k].setBlock(prev_1_dest[k])
                        map_list[k].setBlock_to2(prev_2_source[k])
                        map_list[k].setBlock_to2(prev_2_dest[k])
                        map_list[k].setValue_mul(prev_5_source[k],5)
                        map_list[k].setValue_mul(prev_5_dest[k],5)
                        map_list[k].setValue_mul(prev_5_source2[k],5)
                        map_list[k].setValue_mul(prev_5_dest2[k],5)
                        map_list[k].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
                    return_path=map_list[min_path_index].read_path_type(min_path)#获取path的类型

                    regulator_odd=map_list[0].set_path_regulator(min_path,"odd",m)#获取奇屏蔽的点
                    regulator_even=map_list[1].set_path_regulator(min_path,"even",m)#获取偶屏蔽的点

                    get_reg_odd=map_list[0].get_regulate_point(min_path,regulator_odd,m)#获取奇屏蔽regulator
                    get_reg_even=map_list[1].get_regulate_point(min_path,regulator_even,m)#获取偶屏蔽regulator
                    #对应map添加regulator
                    #print("--------------------show reg,path:{0}-----------------------".format(i))    
                    map_list[0].setBlock(regulator_odd) #添加path regulator
                    map_list[0].setValue_mul(get_reg_odd,5)           
                    map_list[1].setBlock(regulator_even) 
                    map_list[1].setValue_mul(get_reg_even,5)
                    #showMap_all(map_list)
                    #print("--------------------clear port regulator,path:{0}-----------------------".format(i))    

                    #showMap_all(map_list)

                    break#跳出for m 循环 不继续执行



            #get pcell path according to min_path

            temp=[coord_info[i][1],coord_info[i][0]]#temp来重新排列coord_info
            path_min_temp=min_path
            new_path=[]
            len_path=len(path_min_temp)
            if(len_path>=min_port_reg_try):#minimal path len acceptable is ?
                print("succeed")
                print("--------------------show result,path:{0}-----------------------".format(i+1))
                showMap_all(map_list)

                for k in range(0,len_path):
                    new_path.append([path_min_temp[k][0]+map_origin[0],path_min_temp[k][1]+map_origin[1]])#把还原的path坐标写入new path中
                #print(new_path)
                index_seq=get_index_sequence(new_path,coord_info[i][1][1],last_check_index(coord_info[i][0][1]))#获取path的index序列
                #print(index_seq)
                rtype_seq=get_route_type(index_seq)#获取path的走线类型
                std_path_coord=[]
                for p in range(0,len_path-1):#转为pcell坐标
                    new_path[p]=[new_path[p][0]*layout_unit_len,new_path[p][1]*layout_unit_len]
                    std_path_coord.append(new_path[p])
                    new_path[p]=pcell_coord(new_path[p],index_seq[p])
                #设置最后一个点的pcell坐标
                new_path[-1]=[new_path[-1][0]*layout_unit_len,new_path[-1][1]*layout_unit_len]
                std_path_coord.append(new_path[-1])
                new_path[-1]=pcell_coord(new_path[-1],last_check_index(index_seq[-1]))
                #分析path及其index、走线类型，获取一个pycell程序可读的info list
                info=analyze_path(new_path,return_path,index_seq,rtype_seq,std_path_coord)
                print("source:{0} to destination:{1}".format(new_path[0],new_path[-1]))
                #将info list转变为pycell，生成script记入script_all
                script=path_to_pcell(info,new_path,index_seq)
                script_all.append(script)
            else:#若没有有效的path，则输出失败信息到logger
                print("No valid path from {0} to {1}".format(source,dest))
                failed_path.append(i)
                log_temp="Instance {0} port {1} ({2},{3}) to Instance {4} port {5} ({6},{7})".format(connection_info[i][2],connection_info[i][3].replace("wire",""),
coord_info[i][1][0][0],coord_info[i][1][0][1],connection_info[i][0],connection_info[i][1].replace("wire",""),coord_info[i][0][0][0],coord_info[i][0][0][1])
                log_failed_coord.append(log_temp)
        #记录本次布线循环的所有信息，包括利用率、script、失败的路径index、log信息等
        util=map_list[2].get_map_util()
        script_summary.append(script_all)
        failed_path_summary.append(failed_path)
        util_summary.append(util)
        log_summary.append(log_failed_coord)

    coord_summary=[]#同上面的summary
    connection_summary=[]#同上面的summary

    invalid_loop=False #retry loop检测，若重新排序后和之前某次仿真的序列一样，说明后续所有重排操作进入无限循环
    for t in range(0,try_num):    
        run_routing(0)#运行布线函数
        print("Map utilization:{0}%".format(util_summary[t]/100))
        curr_script_len=len(script_summary[t])#获取本次布线的script长度，来判断本次布线成功与否
        if(curr_script_len==coord_len):#如果成功则终止retry程序
            print("Succeed at cycle {0}, exit searching program".format(t))
            break
        #重新排布coord_info和connection_info，恢复所有map，准备下一次布线
        print("Rearranging connection info sequence and reference map...")
        coord_summary.append(coord_info)
        coord_temp=[]
        connection_summary.append(connection_info)
        connection_temp=[]
        for i in failed_path_summary[t]:
            coord_temp.append(coord_info[i])
            connection_temp.append(connection_info[i])
        for i in range(0,coord_len):
            if(i in failed_path_summary[t]):
                pass
            else:
                coord_temp.append(coord_info[i])
                connection_temp.append(connection_info[i])
        for i in range(0,coord_len):
            coord_info[i]=coord_temp[i]
            connection_info[i]=connection_temp[i]
            
        #检测是否出现重复的coord_info
        for i in range(0,t):
            if(coord_info==coord_summary[t]):
                invalid_loop=True
                break
        if(invalid_loop):#若出现重复coord_info则跳出retry程序
            print("Invalid retry loop, exit")
            break
        for j in range(0,map_for_search_path_num):
            for x in range(width):
                for y in range(height):
                    map_list[j].setValue([x,y],layout_map_reg.getValue([x,y]))
        if(t<try_num-1):#根据retry的次数来输出不同的信息
            print("Start retry program, cycle {0}".format(t+1))
        else:
            print("Reach the largest number of retry cycles, exit")
    #若超出retry的次数仍未break，则从所有布线结果中挑选最优解
    len_script=len(script_summary)
    script_len_list=[]
    for l in range(0,len_script):#计算所有布线结果的script长度
        script_len_list.append(len(script_summary[l]))
    max_script=max(script_len_list)#获取script长度最大值
    temp_max_index = [(i, script_len_list[i]) for i in range(len(script_len_list))]#查找最大值对应的index
    max_index_list=[i for i, n in temp_max_index if n == max_script]#查找最大值对应的index
    if(len(max_index_list)==1):#如果只有一个最大值则直接选这一个
        best_index=max_index_list[0]
    else:#如果有多个最大值则比较map利用率，选最小的 #如果多个map利用率相同则取第一个，如果以后有别的影响因素再进一步筛选
        util_temp_list=[]
        for u in max_index_list:
            util_temp_list.append(util_summary[u])
        util_min_index=util_temp_list.index(min(util_temp_list))
        best_index=max_index_list[util_min_index]
    #print(max_script_length_index)
    for s in range(0,script_len_list[best_index]):#输出最长script
        for script_str in script_summary[best_index][s]:
            print(script_str,file=text)
    print("---------------------------------summary-------------------------------------")#以下输出summary信息
    if(len_script==1):
        print("All path finished successfully without running retry program")
    else:
        print("Best result is from cycle {0}".format(best_index+1))
        if(len(log_summary[best_index])!=0):
            for failed_path in log_summary[best_index]:
                print("Failed:{0}".format(failed_path))
        else:
            print("All path finished successfully after running retry program")
    print("Current map utilization is {0}%".format(util_summary[best_index]/100))
    text.close()