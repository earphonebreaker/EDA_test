# -*- coding: utf-8 -*-
#2020/3/21 ysc
file_list=[
"./SKILL/sfqtool.il",
"./SKILL/upload.il",
"./script_source/margins.py",
"./auxes/multiple_sim/auto_margin_extract",
"./auxes/multiple_sim/auto_margin_extract_witharg",
"./auxes/multiple_sim/auto_timing_extract",
"./auxes/multiple_sim/auto_timing_extract_witharg",
"./auxes/multiple_sim/fullyauto_timing_extract_witharg"
]

import os,sys
curr_dir=os.getcwd()
for f in file_list:
	with open ( f , "r" ) as ref:
		rewrite_file=open("{0}temp".format(f),"w+")
		for l in ref.readlines():
			if "env_path=\"" in l:
				print("env_path=\"{0}/\"".format(curr_dir),file=rewrite_file)
			else:
				print(l.rstrip(),file=rewrite_file)
		rewrite_file.close()
for f in file_list:
	os.system("rm {0}".format(f))
	os.system("mv {0}temp {1}".format(f,f))
