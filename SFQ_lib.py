#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
from Param_lib import *
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


# In[54]:


def interface(input_width,output_width,origin,rotate,layer):#interface的python模型 #origin为30*30方格的0,15处
    enlarge_coef=3
    path_width=output_width
    if(layer=="mp1"):
        output_width=output_width-1
        itface_width=(output_width-input_width)/2+enlarge_coef+0.5
    else:
        itface_width=(output_width-input_width)/2+enlarge_coef
    if(rotate==1):
        p1=[origin[0],origin[1]+input_width/2]
        p2=[origin[0]-(output_width-input_width)/2,origin[1]+output_width/2]
        p3=[p2[0]-enlarge_coef,p2[1]]
        p4=[p3[0],origin[1]-output_width/2]
        p5=[origin[0]-(output_width-input_width)/2,origin[1]-output_width/2]
        p6=[origin[0],origin[1]-input_width/2]
        path_1=[origin[0]-itface_width,origin[1]]
        path_2=[origin[0]-layout_unit_len,origin[1]]
    elif(rotate==2):
        p1=[origin[0]+input_width/2,origin[1]]
        p2=[origin[0]+output_width/2,origin[1]-(output_width-input_width)/2]
        p3=[p2[0],p2[1]-enlarge_coef]
        p4=[origin[0]-output_width/2,p3[1]]
        p5=[origin[0]-output_width/2,origin[1]-(output_width-input_width)/2]
        p6=[origin[0]-input_width/2,origin[1]]
        path_1=[origin[0],origin[1]-itface_width]
        path_2=[origin[0],origin[1]-layout_unit_len]
    elif(rotate==3):
        p1=[origin[0],origin[1]+input_width/2]
        p2=[origin[0]+(output_width-input_width)/2,origin[1]+output_width/2]
        p3=[p2[0]+enlarge_coef,p2[1]]
        p4=[p3[0],origin[1]-output_width/2]
        p5=[origin[0]+(output_width-input_width)/2,origin[1]-output_width/2]
        p6=[origin[0],origin[1]-input_width/2]
        path_1=[origin[0]+itface_width,origin[1]]
        path_2=[origin[0]+layout_unit_len,origin[1]]
    elif(rotate==4):
        p1=[origin[0]+input_width/2,origin[1]]
        p2=[origin[0]+output_width/2,origin[1]+(output_width-input_width)/2]
        p3=[p2[0],p2[1]+enlarge_coef]
        p4=[origin[0]-output_width/2,p3[1]]
        p5=[origin[0]-output_width/2,origin[1]+(output_width-input_width)/2]
        p6=[origin[0]-input_width/2,origin[1]]
        path_1=[origin[0],origin[1]+itface_width]
        path_2=[origin[0],origin[1]+layout_unit_len]
    if(layer=="mp1"):
        script='''
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list({12}:{13} {14}:{15}) ?width {16} ?justification "center" ?cvId  cellID)'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],path_1[0],path_1[1],path_2[0],path_2[1],path_width)
    elif(layer=="mn0"):
        script='''
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))
rodCreatePath(?layer "mn0" ?pts list({12}:{13} {14}:{15}) ?width {16} ?justification "center" ?cvId  cellID)'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],path_1[0],path_1[1],path_2[0],path_2[1],output_width)
    return script
#test=interface(4,18,[60,-34],4,"mn0")
#print(test)


# In[38]:


def corner(wire_width,corner_width,wire_type,origin,in_index,out_index,descend):#corner的python模型，descend为 13输入则向下，24输入则向左 #origin为30*30方格的0,15处
    tan675=2.414213562
    x=layout_unit_len/2-wire_width/(2*tan675)
    if(in_index==1):
        if(out_index==2):
            p1=[origin[0],origin[1]+wire_width/2]
            p2=[origin[0]-wire_width/tan675,origin[1]+wire_width/2]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]-wire_width/2]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
        elif(out_index==1):
            if(descend==1):
                p1=[origin[0],origin[1]+wire_width/2]
                p2=[origin[0]-wire_width/tan675-x,origin[1]+wire_width/2]
                p3=[origin[0]-corner_width*layout_unit_len+x,origin[1]-(corner_width-1)*layout_unit_len+wire_width/2]
                p4=[origin[0]-corner_width*layout_unit_len,origin[1]-(corner_width-1)*layout_unit_len+wire_width/2]                
                p5=[origin[0]-corner_width*layout_unit_len,origin[1]-(corner_width-1)*layout_unit_len-wire_width/2]
                p6=[origin[0]-corner_width*layout_unit_len+x+wire_width/tan675,origin[1]-(corner_width-1)*layout_unit_len-wire_width/2]
                p7=[origin[0]-x,origin[1]-wire_width/2]
                p8=[origin[0],origin[1]-wire_width/2]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0],origin[1]-wire_width/2]
                p2=[origin[0]-wire_width/tan675-x,origin[1]-wire_width/2]
                p3=[origin[0]-corner_width*layout_unit_len+x,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]
                p4=[origin[0]-corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]                
                p5=[origin[0]-corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p6=[origin[0]-corner_width*layout_unit_len+x+wire_width/tan675,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p7=[origin[0]-x,origin[1]+wire_width/2]
                p8=[origin[0],origin[1]+wire_width/2]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==4):
            p1=[origin[0],origin[1]-wire_width/2]
            p2=[origin[0]-wire_width/tan675,origin[1]-wire_width/2]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]+wire_width/2]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    elif(in_index==2):
        if(out_index==1):
            p1=[origin[0]+wire_width/2,origin[1]]
            p2=[origin[0]+wire_width/2,origin[1]-wire_width/tan675]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p6=[origin[0]-wire_width/2,origin[1]]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
        elif(out_index==2):
            if(descend==1):
                p1=[origin[0]+wire_width/2,origin[1]]
                p2=[origin[0]+wire_width/2,origin[1]-wire_width/tan675-x]
                p3=[origin[0]-(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len+x]
                p4=[origin[0]-(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len]                
                p5=[origin[0]-(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len]
                p6=[origin[0]-(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len+x+wire_width/tan675]
                p7=[origin[0]-wire_width/2,origin[1]-x]
                p8=[origin[0]-wire_width/2,origin[1]]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0]-wire_width/2,origin[1]]
                p2=[origin[0]-wire_width/2,origin[1]-wire_width/tan675-x]
                p3=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len+x]
                p4=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len]                
                p5=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len]
                p6=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len+x+wire_width/tan675]
                p7=[origin[0]+wire_width/2,origin[1]-x]
                p8=[origin[0]+wire_width/2,origin[1]]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==3):
            p1=[origin[0]-wire_width/2,origin[1]]
            p2=[origin[0]-wire_width/2,origin[1]-wire_width/tan675]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p6=[origin[0]+wire_width/2,origin[1]]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    elif(in_index==3):
        if(out_index==2):
            p1=[origin[0],origin[1]+wire_width/2]
            p2=[origin[0]+wire_width/tan675,origin[1]+wire_width/2]
            p3=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2+wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675]
            p4=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2+wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2-wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]-wire_width/2]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
        elif(out_index==3):
            if(descend==1):
                p1=[origin[0],origin[1]+wire_width/2]
                p2=[origin[0]+wire_width/tan675+x,origin[1]+wire_width/2]
                p3=[origin[0]+corner_width*layout_unit_len-x,origin[1]-(corner_width-1)*layout_unit_len+wire_width/2]
                p4=[origin[0]+corner_width*layout_unit_len,origin[1]-(corner_width-1)*layout_unit_len+wire_width/2]                
                p5=[origin[0]+corner_width*layout_unit_len,origin[1]-(corner_width-1)*layout_unit_len-wire_width/2]
                p6=[origin[0]+corner_width*layout_unit_len-x-wire_width/tan675,origin[1]-(corner_width-1)*layout_unit_len-wire_width/2]
                p7=[origin[0]+x,origin[1]-wire_width/2]
                p8=[origin[0],origin[1]-wire_width/2]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0],origin[1]-wire_width/2]
                p2=[origin[0]+wire_width/tan675+x,origin[1]-wire_width/2]
                p3=[origin[0]+corner_width*layout_unit_len-x,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]
                p4=[origin[0]+corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]                
                p5=[origin[0]+corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p6=[origin[0]+corner_width*layout_unit_len-x-wire_width/tan675,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p7=[origin[0]+x,origin[1]+wire_width/2]
                p8=[origin[0],origin[1]+wire_width/2]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==4):
            p1=[origin[0],origin[1]-wire_width/2]
            p2=[origin[0]+wire_width/tan675,origin[1]-wire_width/2]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]+wire_width/2]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)

    elif(in_index==4):
        if(out_index==1):
            p1=[origin[0]+wire_width/2,origin[1]]
            p2=[origin[0]+wire_width/2,origin[1]+wire_width/tan675]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p6=[origin[0]-wire_width/2,origin[1]]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
        elif(out_index==4):
            if(descend==1):
                p1=[origin[0]+wire_width/2,origin[1]]
                p2=[origin[0]+wire_width/2,origin[1]+wire_width/tan675+x]
                p3=[origin[0]-(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len-x]
                p4=[origin[0]-(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len]                
                p5=[origin[0]-(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len]
                p6=[origin[0]-(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len-x-wire_width/tan675]
                p7=[origin[0]-wire_width/2,origin[1]+x]
                p8=[origin[0]-wire_width/2,origin[1]]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0]-wire_width/2,origin[1]]
                p2=[origin[0]-wire_width/2,origin[1]+wire_width/tan675+x]
                p3=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len-x]
                p4=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len]                
                p5=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len]
                p6=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len-x-wire_width/tan675]
                p7=[origin[0]+wire_width/2,origin[1]+x]
                p8=[origin[0]+wire_width/2,origin[1]]
                script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==3):
            p1=[origin[0]-wire_width/2,origin[1]]
            p2=[origin[0]-wire_width/2,origin[1]+wire_width/tan675]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p6=[origin[0]+wire_width/2,origin[1]]
            script='''
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    return script
#test=corner(22,1,"mn0",[layout_unit_len/2,-90],1,1,0)
#print(test)


# In[24]:


def path(source,dest,width,wire_type):#普通线的模型 #origin为线的中心
    script='''
rodCreatePath(?layer "{0}" ?pts list({2}:{3} {4}:{5}) ?width {1} ?justification "center" ?cvId  cellID)'''.format(wire_type,width,source[0],source[1],dest[0],dest[1])
    return script
#test=path([90,90],[180,30],22,"mn0")
#print(test)


# In[32]:


def cross(width,origin,in_index,ctype):#cross的模型 #origin为30*30方格的0,15处
    if(in_index==1):
        center=[origin[0]-layout_unit_len/2,origin[1]]
    elif(in_index==2):
        center=[origin[0],origin[1]-layout_unit_len/2]
    elif(in_index==3):
        center=[origin[0]+layout_unit_len/2,origin[1]]
    elif(in_index==4):
        center=[origin[0],origin[1]+layout_unit_len/2]
    p1=[center[0]-width/2,center[1]-width/2]
    p2=[center[0]-width/2,center[1]+width/2]
    p3=[center[0]+width/2,center[1]+width/2]
    p4=[center[0]+width/2,center[1]-width/2]
    script='''
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7}))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -1)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 1)'''.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1])
    if(ctype==1):
        ad_path1=path([center[0]-layout_unit_len/2,center[1]],[center[0]-width/2-1,center[1]],width,"mp1")
        ad_path2=path([center[0]+width/2,center[1]],[center[0]+layout_unit_len/2,center[1]],width,"mn0")
    elif(ctype==2):
        ad_path1=path([center[0],center[1]-layout_unit_len/2],[center[0],center[1]-width/2-1],width,"mp1")
        ad_path2=path([center[0],center[1]+width/2],[center[0],center[1]+layout_unit_len/2],width,"mn0")
    elif(ctype==3):
        ad_path1=path([center[0]+width/2+1,center[1]],[center[0]+layout_unit_len/2,center[1]],width,"mp1")
        ad_path2=path([center[0]-layout_unit_len/2,center[1]],[center[0]-width/2,center[1]],width,"mn0")
    elif(ctype==4):
        ad_path1=path([center[0],center[1]+width/2+1],[center[0],center[1]+layout_unit_len/2],width,"mp1")
        ad_path2=path([center[0],center[1]-layout_unit_len/2],[center[0],center[1]-width/2],width,"mn0")
    return script+ad_path1+ad_path2
#test=cross(22,[110,10],2,3)
#print(test)


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


# In[ ]:


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

