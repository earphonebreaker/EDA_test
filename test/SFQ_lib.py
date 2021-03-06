﻿#!/usr/bin/env python
# coding: utf-8

# In[3]:


#class类型的单元库
#2020/2/8 杨树澄
#目前包含面积，实例名，端口信息，跟库有关的函数等
#注：端口位置（port_type）统一按照初始化给出的port顺序做映射
#注：面积为[a,b]->a*b,其中a为x方向长度，b为y方向长度
#q2d和d2q暂时缺省，目测只会有一种版本
#pad和aux也暂时缺省（fbias）
#2020/2/18 添加类的orient和origin（xy）参数，新增moat的模型
#后添加的统一端口序列：'AI', 'TI', 'BI', 'SI', 'RI','RESET', 'AO', 'TO', 'BO' ,'CO', 'ABO', 'AOA', 'AOB', 'AOC'
import re
def port_sequence():
    return ['AI', 'TI', 'BI', 'SI', 'RI','RESET', 'AO', 'TO', 'BO' ,'CO', 'ABO', 'AOA', 'AOB', 'AOC']


# In[4]:


class jtl1j_a:#端口位置顺序为AI，AO
    area=[1,1]
    def __init__ (self,instname,portAI,wireAI,portAO,wireAO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAO=portAO
        self.wireAO=wireAO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="13"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="13"):
            self.port_type=[1,3]
        elif(port_type=="14"):
            self.port_type=[1,4]
        else:
            raise Exception("Undefined layout")


# In[5]:


#c=jtl1j_a("inst1",'AI','AO','net1','net2',port_type='14',xy=[330,320])
#c.xy=[120,320]
#c.xy


# In[6]:


class jtl2j_a:#端口位置顺序为AI，AO
    area=[2,1]
    def __init__ (self,instname,portAI,wireAI,portAO,wireAO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAO=portAO
        self.wireAO=wireAO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="12"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="12"):
            self.port_type=[1,2]
        elif(port_type=="14"):
            self.port_type=[1,4]
        elif(port_type=="15"):
            self.port_type=[1,5]
        elif(port_type=="25"):
            self.port_type=[2,5]
        elif(port_type=="56"):
            self.port_type=[5,6]
        elif(port_type=="21"):
            self.port_type=[2,1]
        elif(port_type=="51"):
            self.port_type=[5,1]
        elif(port_type=="52"):
            self.port_type=[5,2]
        elif(port_type=="65"):
            self.port_type=[6,5]
        else:
            raise Exception("Undefined layout")


# In[7]:


class jtl3j_a:#端口位置顺序为AI，AO
    area=[3,1]
    def __init__ (self,instname,portAI,wireAI,portAO,wireAO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAO=portAO
        self.wireAO=wireAO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="15"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="15"):
            self.port_type=[1,5]
        elif(port_type=="26"):
            self.port_type=[2,6]
        elif(port_type=="58"):
            self.port_type=[5,8]
        elif(port_type=="62"):
            self.port_type=[6,2]
        elif(port_type=="85"):
            self.port_type=[8,5]
        else:
            raise Exception("Undefined layout")


# In[8]:


class jtl4j_a:#端口位置顺序为AI，AO,单元面积（形状）和端口位置关联
    def __init__ (self,instname,portAI,wireAI,portAO,wireAO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAO=portAO
        self.wireAO=wireAO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="12"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="12"):
            self.port_type=[1,2]
            self.area=[2,2]
        elif(port_type=="13"):
            self.port_type=[1,3]
            self.area=[2,2]
        elif(port_type=="31"):
            self.port_type=[3,1]
            self.area=[2,2]
        elif(port_type=="15"):
            self.port_type=[1,5]
            self.area=[3,1]
        else:
            raise Exception("Undefined layout")


# In[9]:


class jtl_crs22:#端口位置顺序为AI，BI,AO,BO
    area=[2,2]
    def __init__ (self,instname,portAI,wireAI,portBI,wireBI,portAO,wireAO,portBO,wireBO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAO=portAO
        self.wireAO=wireAO
        self.portBI=portBI
        self.wireBI=wireBI
        self.portBO=portBO
        self.wireBO=wireBO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="2358"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="2358"):
            self.port_type=[2,3,5,8]
        elif(port_type=="2853"):
            self.port_type=[2,8,5,3]
        elif(port_type=="5328"):
            self.port_type=[5,3,2,8]
        elif(port_type=="5823"):
            self.port_type=[5,8,2,3]
        elif(port_type=="2153"):
            self.port_type=[2,1,5,3]
        elif(port_type=="5123"):
            self.port_type=[5,1,2,3]
        elif(port_type=="2351"):
            self.port_type=[2,3,5,1]
        elif(port_type=="5321"):
            self.port_type=[5,3,2,1]
        else:
            raise Exception("Undefined layout")


# In[10]:


class s1j2o_c:#端口位置顺序为AI，AOA,AOB
    area=[2,1]
    def __init__ (self,instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAOA=portAOA
        self.wireAOA=wireAOA
        self.portAOB=portAOB
        self.wireAOB=wireAOB
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="135"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="135"):
            self.port_type=[1,3,5]
        elif(port_type=="514"):
            self.port_type=[5,1,4]
        else:
            raise Exception("Undefined layout")


# In[11]:


class s2j2o_b:#端口位置顺序为AI，AOA,AOB
    area=[2,1]
    def __init__ (self,instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAOA=portAOA
        self.wireAOA=wireAOA
        self.portAOB=portAOB
        self.wireAOB=wireAOB
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="135"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="135"):
            self.port_type=[1,3,5]
        elif(port_type=="134"):
            self.port_type=[1,4,5]
        elif(port_type=="234"):
            self.port_type=[2,3,4]
        elif(port_type=="235"):
            self.port_type=[2,3,5]
        elif(port_type=="245"):
            self.port_type=[2,4,5]
        else:
            raise Exception("Undefined layout")


# In[12]:


class s2j3o_a:#端口位置顺序为AI，AOA,AOB,AOC
    area=[2,1]
    def __init__ (self,instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,portAOC,wireAOC,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAOA=portAOA
        self.wireAOA=wireAOA
        self.portAOB=portAOB
        self.wireAOB=wireAOB
        self.portAOC=portAOC
        self.wireAOC=wireAOC
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="1234"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="1234"):
            self.port_type=[1,2,3,4]
        elif(port_type=="1235"):
            self.port_type=[1,2,3,5]
        elif(port_type=="1245"):
            self.port_type=[1,2,4,5]
        elif(port_type=="6134"):
            self.port_type=[6,1,3,4]
        elif(port_type=="6135"):
            self.port_type=[6,1,3,5]
        elif(port_type=="6145"):
            self.port_type=[6,1,4,5]
        elif(port_type=="6234"):
            self.port_type=[6,2,3,4]
        elif(port_type=="6235"):
            self.port_type=[6,2,3,5]
        elif(port_type=="6245"):
            self.port_type=[6,2,4,5]
        else:
            raise Exception("Undefined layout")


# In[13]:


class s2j3o_c:#端口位置顺序为AI，AOA,AOB,AOC
    area=[2,1]
    def __init__ (self,instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,portAOC,wireAOC,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portAOA=portAOA
        self.wireAOA=wireAOA
        self.portAOB=portAOB
        self.wireAOB=wireAOB
        self.portAOC=portAOC
        self.wireAOC=wireAOC
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="2345"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="2345"):
            self.port_type=[2,3,4,5]
        elif(port_type=="2543"):
            self.port_type=[2,5,4,3]
        else:
            raise Exception("Undefined layout")


# In[14]:


class spl_jtl2j:#端口位置顺序为AI，AOA,AOB,AOC
    area=[2,2]
    def __init__ (self,instname,portAI,wireAI,portBI,wireBI,portAOA,wireAOA,portAOB,wireAOB,portBO,wireBO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portBI=portBI
        self.wireBI=wireBI
        self.portAOA=portAOA
        self.wireAOA=wireAOA
        self.portAOB=portAOB
        self.wireAOB=wireAOB
        self.portBO=portBO
        self.wireBO=wireBO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="18673"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="18673"):
            self.port_type=[1,8,6,7,3]
        else:
            raise Exception("Undefined layout")


# In[15]:


class and_e:#端口位置顺序为AI,TI,BI,ABO
    area=[3,3]
    def __init__ (self,instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portABO,wireABO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portBI=portBI
        self.wireBI=wireBI
        self.portTI=portTI
        self.wireTI=wireTI
        self.portABO=portABO
        self.wireABO=wireABO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="1238"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="1238"):
            self.port_type=[1,2,3,8]
        elif(port_type=="1238"):
            self.port_type=[1,2,4,8]
        elif(port_type=="1278"):
            self.port_type=[1,2,7,8]
        else:
            raise Exception("Undefined layout")


# In[16]:


class cb_a:#端口位置顺序为AI,BI,ABO
    area=[2,2]
    def __init__ (self,instname,portAI,wireAI,portBI,wireBI,portABO,wireABO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portBI=portBI
        self.wireBI=wireBI
        self.portABO=portABO
        self.wireABO=wireABO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="124"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="124"):
            self.port_type=[1,2,4]
        elif(port_type=="125"):
            self.port_type=[1,2,5]
        elif(port_type=="135"):
            self.port_type=[1,3,5]
        elif(port_type=="136"):
            self.port_type=[1,3,6]
        elif(port_type=="835"):
            self.port_type=[8,3,5]
        else:
            raise Exception("Undefined layout")


# In[17]:


class d22_a:#端口位置顺序为AI,TI,TO
    area=[2,2]
    def __init__ (self,instname,portAI,wireAI,portTI,wireTI,portTO,wireTO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portTI=portTI
        self.wireTI=wireTI
        self.portTO=portTO
        self.wireTO=wireTO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="135"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="146"):
            self.port_type=[1,4,6]
        elif(port_type=="175"):
            self.port_type=[1,7,5]
        elif(port_type=="135"):
            self.port_type=[1,3,5]
        elif(port_type=="375"):
            self.port_type=[3,7,5]
        elif(port_type=="386"):
            self.port_type=[3,8,6]
        elif(port_type=="316"):
            self.port_type=[3,1,6]
        else:
            raise Exception("Undefined layout")


# In[18]:


class jandf_a:#端口位置顺序为AI,TI,BI,ABO
    area=[5,5]
    def __init__ (self,instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portABO,wireABO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portBI=portBI
        self.wireBI=wireBI
        self.portTI=portTI
        self.wireTI=wireTI
        self.portABO=portABO
        self.wireABO=wireABO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="420169"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="420169"):
            self.port_type=[4,20,16,9]
        else:
            raise Exception("Undefined layout")


# In[19]:


class xor_b:#端口位置顺序为AI,TI,BI,TO
    area=[3,2]
    def __init__ (self,instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portTO,wireTO,**kwargs):
        self.instname=instname
        self.portAI=portAI
        self.wireAI=wireAI
        self.portBI=portBI
        self.wireBI=wireBI
        self.portTI=portTI
        self.wireTI=wireTI
        self.portTO=portTO
        self.wireTO=wireTO
        if 'port_type' in kwargs:
            port_type=kwargs['port_type']
        else:
            port_type="1826"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="1826"):
            self.port_type=[1,8,2,6]
        elif(port_type=="1836"):
            self.port_type=[1,8,3,6]
        elif(port_type=="10826"):
            self.port_type=[10,8,2,6]
        else:
            raise Exception("Undefined layout")


# In[20]:


class moat:#没有端口的moat
    area=[1,1]
    def __init__ (self,instname,**kwargs):
        self.instname=instname
        if 'reserved_info' in kwargs:
            self.reserved_info=kwargs['reserved_info']
        else:
            self.reserved_info="reserved"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]


# In[21]:


def read_instance(info):
    modulename=info[0]#获取module名
    instname=info[1]#获取inst名
    if(modulename=='jtl1j_a'):
        portAI='AI'
        portAO='AO'
        wireAI=info[3][info[2].index('AI')]#查找端口对应连线
        wireAO=info[3][info[2].index('AO')]
        model=jtl1j_a(instname,portAI,wireAI,portAO,wireAO)#返回一个模型（class，端口类型缺省）
    elif(modulename=='jtl2j_a'):
        portAI='AI'
        portAO='AO'
        wireAI=info[3][info[2].index('AI')]
        wireAO=info[3][info[2].index('AO')]
        model=jtl2j_a(instname,portAI,wireAI,portAO,wireAO)
    elif(modulename=='jtl3j_a'):
        portAI='AI'
        portAO='AO'
        wireAI=info[3][info[2].index('AI')]
        wireAO=info[3][info[2].index('AO')]
        model=jtl3j_a(instname,portAI,wireAI,portAO,wireAO)
    elif(modulename=='jtl4j_a'):
        portAI='AI'
        portAO='AO'
        wireAI=info[3][info[2].index('AI')]
        wireAO=info[3][info[2].index('AO')]
        model=jtl4j_a(instname,portAI,wireAI,portAO,wireAO)
    elif(modulename=='jtl_crs22'):
        portAI='AI'
        portAO='AO'
        portBI='BI'
        portBO='BO'
        wireAI=info[3][info[2].index('AI')]
        wireAO=info[3][info[2].index('AO')]
        wireBI=info[3][info[2].index('BI')]
        wireBO=info[3][info[2].index('BO')]
        model=jtl_crs22(instname,portAI,wireAI,portBI,wireBI,portAO,wireAO,portBO,wireBO)
    elif(modulename=='s1j2o_c'):
        portAI='AI'
        portAOA='AOA'
        portAOB='AOB'
        wireAI=info[3][info[2].index('AI')]
        wireAOA=info[3][info[2].index('AOA')]
        wireAOB=info[3][info[2].index('AOB')]
        model=s1j2o_c(instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB)
    elif(modulename=='s2j2o_b'):
        portAI='AI'
        portAOA='AOA'
        portAOB='AOB'
        wireAI=info[3][info[2].index('AI')]
        wireAOA=info[3][info[2].index('AOA')]
        wireAOB=info[3][info[2].index('AOB')]
        model=s2j2o_b(instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB)
    elif(modulename=='s2j3o_a'):
        portAI='AI'
        portAOA='AOA'
        portAOB='AOB'
        portAOC='AOC'
        wireAI=info[3][info[2].index('AI')]
        wireAOA=info[3][info[2].index('AOA')]
        wireAOB=info[3][info[2].index('AOB')]
        wireAOC=info[3][info[2].index('AOC')]
        model=s2j3o_a(instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,portAOC,wireAOC)
    elif(modulename=='s2j3o_c'):
        portAI='AI'
        portAOA='AOA'
        portAOB='AOB'
        portAOC='AOC'
        wireAI=info[3][info[2].index('AI')]
        wireAOA=info[3][info[2].index('AOA')]
        wireAOB=info[3][info[2].index('AOB')]
        wireAOC=info[3][info[2].index('AOC')]
        model=s2j3o_c(instname,portAI,wireAI,portAOA,wireAOA,portAOB,wireAOB,portAOC,wireAOC)
    elif(modulename=='spl_jtl2j'):
        portAI='AI'
        portAOA='AOA'
        portAOB='AOB'
        portBI='BI'
        portBO='BO'
        wireAI=info[3][info[2].index('AI')]
        wireBO=info[3][info[2].index('BO')]
        wireBI=info[3][info[2].index('BI')]
        wireAOA=info[3][info[2].index('AOA')]
        wireAOB=info[3][info[2].index('AOB')]
        model=spl_jtl2j(instname,portAI,wireAI,portBI,wireBI,portAOA,wireAOA,portAOB,wireAOB,portBO,wireBO)  
    elif(modulename=='and_e'):
        portAI='AI'
        portTI='TI'
        portBI='BI'
        portABO='ABO'
        wireAI=info[3][info[2].index('AI')]
        wireTI=info[3][info[2].index('TI')]
        wireBI=info[3][info[2].index('BI')]
        wireABO=info[3][info[2].index('ABO')]
        model=and_e(instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portABO,wireABO)
    elif(modulename=='cb_a'):
        portAI='AI'
        portBI='BI'
        portABO='ABO'
        wireAI=info[3][info[2].index('AI')]
        wireBI=info[3][info[2].index('BI')]
        wireABO=info[3][info[2].index('ABO')]
        model=cb_a(instname,portAI,wireAI,portBI,wireBI,portABO,wireABO)
    elif(modulename=='d22_a'):
        portAI='AI'
        portTI='TI'
        portTO='TO'
        wireAI=info[3][info[2].index('AI')]
        wireTI=info[3][info[2].index('TI')]
        wireTO=info[3][info[2].index('TO')]
        model=d22_a(instname,portAI,wireAI,portTI,wireTI,portTO,wireTO)
    elif(modulename=='jandf_a'):
        portAI='AI'
        portTI='TI'
        portBI='BI'
        portABO='ABO'
        wireAI=info[3][info[2].index('AI')]
        wireTI=info[3][info[2].index('TI')]
        wireBI=info[3][info[2].index('BI')]
        wireABO=info[3][info[2].index('ABO')]
        model=jandf_a(instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portABO,wireABO)
    elif(modulename=='xor_b'):
        portAI='AI'
        portTI='TI'
        portBI='BI'
        portTO='TO'
        wireAI=info[3][info[2].index('AI')]
        wireTI=info[3][info[2].index('TI')]
        wireBI=info[3][info[2].index('BI')]
        wireTO=info[3][info[2].index('TO')]
        model=xor_b(instname,portAI,wireAI,portTI,wireTI,portBI,wireBI,portTO,wireTO)
    elif(modulename=='moat'):
        model=moat(instname)
    else:
        raise Exception("No module matched")
    return model


# In[22]:


def process_port(string):#顺序出自上面的SFQlib规定 主要用来把版图截取的端口信息按照顺序重新规划并输出端口名和版图类型
    port_seq=port_sequence()
    num_list = re.findall('\d+', string)
    string=string.upper()
    port_index=[]
    port_name=[]
    for i in num_list:
        index=string.find(i)
        port_name.append(string[:index])
        port_index.append(string[index])
        string=string[index+1:]        
    #print(port_index)
    #print(port_name)
    port_index_arranged=[]
    port_name_arranged=[]
    for k in port_seq:
        if k in port_name:
            index_1=port_name.index(k)
            port_index_arranged.append(port_index[index_1])
            port_name_arranged.append(port_name[index_1])
        else:
            continue
    #print(port_index_arranged)
    #print(port_name_arranged)
    port_type=[]
    for i in port_index_arranged:
        port_type.append(int(i))
    return [port_name_arranged,port_type]
#process_port("ai1bi3to6ti8")
def layout_to_model(module_name,inst_name):#读取layout读出的module名和对应的inst名，获得一个来自SFQlib的model
    global port_info
    if(module_name=="moat_1x1"):
        module_name_cut="moat"
    else:
        index_1=module_name.find("_")
        #print(index_1)
        index_2=module_name[index_1+1:].find("_")
        #print(module_name[index_1+1:])
        #print(index_2)
        module_name_cut=module_name[:index_1+index_2+1]
        index_3=module_name.rfind("_")
        port_info=module_name[index_3+1:]
    port_info_processed=process_port(port_info)
    info_combined=[module_name_cut,inst_name,port_info_processed[0],port_info_processed[0]]
    layout_model=read_instance(info_combined)#read_instance函数来自SFQlib，和netlist reader同理，wire用版图端口名代替，并在此设置版图类型
    layout_model.port_type=port_info_processed[1]
    #print(port_info_processed[1])
    #print(layout_model.port_type)
    return layout_model
    
#k=info_to_model(t[0][0],t[4][0])


# In[23]:


def port_rearrangement(SFQmodel):#返回一个根据标准来的wire排序
    model_dir=dir(SFQmodel)
    len_dir=len(model_dir)
    seq_port=port_sequence()
    len_seq=len(seq_port)
    wire_name=[]
    for i in range(0,len_seq):
        if "wire"+seq_port[i] in model_dir:
            wire_name.append("wire"+seq_port[i])
    return wire_name


# In[24]:


def port_direction(port_name):#判断端口是什么类型的
    input_port=['AI', 'TI', 'BI', 'SI', 'RI','RESET']
    output_port=['AO', 'TO', 'BO' ,'CO', 'ABO', 'AOA', 'AOB', 'AOC']
    port_name=port_name.replace("wire","")
    if port_name in input_port:
        isOutput=False
    else:
        isOutput=True
    return isOutput


# In[25]:


def port_location(number,area):#根据端口位置序号和面积类型来判断端口与原点的相对位置
    x_index=area[0]
    y_index=area[1]
    if( number<=y_index ):
        relative_coord=[0,(y_index-number)*30+15]
        index=1
    elif( number>y_index and number<=(x_index+y_index)):
        relative_coord=[(number-y_index-1)*30+15,0]
        index=2
    elif( number>(x_index+y_index) and number<=(2*y_index+x_index)):
        relative_coord=[x_index*30,(number-x_index-y_index-1)*30+15]
        index=3
    elif( number>(2*y_index+x_index) and number<=(2*(x_index+y_index)) ): 
        relative_coord=[(2*(x_index+y_index)-number)*30+15,y_index*30]
        index=4
    else:
        raise Error("Undefined port location")
    return [relative_coord,index]

#测试模块
#area=[3,2]
#for i in range(1,2*(area[0]+area[1])+1):
#    print("端口序号为{0}".format(i))
#    test=port_location(i,area)
#    print(test)


# In[26]:


def port_coord_to_map(coord,index):#绘制地图时端口坐标转回左下点
    if(index==1):
        new_coord=[int(coord[0]/30-1),int((coord[1]-15)/30)]
    elif(index==2):
        new_coord=[int((coord[0]-15)/30),int((coord[1]-30)/30)]
    elif(index==3):
        new_coord=[int((coord[0])/30),int((coord[1]-15)/30)]
    elif(index==4):
        new_coord=[int((coord[0]-15)/30),int((coord[1])/30)]
    return new_coord


# In[27]:


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
#测试代码
#orient_list=["R0","R90","R180","R270","MX","MY","MXR90","MYR90"]
#origin=[360,330]
#relative_coord=[45, 60]#版图面积为2*2，端口位置7
#for i in orient_list:
#    print("当前版图方向为{0}".format(i))
#    test=get_abs_coord(i,origin,relative_coord)
#    print(test)


# In[28]:


#测试代码
c='''print("test for jtl")    
info=['jtl4j_a', 'I39', ['AO', 'AI'], ['net05', 'CI']]
c=read_instance(info)
print("area:{0}".format(c.area))
print("instname:{0}".format(c.instname))
print(c.portAI)
print(c.wireAI)
print(c.portAO)
print(c.wireAO)
#print(c.portAI)
#print(c.wireAI)
print(c.port_type)

info=['jtl_crs22', 'I76', ['BO', 'AO', 'BI', 'AI'], ['net070', 'net0105', 'net088', 'net087']]
c=read_instance(info)
print("test for jtl_crs")    
print("area:{0}".format(c.area))
print("instname:{0}".format(c.instname))
print(c.area)
print(c.instname)
print(c.portAI)
print(c.wireAI)
print(c.portAO)
print(c.wireAO)
#print(c.portAI)
#print(c.wireAI)
print(c.port_type)
info=['s2j2o_b', 'I53', ['AOA', 'AOB', 'AI'], ['net099', 'net0104', 'net8']]
c=read_instance(info)
print("test for spl")    
print("area:{0}".format(c.area))
print("instname:{0}".format(c.instname))
print(c.area)
print(c.instname)
print(c.portAI)
print(c.wireAI)
print(c.portAOA)
print(c.wireAOA)
print(c.portAOB)
print(c.wireAOB)
print(c.port_type)'''
#c=['jandf_a', 'jandfa0', ['BI', 'ABO', 'TI', 'AI'], ['net010', 'net011', 'net012', 'net013']]
#print(read_instance(c))


# In[ ]:




