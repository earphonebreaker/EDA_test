#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 09:54:18 2020

@author: yangshucheng

for generate SFQ_lib.py from target path
"""

import re

def port_sequence():
    return ['AI', 'TI','TIA','TIB', 'BI','CI','SI', 'RI','TNRI','RESET', \
            'AO','TO','TOA','TOB','TOC', 'BO' ,'TNRO','CO', 'ABO', 'AOA', \
            'AOB', 'AOC', 'OA', 'OB', 'OC','OUT']

target_lib={'/home/SIMIT/wangmingliang/Cadence/lib/lib_Nb03/wml03_lib':['TEST_PASS']}
aux_lib='rj03_lib'
aux_cell='fbias_1x1_a'
celllist={}
for t in target_lib.keys():
    for cat in target_lib[t]:
        with open(t+'/'+cat+'.Cat','r') as f:
            temp_list=f.readlines()
            for i in range(2,len(temp_list)):
                lib_cell=temp_list[i].replace(" type=\"cell\"\n","")
                cell=lib_cell.split("/")[1]
                if(cell[-1]=="c"):
                    continue
                elif(re.search(r'^[A-Za-z0-9]*_[A-Za-z0-9]*_[0-9]x[0-9]_[A-Za-z0-9]*$',cell) or \
                     re.search(r'^[A-Za-z0-9]*_[0-9]x[0-9]_[A-Za-z0-9]*$',cell)):
                    area=re.search(r'[0-9]x[0-9]',cell).group(0)
                    #print(area)
                    index=cell.index(area)
                    cellname=cell[:index-1]
                    cellport=cell[index:]
                    if(cellname not in celllist.keys()):
                        celllist.update({cellname:[cellport]})
                    else:
                        celllist[cellname].append(cellport)

def class_gen(cellname,cellport):
    port_string=re.search(r'_[A-Za-z0-9]*',cellport[0]).group()[1:]
    area_1st_str=re.search(r'^[0-9]x[0-9]',cellport[0]).group().split("x")
    area_1st=[int(area_1st_str[0]),int(area_1st_str[1])]
    [port_list,port_seq]=process_port(port_string)
    port_seq_str="".join(str(x) for x in port_seq)
    port_seq_int=[int(x) for x in port_seq]
    script_sum=""
    script1='''class {0}:#端口位置顺序为{1}
    def __init__ (self,instname,'''.format(cellname,port_list)
    script_sum=script_sum+script1
    for port in port_list:
        script_sum=script_sum+"port{0},wire{0},".format(port)
    script_sum=script_sum+'''**kwargs):
        self.instname=instname'''
    for port in port_list:
        script_sum=script_sum+'''
        self.port{}=port{}
        self.wire{}=wire{}'''.format(port,port,port,port)
    script_sum=script_sum+'''
        if 'port_type' in kwargs:
                port_type=kwargs['port_type']
        else:
                port_type="{0}"
        if 'orient' in kwargs:
            self.orient=kwargs['orient']
        else:
            self.orient="R0"
        if 'xy' in kwargs:
            self.xy=kwargs['xy']
        else:
            self.xy=[0,0]
        if(port_type=="{1}"):
            self.port_type={2}
            self.area={3}'''.format(port_seq_str,port_seq_str,port_seq_int,area_1st)
    layout_type=[[port_list,port_seq_int,area_1st]]
    for c in range(1,len(cellport)):
        p_string=re.search(r'_[A-Za-z0-9]*',cellport[c]).group()[1:]
        [p_list,p_seq]=process_port(p_string)
        area_string=re.search(r'^[0-9]x[0-9]',cellport[c]).group().split("x")
        area=[int(area_string[0]),int(area_string[1])]
        p_seq_str="".join(str(x) for x in p_seq)
        p_seq_int=[int(x) for x in p_seq]
        script_sum=script_sum+'''
        elif(port_type=="{0}"):
            self.port_type={1}
            self.area={2}'''.format(p_seq_str,p_seq_int,area)
        layout_type.append([p_list,p_seq_int,area])
    script_sum=script_sum+'''
        else:
            raise Exception("Undefined layout-{2}")
    def read_type(self):
        type_num={0}
        #format:[port_name,port_sequence,area]
        layout_type={1}
        return [type_num,layout_type]
    '''.format(len(layout_type),layout_type,cellname)
    
    return script_sum

def read_instance_gen(celllist):
    script_sum='''def read_instance(info):
    modulename=info[0]#获取module名
    instname=info[1]#获取inst名'''
    cell_name_list=[x for x in celllist.keys()]
    #print(cell_name_list)
    for c in range(len(cell_name_list)):
        if(c==0):
            script_sum=script_sum+'''
    if(modulename=='{0}'):'''.format(cell_name_list[c])
        else:
            script_sum=script_sum+'''
    elif(modulename=='{0}'):'''.format(cell_name_list[c])
        cellport=celllist[cell_name_list[c]][0]
        port=re.search(r'_[A_Za-z0-9]*$',cellport).group()[1:]
        [p_list,p_seq]=process_port(port)
        init_str=''
        for p in p_list:
            script_sum=script_sum+'''
        port{0}='{1}'
        wire{2}=info[3][info[2].index('{3}')]'''.format(p,p,p,p)
            init_str=init_str+"port{0},wire{1},".format(p,p)
        init_str=init_str[:-1]
        script_sum=script_sum+'''
        model={0}(instname,{1})'''.format(cell_name_list[c],init_str)
    script_sum=script_sum+'''
    else:
        raise Exception("No module matched-{0}".format(modulename))
    return model'''
    return(script_sum)


        
        

test=class_gen("ndroc_ip1",celllist['ndroc_ip1'])
test2=read_instance_gen(celllist)

def process_port(string):#顺序出自上面的SFQlib规定 主要用来把版图截取的端口信息按照顺序重新规划并输出端口名和版图类型
    port_seq=port_sequence()
    string=string.upper()
    num_list = re.findall('\d+', string)
    name_list=re.findall(r'[A-Za-z]+',string)
    len_num=len(num_list)
    port_name_arranged=[]
    port_type=[]
    for s in port_seq:
        if(s in name_list):
            index=name_list.index(s)
            port_type.append(num_list[index])
            port_name_arranged.append(s)
    return [port_name_arranged,port_type]
#process_port("ai1bi3to62ti8")
other_script='''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
automatically generated from script
stores layout-relevant data and functions, including SFQ cell-lib\PTL-Pcell.
"""
import re
from Param_lib import *
def port_sequence():
    return {0}'''.format(port_sequence())
other_script2='''
def process_port(string):#顺序出自上面的SFQlib规定 主要用来把版图截取的端口信息按照顺序重新规划并输出端口名和版图类型
    port_seq=port_sequence()
    string=string.upper()
    num_list = re.findall('\d+', string)
    name_list=re.findall(r'[A-Za-z]+',string)
    len_num=len(num_list)
    port_name_arranged=[]
    port_type=[]
    for s in port_seq:
        if(s in name_list):
            index=name_list.index(s)
            port_type.append(num_list[index])
            port_name_arranged.append(s)
    return [port_name_arranged,port_type]

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
def port_direction(port_name):#判断端口是什么类型的
    input_port=['AI', 'TI','TIA','TIB', 'BI','CI','SI', 'RI','TNRI','RESET']
    output_port=['AO','TO','TOA','TOB','TOC', 'BO' ,'TNRO','CO', 'ABO', 'AOA','AOB', 'AOC', 'OA', 'OB', 'OC','OUT']
    port_name=port_name.replace("wire","")
    if port_name in input_port:
        isOutput=False
    else:
        isOutput=True
    return isOutput


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
        script=\'\'\'
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list({12}:{13} {14}:{15}) ?width {16} ?justification "center" ?cvId  cellID)\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],path_1[0],path_1[1],path_2[0],path_2[1],path_width)
    elif(layer=="mn0"):
        script=\'\'\'
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))
rodCreatePath(?layer "mn0" ?pts list({12}:{13} {14}:{15}) ?width {16} ?justification "center" ?cvId  cellID)\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],path_1[0],path_1[1],path_2[0],path_2[1],output_width)
    return script

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
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
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
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0],origin[1]-wire_width/2]
                p2=[origin[0]-wire_width/tan675-x,origin[1]-wire_width/2]
                p3=[origin[0]-corner_width*layout_unit_len+x,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]
                p4=[origin[0]-corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]                
                p5=[origin[0]-corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p6=[origin[0]-corner_width*layout_unit_len+x+wire_width/tan675,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p7=[origin[0]-x,origin[1]+wire_width/2]
                p8=[origin[0],origin[1]+wire_width/2]
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==4):
            p1=[origin[0],origin[1]-wire_width/2]
            p2=[origin[0]-wire_width/tan675,origin[1]-wire_width/2]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]+wire_width/2]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    elif(in_index==2):
        if(out_index==1):
            p1=[origin[0]+wire_width/2,origin[1]]
            p2=[origin[0]+wire_width/2,origin[1]-wire_width/tan675]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p6=[origin[0]-wire_width/2,origin[1]]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
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
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0]-wire_width/2,origin[1]]
                p2=[origin[0]-wire_width/2,origin[1]-wire_width/tan675-x]
                p3=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len+x]
                p4=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]-corner_width*layout_unit_len]                
                p5=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len]
                p6=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]-corner_width*layout_unit_len+x+wire_width/tan675]
                p7=[origin[0]+wire_width/2,origin[1]-x]
                p8=[origin[0]+wire_width/2,origin[1]]
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==3):
            p1=[origin[0]-wire_width/2,origin[1]]
            p2=[origin[0]-wire_width/2,origin[1]-wire_width/tan675]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p6=[origin[0]+wire_width/2,origin[1]]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    elif(in_index==3):
        if(out_index==2):
            p1=[origin[0],origin[1]+wire_width/2]
            p2=[origin[0]+wire_width/tan675,origin[1]+wire_width/2]
            p3=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2+wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675]
            p4=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2+wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]+(corner_width-1)*layout_unit_len+layout_unit_len/2-wire_width/2,origin[1]-((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]-wire_width/2]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
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
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0],origin[1]-wire_width/2]
                p2=[origin[0]+wire_width/tan675+x,origin[1]-wire_width/2]
                p3=[origin[0]+corner_width*layout_unit_len-x,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]
                p4=[origin[0]+corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len-wire_width/2]                
                p5=[origin[0]+corner_width*layout_unit_len,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p6=[origin[0]+corner_width*layout_unit_len-x-wire_width/tan675,origin[1]+(corner_width-1)*layout_unit_len+wire_width/2]
                p7=[origin[0]+x,origin[1]+wire_width/2]
                p8=[origin[0],origin[1]+wire_width/2]
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==4):
            p1=[origin[0],origin[1]-wire_width/2]
            p2=[origin[0]+wire_width/tan675,origin[1]-wire_width/2]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)]
            p6=[origin[0],origin[1]+wire_width/2]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)

    elif(in_index==4):
        if(out_index==1):
            p1=[origin[0]+wire_width/2,origin[1]]
            p2=[origin[0]+wire_width/2,origin[1]+wire_width/tan675]
            p3=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/tan675,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p4=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p5=[origin[0]-((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p6=[origin[0]-wire_width/2,origin[1]]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
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
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
            elif(descend==0):
                p1=[origin[0]-wire_width/2,origin[1]]
                p2=[origin[0]-wire_width/2,origin[1]+wire_width/tan675+x]
                p3=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len-x]
                p4=[origin[0]+(corner_width-1)*layout_unit_len-wire_width/2,origin[1]+corner_width*layout_unit_len]                
                p5=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len]
                p6=[origin[0]+(corner_width-1)*layout_unit_len+wire_width/2,origin[1]+corner_width*layout_unit_len-x-wire_width/tan675]
                p7=[origin[0]+wire_width/2,origin[1]+x]
                p8=[origin[0]+wire_width/2,origin[1]]
                script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11} {13}:{14} {15}:{16}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type,p7[0],p7[1],p8[0],p8[1])
        elif(out_index==3):
            p1=[origin[0]-wire_width/2,origin[1]]
            p2=[origin[0]-wire_width/2,origin[1]+wire_width/tan675]
            p3=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/tan675,origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p4=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)+wire_width/2]
            p5=[origin[0]+((corner_width-1)*layout_unit_len+layout_unit_len/2),origin[1]+((corner_width-1)*layout_unit_len+layout_unit_len/2)-wire_width/2]
            p6=[origin[0]+wire_width/2,origin[1]]
            script=\'\'\'
rodCreatePolygon(?cvId cellID ?layer "{12}" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7} {8}:{9} {10}:{11}))\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1],p5[0],p5[1],p6[0],p6[1],wire_type)
            
    return script

def path(source,dest,width,wire_type):#普通线的模型 #origin为线的中心
    script=\'\'\'
rodCreatePath(?layer "{0}" ?pts list({2}:{3} {4}:{5}) ?width {1} ?justification "center" ?cvId  cellID)\'\'\'.format(wire_type,width,source[0],source[1],dest[0],dest[1])
    return script

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
    script=\'\'\'
ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list({0}:{1} {2}:{3} {4}:{5} {6}:{7}))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -1)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 1)\'\'\'.format(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],p4[0],p4[1])
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
    return script+ad_path1+ad_path2'''.encode("utf-8").decode("latin-1")

text=open("SFQ_lib_new.py","w")
print(other_script,file=text)
print(other_script2,file=text)
for key in celllist.keys():
    print(class_gen(key,celllist[key]).encode("utf-8").decode("latin-1"),file=text)
print(read_instance_gen(celllist).encode("utf-8").decode("latin-1"),file=text)
text.close()