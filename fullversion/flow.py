#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import time
from SFQ_lib import *
from Astar_lib import *
from Layout_lib import *
from Netlist_lib import *
from Param_lib import *
import sys, time,os
from multiprocessing.pool import Pool

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

timer = time.localtime(time.time())
time_for_output = "{3}d{0}h{1}m{2}s".format(timer.tm_hour,timer.tm_min,timer.tm_sec,timer.tm_mday)
File_dir=sys.argv[1]
lib_name=sys.argv[2]
cell_name=sys.argv[3]
layer_num=sys.argv[4]
#f = open(, 'a')
#sys.stdout = f
#sys.stdout = Logger('route_{0}_{1}_{2}'.format(lib_name,cell_name,time_for_output))

start=time.time()
print("start routing optimization...")
info_list=map_info(File_dir)
#print(info_list[0])
currpath=os.getcwd()
if(os.path.isfile(currpath+"/createinst.il")):
	os.system("rm createinst.il")

if(layer_num=="mp1"):
	'''for c in range(len(info_list)):
		cross_map_search(info_list[c],lib_name,cell_name)'''
	p=Pool(20)
	for c in range(len(info_list)):
		p.apply_async(cross_map_search,args=(info_list[c],lib_name,cell_name,))
	p.close()
	p.join()
#else:
#	multi_map_search(File_dir,lib_name,cell_name,1,2)
#for i in info_list:
#	print(i[-1])
#print(len(info_list[4]))
end=time.time()
print("Run time:{0}".format(end-start))
done_flag=open("./flag_routing_finished",'w+')
print("routing finished",file=done_flag)
done_flag.close()
#createinst.close()
