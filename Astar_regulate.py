#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import randint
import time
from SFQ_lib import *
from Layout_lib import *
from Netlist_lib import *
from Param_lib import *
start=time.time()
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

    def createBlock(self, block_num):
        for i in range(block_num):
            x, y = (randint(0, self.width-1), randint(0, self.height-1))
            self.map[y][x] = 1
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
            if(x>=0 and y>=0):
                self.map[y][x] = 1
    def setBlock_basic(self,block_list,start): #block list 储存已经存在的单元位置信息
        block_list_len=len(block_list)
        corner=[]

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
                self.map[y_next][x_next] = 3   
            elif(self.map[y][x]==3):
                pass

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
            #print("can't find valid path")#这里添加查找失败返回值
            break;
        
        if location.x == dest.x and location.y == dest.y:
            break

        closedlist[location.getPos()] = location
        openlist.pop(location.getPos())
        addAdjacentPositions(map, location, dest, openlist, closedlist)

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

WIDTH = 10
HEIGHT = 10
BLOCK_NUM = 50
map = Map(WIDTH, HEIGHT)
#map.createBlock(BLOCK_NUM)
map.setBlock([[1,1],[0,0]])
#map.showMap()

source = map.generatePos((0,WIDTH//3),(0,HEIGHT//3))
dest = map.generatePos((WIDTH//2,WIDTH-1),(HEIGHT//2,HEIGHT-1))
print("source:", source)
print("dest:", dest)
path=AStarSearch(map, source, dest)
#map.showMap()
#path=get_path_location(map.map)
print(path)
map.showMap()
end=time.time()
print(end-start)


# In[2]:


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


# In[3]:


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


# In[5]:


def cross_map_search(file_dir,lib,cell,display):
    info=map_info(file_dir)#获取一个infolist
    width=info[0]
    height=info[1]
    layout_info=info[2]
    len_layout=len(layout_info)
    map_origin=info[3]
    
    layout_map_odd=Map(width,height)#奇map
    layout_map_even=Map(width,height)#偶map
    layout_map_nox=Map(width,height)#不允许cross
    layout_map_port=Map(width,height)#记录port位置
    
    map_list=[layout_map_odd,layout_map_even,layout_map_nox,layout_map_port] #所有map存在一个list里
    map_for_search_path_num = 3 #前三个map用于寻路
    
    def showMap_all(map_list):#显示所有map
        for k in range(0,map_for_search_path_num):
            map_list[k].showMap()

    for i in range(0,len_layout):
        block_point=origin_to_blockpoint_enlarged(layout_info[i].area,layout_info[i].xy,layout_info[i].orient)
        abs_point=get_abs_block_point(map_origin,block_point)
        for j in range(0,map_for_search_path_num):
            map_list[j].setBlock(abs_point)

        #开始寻路
    coord_info=info[4]

    connection_info=info[5]
    
    #print(coord_info)#提示一下要连线的路径

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
        for j in range(0,4):#所有map封上端口
            map_list[j].setBlock([block_source,block_dest])
    #print("--------------------blocking port-----------------------")    
    #showMap_all(map_list)

    for i in range(0,coord_len):#????coord怎么和layout def里面的不一样
        #print(coord_info[i])
        port_1_temp=port_coord_to_map(coord_info[i][0][0],coord_info[i][0][1])#获取第一个端口坐标 map中的
        port_1=[port_1_temp[0]-map_origin[0],port_1_temp[1]-map_origin[1]]#获取第一个端口的绝对坐标 map中的
        port_2_temp=port_coord_to_map(coord_info[i][1][0],coord_info[i][1][1])#同上
        port_2=[port_2_temp[0]-map_origin[0],port_2_temp[1]-map_origin[1]]#同上上
        source=(port_2[0],port_2[1])#获取出发点
        dest=(port_1[0],port_1[1])#获取终点

        for j in range(0,map_for_search_path_num):
            map_list[j].clrBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])#先清除掉要布线的这条路径的端口block，不然就找不到valid path
        #for j in range(0,map_for_search_path_num-1):
            #map_list[j].clr_port_area(port_1[0],port_1[1],coord_info[i][0][1])
            #map_list[j].clr_port_area(port_2[0],port_2[1],coord_info[i][1][1])

        #------------get regulator lenth-----------------
        max_port_reg_try=7#?
        min_port_reg_try=1#?
        x_delta=port_2[0]-port_1[0]
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
        #search path in map 3
        regulate_point_map3_1=regulate_route_new(port_1,coord_info[i][0][1],3)#regulate端口处，source
        regulate_point_map3_2=regulate_route_new(port_2,coord_info[i][1][1],3)#regulate端口处,dest
        prev_block_map3_1=map_list[2].get_blocked_point(regulate_point_map3_1)
        prev_block_map3_2=map_list[2].get_blocked_point(regulate_point_map3_2)
        prev_en_map3_1=map_list[2].get_cross_enable(regulate_point_map3_1)
        prev_en_map3_2=map_list[2].get_cross_enable(regulate_point_map3_2)
        map_list[2].setBlock(regulate_point_map3_1)
        map_list[2].setBlock(regulate_point_map3_2)
        path_map3=AStarSearch(map_list[2],source,dest)#A星算path
        if(len(path_map3)==0):
            map_list[2].clrBlock(regulate_point_map3_1)
            map_list[2].clrBlock(regulate_point_map3_2)
            map_list[2].setBlock(prev_block_map3_1)
            map_list[2].setBlock(prev_block_map3_2)
            map_list[2].setBlock_to2(prev_en_map3_1)
            map_list[2].setBlock_to2(prev_en_map3_2)
            map_list[2].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
            regulate_point_map3_1=regulate_route_new(port_1,coord_info[i][0][1],2)#regulate端口处，source
            regulate_point_map3_2=regulate_route_new(port_2,coord_info[i][1][1],2)#regulate端口处,dest
            prev_block_map3_1=map_list[2].get_blocked_point(regulate_point_map3_1)
            prev_block_map3_2=map_list[2].get_blocked_point(regulate_point_map3_2)
            prev_en_map3_1=map_list[2].get_cross_enable(regulate_point_map3_1)
            prev_en_map3_2=map_list[2].get_cross_enable(regulate_point_map3_2)
            map_list[2].setBlock(regulate_point_map3_1)
            map_list[2].setBlock(regulate_point_map3_2)
            path_map3=AStarSearch(map_list[2],source,dest)#A星算path
            if(len(path_map3)==0):
                path_len_map3=inf
            else:
                path_len_map3=len(path_map3)#记录当前path的长度
        else:
            path_len_map3=len(path_map3)#记录当前path的长度
        #--------------------------------------------------------------------------------------------

        for m in range(max_port_reg_try,min_port_reg_try,-1):#待处理
            print("iteration {0} at path {1}".format(max_port_reg_try-m+1,i+1))
            #print("loop start")
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
            for j in range(0,map_for_search_path_num-1):#每一个map都做regulator
                prev_block_1=map_list[j].get_blocked_point(regulate_point1)
                prev_block_2=map_list[j].get_blocked_point(regulate_point2)
                prev_en_1=map_list[j].get_cross_enable(regulate_point1)
                prev_en_2=map_list[j].get_cross_enable(regulate_point2)
                prev_reg_1=map_list[j].get_regulator_point(regulate_point1)
                prev_reg_2=map_list[j].get_regulator_point(regulate_point2)
                prev_1_source.append(prev_block_1)
                prev_1_dest.append(prev_block_2)
                prev_2_source.append(prev_en_1)
                prev_2_dest.append(prev_en_2)
                prev_5_source.append(prev_reg_1)
                prev_5_dest.append(prev_reg_2)
                map_list[j].setBlock(regulate_point1)
                map_list[j].setBlock(regulate_point2)
            #print("--------------------port regulator,path:{0}-----------------------".format(i))    
            #showMap_all(map_list)
            path=[]
            path_len=[]
            #showMap_all(map_list)
            #测试 1 2 3map是否有path，如果没有则恢复regulator并跳出
            for j in range(0,map_for_search_path_num-1):#3个map中查找对应的路径
                path_curr=AStarSearch(map_list[j],source,dest)#A星算path
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
            if(path_len[min_path_index]==inf and m==min_port_reg_try+1):
                print("No valid path")
                continue
            elif( path_len[0]>path_len_map3 and path_len[1]>path_len_map3 and m!=min_port_reg_try+1):
                for j in range(0,map_for_search_path_num-1):
                    prev_reg_1=map_list[j].get_regulator_point(regulate_point1)
                    prev_reg_2=map_list[j].get_regulator_point(regulate_point2)
                    prev_5_source2.append(prev_reg_1)
                    prev_5_dest2.append(prev_reg_2)
                    map_list[j].clrBlock(regulate_point1)
                    map_list[j].clrBlock(regulate_point2)
                    map_list[j].setBlock(prev_1_source[j])
                    map_list[j].setBlock(prev_1_dest[j])
                    map_list[j].setBlock_to2(prev_2_source[j])
                    map_list[j].setBlock_to2(prev_2_dest[j])
                    map_list[j].setValue_mul(prev_5_source[j],5)
                    map_list[j].setValue_mul(prev_5_dest[j],5)
                    map_list[j].setValue_mul(prev_5_source2[j],5)
                    map_list[j].setValue_mul(prev_5_dest2[j],5)
                    #map_list[j].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])
                print("failed, try again")
                #showMap_all(map_list)
                continue #调到for m循环，m-1后继续测试
            elif(path_len[min_path_index]>=min_port_reg_try and path_len[min_path_index]!=inf):#如果能直接找到路径则寻找最短 # minimal path len is ?
                map_list[0].setBlock_basic(min_path,m)
                map_list[1].setBlock_basic(min_path,m)
                map_list[2].setBlock(min_path)#第三个map设置为全屏蔽
                #print("--------------------show map,path:{0}-----------------------".format(i))    
                #showMap_all(map_list)
                for j in range(0,map_for_search_path_num-1):#清除port regulator
                    prev_reg_1=map_list[j].get_regulator_point(regulate_point1)
                    prev_reg_2=map_list[j].get_regulator_point(regulate_point2)
                    prev_5_source2.append(prev_reg_1)
                    prev_5_dest2.append(prev_reg_2)
                    map_list[j].clrBlock(regulate_point1)
                    map_list[j].clrBlock(regulate_point2)
                    map_list[j].setBlock(prev_1_source[j])
                    map_list[j].setBlock(prev_1_dest[j])
                    map_list[j].setBlock_to2(prev_2_source[j])
                    map_list[j].setBlock_to2(prev_2_dest[j])
                    map_list[j].setValue_mul(prev_5_source[j],5)
                    map_list[j].setValue_mul(prev_5_dest[j],5)
                    map_list[j].setValue_mul(prev_5_source2[j],5)
                    map_list[j].setValue_mul(prev_5_dest2[j],5)
                    map_list[j].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])

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

        #recover activity in map 3
        map_list[2].clrBlock(regulate_point_map3_1)
        map_list[2].clrBlock(regulate_point_map3_2)
        map_list[2].setBlock(prev_block_map3_1)
        map_list[2].setBlock(prev_block_map3_2)
        map_list[2].setBlock_to2(prev_en_map3_1)
        map_list[2].setBlock_to2(prev_en_map3_2)
        map_list[2].setBlock([[port_2[0],port_2[1]],[port_1[0],port_1[1]]])

        #get pcell path according to min_path

        temp=[coord_info[i][1],coord_info[i][0]]#只能用temp来重新排一下coord_info了
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
            index_seq=get_index_sequence(new_path,coord_info[i][1][1],last_check_index(coord_info[i][0][1])) 
            #print(index_seq)
            rtype_seq=get_route_type(index_seq)
            std_path_coord=[]
            for i in range(0,len_path-1):
                new_path[i]=[new_path[i][0]*layout_unit_len,new_path[i][1]*layout_unit_len]#以后换成layout_unit_len
                std_path_coord.append(new_path[i])
                new_path[i]=pcell_coord(new_path[i],index_seq[i])
            new_path[-1]=[new_path[-1][0]*layout_unit_len,new_path[-1][1]*layout_unit_len]
            std_path_coord.append(new_path[-1])
            new_path[-1]=pcell_coord(new_path[-1],last_check_index(index_seq[-1]))            
            info=analyze_path(new_path,return_path,index_seq,rtype_seq,std_path_coord)
            print("source:{0} to destination:{1}".format(new_path[0],new_path[-1]))
            script=path_to_pcell(info,new_path,index_seq)


        else:
            script=[]
            print("NO valid path from {0} to {1}".format(source,dest))
        #for s in script:
        #    print(s)
        '''script=path_to_inst(new_path,temp,0,connection_info[i][0]+'_'+connection_info[i][2],0)#输入path 获取dbcreate脚本'''
        len_script=len(script)
        for j in range(0,len_script):
            print(script[j],file=text)#将dbcreate脚本字符串写进text中输出



        #if(display==1):#显示函数，如果电路规模过大建议display置零
            #print("path:{0}".format(new_path))
            #layout_map.showMap()

    text.close()


# In[ ]:





# In[ ]:




