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
display=0
#f = open(, 'a')
#sys.stdout = f
sys.stdout = Logger('route_{0}_{1}_{2}'.format(lib_name,cell_name,time_for_output))

start=time.time()
print("start routing optimization...")
info_list=map_info(File_dir)
#print(info_list[0])
currpath=os.getcwd()
if(os.path.isfile(currpath+"/createinst.il")):
	os.system("rm createinst.il")

if(layer_num=="mp1"):
	log_sum_to_flow=[]
	util_sum_to_flow=[]
	'''for c in range(len(info_list)):
		cross_map_search(info_list[c],lib_name,cell_name)'''
	p=Pool(30)
	results=[p.apply_async(cross_map_search,args=(info,lib_name,cell_name,display,)) for info in info_list]
	p.close()
	p.join()
#else:
#	multi_map_search(File_dir,lib_name,cell_name,1,2)
#for i in info_list:
#	print(i[-1])
#print(len(info_list[4]))
print("--------------------------------------Top-Level Summary ------------------------------------------")#以下输出summary信息
#print(results)
failed_path=[]
total=0
used=0
for r in results:
	#print(r.get())
	[failed,util]=r.get()
	for f in failed:
		failed_path.append(f)
	total+=util[0]
	used+=util[1]
if(len(failed_path)==0):
	print("No failed Path in routable area")
else:
	for f in failed_path:
		print("Failed:{0}".format(f))
util_round=int((used/total)*100000)/1000
print("Total Utilization for routable area:{0}%".format((util_round)))
#util_sum_temp=float(used/total)*10000
#util=int(util_sum_temp)
#print("Map Utilization for all routable area:{0}%".format(util*100))
end=time.time()
runtime=int((end-start)*1000)/1000
print("Run time:{0} sec".format(runtime))
done_flag=open("./flag_routing_finished",'w+')
print("routing finished",file=done_flag)
done_flag.close()
#createinst.close()
