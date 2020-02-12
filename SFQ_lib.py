#!/usr/bin/env python
# coding: utf-8

# In[16]:


#class类型的单元库
#2020/2/8 杨树澄
#目前包含面积，实例名，端口信息等
#注：端口位置（port_type）统一按照初始化给出的port顺序做映射
#注：面积为[a,b]->a*b,其中a为x方向长度，b为y方向长度
#q2d和d2q暂时缺省，目测只会有一种版本
#pad和aux也暂时缺省（fbias）


# In[21]:


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
        if(port_type=="13"):
            self.port_type=[1,3]
        elif(port_type=="14"):
            self.port_type=[1,4]
        else:
            raise Exception("Undefined layout")


# In[24]:


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


# In[25]:


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


# In[26]:


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


# In[62]:


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


# In[29]:


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
        if(port_type=="135"):
            self.port_type=[1,3,5]
        elif(port_type=="514"):
            self.port_type=[5,1,4]
        else:
            raise Exception("Undefined layout")


# In[31]:


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


# In[32]:


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


# In[33]:


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
        if(port_type=="2345"):
            self.port_type=[2,3,4,5]
        elif(port_type=="2543"):
            self.port_type=[2,5,4,3]
        else:
            raise Exception("Undefined layout")


# In[34]:


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
        if(port_type=="18673"):
            self.port_type=[1,8,6,7,3]
        else:
            raise Exception("Undefined layout")


# In[35]:


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
        if(port_type=="1238"):
            self.port_type=[1,2,3,8]
        elif(port_type=="1238"):
            self.port_type=[1,2,4,8]
        elif(port_type=="1278"):
            self.port_type=[1,2,7,8]
        else:
            raise Exception("Undefined layout")


# In[36]:


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


# In[37]:


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


# In[38]:


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
        if(port_type=="420169"):
            self.port_type=[4,20,16,9]
        else:
            raise Exception("Undefined layout")


# In[39]:


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
        if(port_type=="1826"):
            self.port_type=[1,8,2,6]
        elif(port_type=="1836"):
            self.port_type=[1,8,3,6]
        elif(port_type=="10826"):
            self.port_type=[10,8,2,6]
        else:
            raise Exception("Undefined layout")


# In[72]:


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
    else:
        raise Exception("No module matched")
    return model


# In[1]:


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




