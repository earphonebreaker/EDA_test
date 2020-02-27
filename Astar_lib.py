#!/usr/bin/env python
# coding: utf-8

# In[1]:


#2020/2/27 杨树澄
#优化好的A star算法库


# In[2]:


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
        map.map[location.y][location.x] = 2
        #print(location.x,location.y)
        path_temp.append([location.x,location.y])
        location = location.pre_entry
    path=path_temp[::-1]
    return path


# In[2]:


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




