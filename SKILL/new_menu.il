;2020/2/12 杨树澄
;SFQ工具箱
;-----------------------------计算margin--------------------------------
procedure( margin_form( wid )
let( ( margin_dir margin_lib margin_cell margin1Symbol margin1 )
;获取当前编辑的单元信息↓
deCV_margin = deGetEditCellView()
libName_margin = deCV_margin~>libName
cellName_margin = deCV_margin~>cellName
viewName_margin = deCV_margin~>viewName
;目录↓
margin_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'margin_dir
?value "~/Cadence/designs/"
?defValue "~/Cadence/designs/"
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
;表格主体↓
margin1Symbol = gensym( 'WindowForm ) 
margin1 = hiCreateAppForm(
?name margin1Symbol
?formTitle "Calculate Margins"
?callback  "mycallbackfunc_margin( hiGetCurrentForm() )"
?dontBlock t
?fields list( margin_dir margin_lib margin_cell )
?unmapAfterCB t )
margin1->wid = wid ;;; associate the wid with the form, via a user-
;;; defined slot
margin1 ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_margin( margin1 )
let( ( wid getdir_margin getlib_margin getcell_margin )
;;; pick up current form values
wid = margin1->wid ;;; user specified slot linking the form
;;; to the window
getdir_margin = margin1->margin_dir->value
getlib_margin = margin1->margin_lib->value
getcell_margin = margin1->margin_cell->value
;;; set the window name
;println( getdir )
;println( getlib )
;println( getcell )
CalculateMargins(getdir_margin)
pscan_netlist( getdir_margin getlib_margin getcell_margin )
system("bash margin.sh")
system("rm margin.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( margin_window()
let( ( wf )
wf=margin_form(window(1))
hiDisplayForm( wf )
)
)
;生成sh脚本
procedure( CalculateMargins( str )
let( ( f )
f = outfile("./margin.sh" "w")
c=strcat( "cd" " " str)
d="python margins.py main"
e="cp /home/SIMIT/yangshucheng/files/margins.py ./" ;此处为复制到仿真目录的margin脚本地址
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s" d )
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

procedure( timing_form( wid2 )
let( ( timing_dir timing_lib timing_cell timing1Symbol timing1 )

deCV_timing = deGetEditCellView()
libName_timing = deCV_timing~>libName
cellName_timing = deCV_timing~>cellName
viewName_timing = deCV_timing~>viewName

timing_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'timing_dir
?value "~/Cadence/designs/"
?defValue "~/Cadence/designs/"
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

timing1Symbol = gensym( 'WindowForm ) ;;; advanced version
;;; otherwise use 'WindowForm

timing1 = hiCreateAppForm(
?name timing1Symbol
?formTitle "Timing extraction"
?callback  "mycallbackfunc_timing( hiGetCurrentForm() )"
?dontBlock t
?fields list( timing_dir timing_lib timing_cell )
?unmapAfterCB t )
timing1->wid2 = wid2 ;;; associate the wid with the form, via a user-
;;; defined slot
timing1 ;;; my return value
) ; let
) ; procedure

procedure( mycallbackfunc_timing( timing1 )
let( ( wid2 getdir_timing getlib_timing getcell_timing )
;;; pick up current form values
wid2 = timing1->wid2 ;;; user specified slot linking the form
;;; to the window
getdir_timing = timing1->timing_dir->value
getlib_timing = timing1->timing_lib->value
getcell_timing = timing1->timing_cell->value
;;; set the window name
;println( getdir )
;println( getlib )
;println( getcell )
CalculateTiming(getdir_timing)
pscan_netlist( getdir_timing getlib_timing getcell_timing )
ipcBeginProcess("bash timing.sh") ;ipc函数后台运行，不显示在terminal内
system("rm timing.sh") 
t ;;; my return value
) ; let
) ; procedure

procedure( timing_window()
let( ( wf_timing )
wf_timing=timing_form(window(1))
hiDisplayForm( wf_timing )
)
)

procedure( CalculateTiming( str )
let( ( f )
f = outfile("./timing.sh" "w")
c=strcat( "cd" " " str)
d="python Timing_extract.py --circuit=main --param1=DAT --step1=1 --max1=30 --min1=0 --param2=XI --step2=0.05 --max2=1.35 --min2=0.7";后期考虑加入这些参数设置
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
;目录↓
psui_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'psui_dir
?value "~/Cadence/designs/"
?defValue "~/Cadence/designs/"
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
system("bash psui.sh")
system("rm psui.sh")
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
;目录↓
simulate_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'simulate_dir
?value "~/Cadence/designs/"
?defValue "~/Cadence/designs/"
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
system("bash simulate.sh")
system("rm simulate.sh")
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
procedure( SFQSimulate( str )
let( ( f )
f = outfile("./simulate.sh" "w")
c=strcat( "cd" " " str)
d="python simulate.py main"
e="cp /home/SIMIT/yangshucheng/files/simulate.py ./" ;此处为复制到仿真目录的simulate脚本地址
fprintf( f "%s\n" c )
fprintf( f "%s\n" e )
fprintf( f "%s" d )
close(f)
)
)
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
?callback "psui_window" ;预留
)
menuItem_timing=hiCreateMenuItem( ;菜单栏3
?name 'Timing
?itemText "Timing"
?callback "timing_window" ;预留
)
menuItem_simulate=hiCreateMenuItem( ;菜单栏3
?name 'Simulate
?itemText "Simulate"
?callback "simulate_window" ;预留
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'trSubMenuA
""
list(
menuItem_simulate
menuItem_margins
menuItem_psui
menuItem_timing
)
)
;设置带slider的菜单选项-前仿
sliderMenuItem_A = hiCreateSliderMenuItem( 
?name 'menu_A
?itemText "front-end"
?subMenu trSubMenuA
)
;设置分割线
separator_1=hiCreateSeparatorMenuItem(
?name 'menu_S
)
;后仿菜单选项卡
menuItem_4=hiCreateMenuItem( ;菜单栏4
?name 'menu_4
?itemText "Placement"
?callback "function_4" ;预留
)
menuItem_5=hiCreateMenuItem( ;菜单栏5
?name 'menu_5
?itemText "Routing"
?callback "function_5" ;预留
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'trSubMenuB
""
list(
menuItem_4
menuItem_5
)
)
;设置带slider的菜单选项
sliderMenuItem_B = hiCreateSliderMenuItem( 
?name 'menu_B
?itemText "back-end"
?subMenu trSubMenuB
)

menuItem_B= hiCreateMenuItem(
?name 'menu_B
?itemText "back-end"
?callback "function_B"
)

menuItem_C= hiCreateMenuItem(
?name 'menu_C
?itemText "other"
?callback "function_C"
)

hiCreatePulldownMenu(
'trPulldownMenu
"SFQsim"
list( sliderMenuItem_A sliderMenuItem_B  separator_1 menuItem_C )
)
;添加至layout窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'trPulldownMenu (hiGetNumMenus (hiGetCIWindow)));
procedure(add_layout_menu(args)
hiInsertBannerMenu((getCurrentWindow) 'trPulldownMenu (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("maskLayout"  nil nil 'add_layout_menu)
;------------------------------------------------------------------------------

;添加至schematic窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'trPulldownMenu (hiGetNumMenus (hiGetCIWindow)));
procedure(add_schematic_menu(args)
hiInsertBannerMenu((getCurrentWindow) 'trPulldownMenu (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("schematic"  nil nil 'add_schematic_menu)
;------------------------------------------------------------------------------