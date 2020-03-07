;2020/2/12 杨树澄
;2020/3/4 route功能整合，接口工作正常
;SFQ工具箱
;-----------------------------计算margin--------------------------------
procedure( margin_form( wid_margin )
let( ( margin_dir margin_lib margin_cell margin_max margin_eps  margin1Symbol margin1 )
;获取当前编辑的单元信息↓
deCV_margin = deGetEditCellView()
libName_margin = deCV_margin~>libName
cellName_margin = deCV_margin~>cellName
viewName_margin = deCV_margin~>viewName
dirwithcellview_margin=strcat( "~/Cadence/designs/" cellName_margin )
;目录↓
margin_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'margin_dir
?value dirwithcellview_margin
?defValue dirwithcellview_margin
)
;库名↓
margin_lib = hiCreateStringField(
?prompt "Library Name"
?name 'margin_lib
?value libName_margin
?defValue libName_margin
)
;单元名↓
margin_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'margin_cell
?value cellName_margin
?defValue cellName_margin
)

;最大上确界↓
margin_max = hiCreateStringField(
?prompt "Max margin"
?name 'margin_max
?value "0.5"
?defValue "0.5"
)
;精度↓
margin_eps = hiCreateStringField(
?prompt "Eps"
?name 'margin_eps
?value "0.01"
?defValue "0.01"
)

;表格主体↓
margin1Symbol = gensym( 'WindowForm ) 
margin1 = hiCreateAppForm(
?name margin1Symbol
?formTitle "Calculate Margins"
?callback  "mycallbackfunc_margin( hiGetCurrentForm() )"
?dontBlock t
?fields list( margin_dir margin_lib margin_cell margin_max margin_eps )
?unmapAfterCB t )
margin1->wid_margin = wid_margin ;;; associate the wid with the form, via a user-
;;; defined slot
margin1 ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_margin( margin1 )
let( ( wid_margin getdir_margin getlib_margin getcell_margin get_max get_eps)
;;; pick up current form values
wid_margin = margin1->wid_margin ;;; user specified slot linking the form
;;; to the window
getdir_margin = margin1->margin_dir->value
getlib_margin = margin1->margin_lib->value
getcell_margin = margin1->margin_cell->value
getmax_margin = margin1->margin_max->value
geteps_margin = margin1->margin_eps->value
CalculateMargins(getdir_margin getmax_margin geteps_margin)
pscan_netlist( getdir_margin getlib_margin getcell_margin )
system("gnome-terminal -x bash -c 'sh ./margin.sh;exec bash'")
ipcSleep(1)
ipcBeginProcess("rm margin.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( margin_window()
let( ( wf_margin )
wf_margin=margin_form(window(1))
hiDisplayForm( wf_margin )
)
)
;生成sh脚本
procedure( CalculateMargins( dir max eps )
let( ( f )
f = outfile("./margin.sh" "w")
c=strcat( "cd" " " dir)
d=strcat( "python margins_for_SKILL.py main " max " " eps )
e="cp /home/SIMIT/yangshucheng/files/margins_for_SKILL.py ./" ;此处为复制到仿真目录的margin脚本地址
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s\n" d )
close(f)
)
)
;网表定向生成
procedure( pscan_netlist( path lib cell )
let( ( n )
simInitEnvWithArgs( 
path
lib
cell
"schematic"
"pscan2"
"forceInit"
) 

simSetEnvOptions() 
simEnvOptionsForm->simFormIncrNetlist->myChoice->value =  nil 
simEnvOptionsForm->simFormNetlistHier->myChoice->value =  t 
hiFormDone(simEnvOptionsForm) 

simRunNetAndSimWithArgs( 
lib
cell
"schematic"
"pscan2"
t
nil
nil
10
) 

)
)
;----------------------------提时序------------------------------------
;margin模块复制过来改的，只有ipc处有变化

procedure( timing_form( wid_timing )
let( ( timing_dir timing_lib timing_cell timing_param1 timing_step1 timing_max1 timing_min1 timing_param2 timing_step2 timing_max2 timing_min2 timing1Symbol timing1 )

deCV_timing = deGetEditCellView()
libName_timing = deCV_timing~>libName
cellName_timing = deCV_timing~>cellName
viewName_timing = deCV_timing~>viewName
dirwithcellview_timing=strcat( "~/Cadence/designs/" cellName_timing )

timing_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'timing_dir
?value dirwithcellview_timing
?defValue dirwithcellview_timing
)

timing_lib = hiCreateStringField(
?prompt "Library Name"
?name 'timing_lib
?value libName_timing
?defValue libName_timing
)

timing_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'timing_cell
?value cellName_timing
?defValue cellName_timing
)


timing_param1 = hiCreateStringField(
?prompt "Parameter 1"
?name 'timing_param1
?value "DAT"
?defValue "DAT"
)
timing_step1 = hiCreateStringField(
?prompt "Step 1"
?name 'timing_step1
?value "1"
?defValue "1"
)
timing_max1 = hiCreateStringField(
?prompt "Max 1"
?name 'timing_max1
?value "30"
?defValue "30"
)
timing_min1 = hiCreateStringField(
?prompt "Min 1"
?name 'timing_min1
?value "0"
?defValue "0"
)



timing_param2 = hiCreateStringField(
?prompt "Parameter 2"
?name 'timing_param2
?value "XI"
?defValue "XI"
)
timing_step2 = hiCreateStringField(
?prompt "Step 2"
?name 'timing_step2
?value "0.05"
?defValue "0.05"
)
timing_max2 = hiCreateStringField(
?prompt "Max 2"
?name 'timing_max2
?value "1.35"
?defValue "1.35"
)
timing_min2 = hiCreateStringField(
?prompt "Min 2"
?name 'timing_min2
?value "0.7"
?defValue "0.7"
)


timing1Symbol = gensym( 'WindowForm ) ;;; advanced version
;;; otherwise use 'WindowForm

timing1 = hiCreateAppForm(
?name timing1Symbol
?formTitle "Timing extraction"
?callback  "mycallbackfunc_timing( hiGetCurrentForm() )"
?dontBlock t
?fields list( timing_dir timing_lib timing_cell timing_param1 timing_step1 timing_max1 timing_min1 timing_param2 timing_step2 timing_max2 timing_min2)
?unmapAfterCB t )
timing1->wid_timing = wid_timing ;;; associate the wid with the form, via a user-
;;; defined slot
timing1 ;;; my return value
) ; let
) ; procedure

procedure( mycallbackfunc_timing( timing1 )
let( ( wid_timing getdir_timing getlib_timing getcell_timing getparam1 getstep1 getmax1 getmin1 getparam2 getstep2 getmax2 getmin2)
;;; pick up current form values
wid_timing = timing1->wid_timing ;;; user specified slot linking the form
;;; to the window
getdir_timing = timing1->timing_dir->value
getlib_timing = timing1->timing_lib->value
getcell_timing = timing1->timing_cell->value
getparam1 = timing1->timing_param1->value
getstep1 = timing1->timing_step1->value
getmax1 = timing1->timing_max1->value
getmin1 = timing1->timing_min1->value
getparam2 = timing1->timing_param2->value
getstep2 = timing1->timing_step2->value
getmax2 = timing1->timing_max2->value
getmin2 = timing1->timing_min2->value

CalculateTiming(getdir_timing getparam1 getstep1 getmax1 getmin1 getparam2 getstep2 getmax2 getmin2)
pscan_netlist( getdir_timing getlib_timing getcell_timing )
ipcBeginProcess("bash timing.sh") ;ipc函数后台运行，不显示在terminal内
ipcSleep(1)
ipcBeginProcess("rm timing.sh")
t ;;; my return value
) ; let
) ; procedure

procedure( timing_window()
let( ( wf_timing )
wf_timing=timing_form(window(1))
hiDisplayForm( wf_timing )
)
)
;    python Timing_extract.py --circuit=main --param1=DAT --step1=1 --max1=30 --min1=0 --param2=XI --step2=0.05 --max2=1.35 --min2=0.7

procedure( CalculateTiming( dir param1 step1 max1 min1 param2 step2 max2 min2 )
let( ( f )
f = outfile("./timing.sh" "w")
c=strcat( "cd" " " dir)
d=strcat( "python Timing_extract.py --circuit=main --param1=" param1 " --step1=" step1 " --max1=" max1 " --min1=" min1 " --param2=" param2 " --step2=" step2 " --max2=" max2 " --min2=" min2 );后期考虑加入这些参数设置
e="cp /home/SIMIT/yangshucheng/files/Timing_extract.py ./"
a="cp /home/SIMIT/yangshucheng/files/pscanrc.py ./"
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s\n" a )
fprintf( f "%s" d )
close(f)
)
)
;--------------------------psui主菜单-----------------------------------
procedure( psui_form( wid_psui )
let( ( psui_dir psui_lib psui_cell psui1Symbol psui1 )
;获取当前编辑的单元信息↓
deCV_psui = deGetEditCellView()
libName_psui = deCV_psui~>libName
cellName_psui = deCV_psui~>cellName
viewName_psui = deCV_psui~>viewName
dirwithcellview_psui=strcat( "~/Cadence/designs/" cellName_psui )

;目录↓
psui_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'psui_dir
?value dirwithcellview_psui
?defValue dirwithcellview_psui
)
;库名↓
psui_lib = hiCreateStringField(
?prompt "Library Name"
?name 'psui_lib
?value libName_psui
?defValue libName_psui
)
;单元名↓
psui_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'psui_cell
?value cellName_psui
?defValue cellName_psui
)
;表格主体↓
psui1Symbol = gensym( 'WindowForm ) 
psui1 = hiCreateAppForm(
?name psui1Symbol
?formTitle "Psui Initialize"
?callback  "mycallbackfunc_psui( hiGetCurrentForm() )"
?dontBlock t
?fields list( psui_dir psui_lib psui_cell )
?unmapAfterCB t )
psui1->wid_psui = wid_psui ;;; associate the wid with the form, via a user-
;;; defined slot
psui1 ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_psui( psui1 )
let( ( wid_psui getdir_psui getlib_psui getcell_psui )
;;; pick up current form values
wid_psui = psui1->wid_psui ;;; user specified slot linking the form
;;; to the window
getdir_psui = psui1->psui_dir->value
getlib_psui = psui1->psui_lib->value
getcell_psui = psui1->psui_cell->value
PsuiInitialize(getdir_psui)
pscan_netlist( getdir_psui getlib_psui getcell_psui )
system("gnome-terminal -x bash -c 'sh ./psui.sh;exec bash;rm psui.sh'")
ipcSleep(1)
ipcBeginProcess("rm psui.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( psui_window()
let( ( wf_psui )
wf_psui=psui_form(window(1))
hiDisplayForm( wf_psui )
)
)
;生成sh脚本
procedure( PsuiInitialize( str )
let( ( f )
f = outfile("./psui.sh" "w")
c=strcat( "cd" " " str)
d="python psui.py main"
e="cp /home/SIMIT/yangshucheng/files/psui.py ./" ;此处为复制到仿真目录的psui脚本地址
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s" d )
close(f)
)
)
;--------------------------------------------------------------------------
;--------------------------simulate-----------------------------------
procedure( simulate_form( wid_simulate )
let( ( simulate_dir simulate_lib simulate_cell simulate1Symbol simulate1 )
;获取当前编辑的单元信息↓
deCV_simulate = deGetEditCellView()
libName_simulate = deCV_simulate~>libName
cellName_simulate = deCV_simulate~>cellName
viewName_simulate = deCV_simulate~>viewName
dirwithcellview_simulate=strcat( "~/Cadence/designs/" cellName_simulate )

;目录↓
simulate_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'simulate_dir
?value dirwithcellview_simulate
?defValue dirwithcellview_simulate
)
;库名↓
simulate_lib = hiCreateStringField(
?prompt "Library Name"
?name 'simulate_lib
?value libName_simulate
?defValue libName_simulate
)
;单元名↓
simulate_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'simulate_cell
?value cellName_simulate
?defValue cellName_simulate
)
;表格主体↓
simulate1Symbol = gensym( 'WindowForm ) 
simulate1 = hiCreateAppForm(
?name simulate1Symbol
?formTitle "Simulate"
?callback  "mycallbackfunc_simulate( hiGetCurrentForm() )"
?dontBlock t
?fields list( simulate_dir simulate_lib simulate_cell )
?unmapAfterCB t )
simulate1->wid_simulate = wid_simulate ;;; associate the wid with the form, via a user-
;;; defined slot
simulate1 ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_simulate( simulate1 )
let( ( wid_simulate getdir_simulate getlib_simulate getcell_simulate )
;;; pick up current form values
wid_simulate = simulate1->wid_simulate ;;; user specified slot linking the form
;;; to the window
getdir_simulate = simulate1->simulate_dir->value
getlib_simulate = simulate1->simulate_lib->value
getcell_simulate = simulate1->simulate_cell->value
SFQSimulate(getdir_simulate)
pscan_netlist( getdir_simulate getlib_simulate getcell_simulate )
system("gnome-terminal -x bash -c 'sh ./simulate.sh;exec bash;rm ./simulate.sh'")
ipcSleep(1)
ipcBeginProcess("rm simulate.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( simulate_window()
let( ( wf_simulate )
wf_simulate=simulate_form(window(1))
hiDisplayForm( wf_simulate )
)
)
;生成sh脚本
procedure( SFQSimulate( path )
let( ( f )
f = outfile("./simulate.sh" "w")
c=strcat( "cd" " " path)
d="python simulate.py main"
e="cp /home/SIMIT/yangshucheng/files/simulate.py ./" ;此处为复制到仿真目录的simulate脚本地址
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s" d )
close(f)
)
)
;--------------------------------------------------------------------------

;--------------------------routing-----------------------------------
procedure( routing_form( wid_routing )
let( ( routing_plot routing_dir routing_lib routing_cell routing1Symbol routing1 )
;获取当前编辑的单元信息↓
deCV_routing = deGetEditCellView()
libName_routing = deCV_routing~>libName
cellName_routing = deCV_routing~>cellName
viewName_routing = deCV_routing~>viewName
dirwithcellview_routing=strcat( "~/Cadence/designs/" cellName_routing )

;choice这个模块不用了，留着给其他窗口用
routing_plot=hiCreateRadioField(
?name `radiofield1 
?choices `("on" "off") 
?prompt "Plot" 
?value "off" 
?defValue "off" 
?callback nil
)

;库名↓
routing_lib = hiCreateStringField(
?prompt "Library Name"
?name 'routing_lib
?value libName_routing
?defValue libName_routing
)
;单元名↓
routing_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'routing_cell
?value cellName_routing
?defValue cellName_routing
)

dir_netlist=strcat( "~/Cadence/" )
;netlist目录↓
Netlist_for_route_dir = hiCreateStringField(
?prompt "Netlist Directory"
?name 'Netlist_for_route_dir
?value dir_netlist
?defValue dir_netlist
)

;表格主体↓
routing1Symbol = gensym( 'WindowForm ) 
routing1 = hiCreateAppForm(
?name routing1Symbol
?formTitle "Routing"
?callback  "mycallbackfunc_routing( hiGetCurrentForm() )"
?dontBlock t
?fields list( routing_lib routing_cell Netlist_for_route_dir)
?unmapAfterCB t )
routing1->wid_routing = wid_routing ;
routing1 ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_routing( routing1 )
let( ( wid_routing getlib_routing getcell_routing plot_op_routing)
;;; pick up current form values
wid_routing = routing1->wid_routing ;;; user specified slot linking the form
;;; to the window
;获取当前打开的单元信息
getlib_routing = routing1->routing_lib->value
getcell_routing = routing1->routing_cell->value
plot_op_routing = routing1->radiofield1->value
getnetlistdir_routing = routing1->Netlist_for_route_dir->value
;print(plot_op_routing)
;输出当前单元的inst名和位置orient等等等信息
routing_info_out( getlib_routing getcell_routing )
;输出一个py的plot脚本，原来用于debug的，现在不用了
;routing_py( plot_op_routing )
;print(getnetlistdir_routing)
;输出routing脚本的generator
routing_py_gen( getnetlistdir_routing getlib_routing getcell_routing )
;从源目录source需要的lib文件
system("cp /home/SIMIT/yangshucheng/files/routing_source/Astar_lib.py ./")
system("cp /home/SIMIT/yangshucheng/files/routing_source/Layout_lib.py ./")
system("cp /home/SIMIT/yangshucheng/files/routing_source/Netlist_lib.py ./")
system("cp /home/SIMIT/yangshucheng/files/routing_source/SFQ_lib.py ./")
system("cp /home/SIMIT/yangshucheng/files/routing_source/flow.py ./")
;plot执行文件，现在不用了
;system("bash ./routing.sh")
;运行route的generator
run_route_gen=ipcBeginProcess("bash ./routing_gen.sh")
;等待程序运行结束
ipcWait(run_route_gen)
;读取例化布线模块的信息
load("./createinst.il")
;删除不需要的lib文件和脚本文件等中间文件
system("rm createinst.il")
system("rm Astar_lib.py")
system("rm Layout_lib.py")
system("rm Netlist_lib.py")
system("rm flow.py")
system("rm SFQ_lib.py")
system("rm routing_name.txt")
system("rm routing_bbox.txt")
system("rm routing_inst.txt")
system("rm routing_xy.txt")
system("rm routing_orient.txt")
;system("rm routing.sh")
system("rm routing_gen.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( routing_window()
let( ( wf_routing )
wf_routing=routing_form(window(1))
hiDisplayForm( wf_routing )
)
)

;生成sh脚本 for plot
procedure( routing_py( var )
let( ( f_py_routing )
f_py_routing = outfile("./routing.sh" "w")
d=strcat("python plot_layout.py " var)
fprintf( f_py_routing "%s" d )
close(f_py_routing)
)
)
;生成sh脚本 for route
procedure( routing_py_gen( path lib cell )
let( ( f_py_routing_gen )
f_py_routing_gen = outfile("./routing_gen.sh" "w")
d=strcat("python flow.py " path " " lib " " cell)
fprintf( f_py_routing_gen "%s" d )
close(f_py_routing_gen)
)
)
;生成layout info
procedure( routing_info_out( lib cell )
let( ( f_name f_orient f_bbox )
cellID = dbOpenCellViewByType( lib cell "layout" )
cellname=cellID~>instances~>cellName
bBox=cellID~>instances~>bBox
orient=cellID~>instances~>orient
xyinfo=cellID~>instances~>xy
inst=cellID~>instances~>name
f_name = outfile("./routing_name.txt" "w")
foreach( item cellname
	fprintf( f_name "%s\n" item ))
close(f_name)
f_orient = outfile("./routing_orient.txt" "w")
foreach( item orient
	fprintf( f_orient "%s\n" item ))
close(f_orient)
f_bbox = outfile("./routing_bbox.txt" "w")
foreach( item bBox
	fprintf( f_bbox "%L\n" item ))
close(f_bbox)
f_xy = outfile("./routing_xy.txt" "w")
foreach( item xyinfo
	fprintf( f_xy "%L\n" item ))
close(f_xy)
f_inst = outfile("./routing_inst.txt" "w")
foreach( item inst
	fprintf( f_inst "%s\n" item ))
close(f_inst)
);let
);proc
;--------------------------------------------------------------------------


;菜单栏设置
menuItem_margins=hiCreateMenuItem( ;菜单栏1
?name 'Margins
?itemText "Margins"
?callback "margin_window" ;调用表格函数
)
menuItem_psui=hiCreateMenuItem( ;菜单栏2
?name 'psui
?itemText "psui"
?callback "psui_window" ;
)
menuItem_timing=hiCreateMenuItem( ;菜单栏3
?name 'Timing
?itemText "Timing"
?callback "timing_window" ;
)
menuItem_simulate=hiCreateMenuItem( ;菜单栏3
?name 'Simulate
?itemText "Simulate"
?callback "simulate_window" ;
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'Presim_SFQtool
""
list(
menuItem_simulate
menuItem_margins
menuItem_psui
menuItem_timing
)
)
;设置带slider的菜单选项-前仿
Presim_Slider_SFQ = hiCreateSliderMenuItem( 
?name 'Presim_SFQ
?itemText "front-end"
?subMenu Presim_SFQtool
)
;设置分割线
separator_SFQtool=hiCreateSeparatorMenuItem(
?name 'spt_SFQtool
)
;后仿菜单选项卡
menuItem_placement=hiCreateMenuItem( ;菜单栏4
?name 'Backend_Place_SFQtool
?itemText "Placement"
?callback "function_4" ;预留
)
menuItem_routing=hiCreateMenuItem( ;菜单栏5
?name 'Backend_Route_SFQtool
?itemText "Routing"
?callback "routing_window" ;
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'Backend_SFQtool
""
list(
menuItem_placement
menuItem_routing
)
)
;设置带slider的菜单选项
Backend_Slider_SFQ = hiCreateSliderMenuItem( 
?name 'Backend_SFQ
?itemText "back-end"
?subMenu Backend_SFQtool
)

Menu_other_SFQtool= hiCreateMenuItem(
?name 'menu_other_sfqtool
?itemText "other"
?callback "function_C"
)

hiCreatePulldownMenu(
'SFQ_pulldown
"SFQtool"
list( Presim_Slider_SFQ Backend_Slider_SFQ  separator_SFQtool Menu_other_SFQtool )
)
;添加至layout窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'SFQ_pulldown (hiGetNumMenus (hiGetCIWindow)));
procedure(add_layout_menu_SFQ(args)
hiInsertBannerMenu((getCurrentWindow) 'SFQ_pulldown (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("maskLayout"  nil nil 'add_layout_menu_SFQ)
;------------------------------------------------------------------------------

;添加至schematic窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'SFQ_pulldown (hiGetNumMenus (hiGetCIWindow)));
procedure(add_schematic_menu_SFQ(args)
hiInsertBannerMenu((getCurrentWindow) 'SFQ_pulldown (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("schematic"  nil nil 'add_schematic_menu_SFQ)
;------------------------------------------------------------------------------