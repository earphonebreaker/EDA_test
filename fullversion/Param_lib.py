#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8

#专门存放parameter的库
#2020/3/7 杨树澄


inf=float('inf') #常量无穷大
layout_unit_len=30 #版图单位长度


map_enlarge=40 #map扩充系数
map_offset=10 #map偏移系数

layer_straight_line=["ptl_13_mp1","ptl_13_mn0"] #以下为调用单元布线部分用到的模型和库
layer_corner_line=["ptl_14_mp1","ptl_14_mn0"]
route_lib="ysc_layout"

drv_out=4 #driver的输出口宽度
rec_out=8 #receiver的输入口长度
wire_width=14 #msl线宽
enlarge_coef=3 #interface延长系数

try_num=30 #retry程序的最大运行次数


