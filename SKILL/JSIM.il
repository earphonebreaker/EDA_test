;2020/3/5 杨树澄
;2020/3/18 Update:添加了margin和simulate的单一单元的仿真选项，和psui菜单
;JSIM菜单
;--------------------------Margin_sweep-----------------------------------
procedure( marginsw_form_jsim( wid_marginsw_jsim )
let( ( marginsw_jsim_dir marginsw_jsim_lib marginsw_jsim_cell marginsw_jsim_1Symbol marginsw1_jsim )
;获取当前编辑的单元信息↓
deCV_marginsw_jsim = deGetEditCellView()
libName_marginsw_jsim = deCV_marginsw_jsim~>libName
cellName_marginsw_jsim = deCV_marginsw_jsim~>cellName
viewName_marginsw_jsim = deCV_marginsw_jsim~>viewName
dirwithcellview_marginsw_jsim=strcat( "~/Cadence/designs/" cellName_marginsw_jsim )

;目录↓
marginsw_dir_jsim = hiCreateStringField(
?prompt "Target Directory"
?name 'marginsw_dir_jsim
?value dirwithcellview_marginsw_jsim
?defValue dirwithcellview_marginsw_jsim
)
;库名↓
marginsw_lib_jsim = hiCreateStringField(
?prompt "Library Name"
?name 'marginsw_lib_jsim
?value libName_marginsw_jsim
?defValue libName_marginsw_jsim
)
;单元名↓
marginsw_cell_jsim = hiCreateStringField(
?prompt "Cellview Name"
?name 'marginsw_cell_jsim
?value cellName_marginsw_jsim
?defValue cellName_marginsw_jsim
)

;param↓
marginsw_param_jsim = hiCreateStringField(
?prompt "Dependent Variable"
?name 'marginsw_param_jsim
?value "XI,XJ,XL"
?defValue "XI,XJ,XL"
)

;max margin↓
marginsw_max_jsim = hiCreateStringField(
?prompt "Max margin"
?name 'marginsw_max_jsim
?value "0.5"
?defValue "0.5"
)

;swparam↓
marginsw_swparam_jsim = hiCreateStringField(
?prompt "Independent Variable"
?name 'marginsw_swparam_jsim
?value "TQ"
?defValue "TQ"
)

;sweep_max↓
marginsw_from_jsim = hiCreateStringField(
?prompt "From"
?name 'marginsw_from_jsim
?value "20"
?defValue "20"
)

;sweep_min↓
marginsw_to_jsim = hiCreateStringField(
?prompt "To"
?name 'marginsw_to_jsim
?value "100"
?defValue "100"
)

;sweep_step↓
marginsw_step_jsim = hiCreateStringField(
?prompt "Step"
?name 'marginsw_step_jsim
?value "10"
?defValue "10"
)
;表格主体↓
marginsw_jsim_1Symbol = gensym( 'WindowForm ) 
marginsw1_jsim = hiCreateAppForm(
?name marginsw_jsim_1Symbol
?formTitle "margin sweep"
?callback  "mycallbackfunc_marginsw_jsim( hiGetCurrentForm() )"
?dontBlock t
?fields list( marginsw_dir_jsim marginsw_lib_jsim marginsw_cell_jsim marginsw_swparam_jsim marginsw_from_jsim marginsw_to_jsim marginsw_step_jsim marginsw_param_jsim marginsw_max_jsim )
?unmapAfterCB t )
marginsw1_jsim->wid_marginsw_jsim = wid_marginsw_jsim ;;; associate the wid with the form, via a user-
;;; defined slot
marginsw1_jsim ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_marginsw_jsim( marginsw1_jsim )
let( ( wid_marginsw_jsim getdir_marginsw_jsim getlib_marginsw_jsim getcell_marginsw_jsim )
;;; pick up current form values
wid_marginsw_jsim = marginsw1_jsim->wid_marginsw_jsim ;;; user specified slot linking the form
;;; to the window
getdir_marginsw_jsim = marginsw1_jsim->marginsw_dir_jsim->value
getlib_marginsw_jsim = marginsw1_jsim->marginsw_lib_jsim->value
getcell_marginsw_jsim = marginsw1_jsim->marginsw_cell_jsim->value
getswparam_marginsw_jsim = marginsw1_jsim->marginsw_swparam_jsim->value
getfrom_marginsw_jsim = marginsw1_jsim->marginsw_from_jsim->value
getto_marginsw_jsim = marginsw1_jsim->marginsw_to_jsim->value
getstep_marginsw_jsim = marginsw1_jsim->marginsw_step_jsim->value
getparam_marginsw_jsim = marginsw1_jsim->marginsw_param_jsim->value
getmax_marginsw_jsim = marginsw1_jsim->marginsw_max_jsim->value
;print(getdir_marginsw_jsim getfrom_marginsw_jsim)
Generate_JSIC_marginsw( getdir_marginsw_jsim getparam_marginsw_jsim getmax_marginsw_jsim getswparam_marginsw_jsim getfrom_marginsw_jsim getto_marginsw_jsim getstep_marginsw_jsim)
pscan_netlist_jsim( getdir_marginsw_jsim getlib_marginsw_jsim getcell_marginsw_jsim )
system("chmod +x ./JSICsim_marginsw.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_marginsw.sh';exec bash'")
ipcSleep(1)
ipcBeginProcess("rm JSICsim_marginsw.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( marginsw_window_jsim()
let( ( wf_marginsw_jsim )
wf_marginsw_jsim=marginsw_form_jsim(window(1))
hiDisplayForm( wf_marginsw_jsim )
)
)
procedure( Generate_JSIC_marginsw( dir param max swparam from to step)
let( ( f )
f = outfile("./JSICsim_marginsw.sh" "w")
c=strcat( "cd" " " dir)
d="JSICsim margin -m "
e=strcat( d param " -M " max " -p " swparam "=" from ":" to ":" step )
fprintf( f "%s\n" c )
fprintf( f "%s" e )
close(f)
)
)
;--------------------------Margin_extract-----------------------------------
procedure( marginex_form_jsim( wid_marginex_jsim )
let( ( marginex_jsim_dir marginex_jsim_lib marginex_jsim_cell marginex_jsim_1Symbol marginex1_jsim )
;获取当前编辑的单元信息↓
deCV_marginex_jsim = deGetEditCellView()
libName_marginex_jsim = deCV_marginex_jsim~>libName
cellName_marginex_jsim = deCV_marginex_jsim~>cellName
viewName_marginex_jsim = deCV_marginex_jsim~>viewName
dirwithcellview_marginex_jsim=strcat( "~/Cadence/designs/" cellName_marginex_jsim )

;目录↓
marginex_dir_jsim = hiCreateStringField(
?prompt "Target Directory"
?name 'marginex_dir_jsim
?value dirwithcellview_marginex_jsim
?defValue dirwithcellview_marginex_jsim
)
;库名↓
marginex_lib_jsim = hiCreateStringField(
?prompt "Library Name"
?name 'marginex_lib_jsim
?value libName_marginex_jsim
?defValue libName_marginex_jsim
)
;单元名↓
marginex_cell_jsim = hiCreateStringField(
?prompt "Cellview Name"
?name 'marginex_cell_jsim
?value cellName_marginex_jsim
?defValue cellName_marginex_jsim
)

;param↓
marginex_param_jsim = hiCreateStringField(
?prompt "Parameter"
?name 'marginex_param_jsim
?value "XI,XJ,XL"
?defValue "XI,XJ,XL"
)

;max margin↓
marginex_max_jsim = hiCreateStringField(
?prompt "Max margin"
?name 'marginex_max_jsim
?value "0.5"
?defValue "0.5"
)
;表格主体↓
marginex_jsim_1Symbol = gensym( 'WindowForm ) 
marginex1_jsim = hiCreateAppForm(
?name marginex_jsim_1Symbol
?formTitle "margin extract"
?callback  "mycallbackfunc_marginex_jsim( hiGetCurrentForm() )"
?dontBlock t
?fields list( marginex_dir_jsim marginex_lib_jsim marginex_cell_jsim marginex_param_jsim marginex_max_jsim )
?unmapAfterCB t )
marginex1_jsim->wid_marginex_jsim = wid_marginex_jsim ;;; associate the wid with the form, via a user-
;;; defined slot
marginex1_jsim ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_marginex_jsim( marginex1_jsim )
let( ( wid_marginex_jsim getdir_marginex_jsim getlib_marginex_jsim getcell_marginex_jsim )
;;; pick up current form values
wid_marginex_jsim = marginex1_jsim->wid_marginex_jsim ;;; user specified slot linking the form
;;; to the window
getdir_marginex_jsim = marginex1_jsim->marginex_dir_jsim->value
getlib_marginex_jsim = marginex1_jsim->marginex_lib_jsim->value
getcell_marginex_jsim = marginex1_jsim->marginex_cell_jsim->value
getparam_marginex_jsim = marginex1_jsim->marginex_param_jsim->value
getmax_marginex_jsim = marginex1_jsim->marginex_max_jsim->value
;print(getdir_marginex_jsim)
Generate_JSIC_marginex( getdir_marginex_jsim getparam_marginex_jsim getmax_marginex_jsim )
pscan_netlist_jsim( getdir_marginex_jsim getlib_marginex_jsim getcell_marginex_jsim )
system("chmod +x ./JSICsim_marginex.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_marginex.sh';exec bash'")
ipcSleep(1)
ipcBeginProcess("rm JSICsim_marginex.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( marginex_window_jsim()
let( ( wf_marginex_jsim )
wf_marginex_jsim=marginex_form_jsim(window(1))
hiDisplayForm( wf_marginex_jsim )
)
)
procedure( Generate_JSIC_marginex( dir param max)
let( ( f )
f = outfile("./JSICsim_marginex.sh" "w")
c=strcat( "cd" " " dir)
d="JSICsim margin -m "
e=strcat( d param " -M " max )
fprintf( f "%s\n" c )
fprintf( f "%s" e )
close(f)
)
)

;--------------------------simulate_sweep-----------------------------------
procedure( simulatesw_form_jsim( wid_simulatesw_jsim )
let( ( simulatesw_jsim_dir simulatesw_jsim_lib simulatesw_jsim_cell simulatesw_jsim_1Symbol simulatesw1_jsim )
;获取当前编辑的单元信息↓
deCV_simulatesw_jsim = deGetEditCellView()
libName_simulatesw_jsim = deCV_simulatesw_jsim~>libName
cellName_simulatesw_jsim = deCV_simulatesw_jsim~>cellName
viewName_simulatesw_jsim = deCV_simulatesw_jsim~>viewName
dirwithcellview_simulatesw_jsim=strcat( "~/Cadence/designs/" cellName_simulatesw_jsim )

;目录↓
simulatesw_dir_jsim = hiCreateStringField(
?prompt "Target Directory"
?name 'simulatesw_dir_jsim
?value dirwithcellview_simulatesw_jsim
?defValue dirwithcellview_simulatesw_jsim
)
;库名↓
simulatesw_lib_jsim = hiCreateStringField(
?prompt "Library Name"
?name 'simulatesw_lib_jsim
?value libName_simulatesw_jsim
?defValue libName_simulatesw_jsim
)
;单元名↓
simulatesw_cell_jsim = hiCreateStringField(
?prompt "Cellview Name"
?name 'simulatesw_cell_jsim
?value cellName_simulatesw_jsim
?defValue cellName_simulatesw_jsim
)


;swparam↓
simulatesw_swparam_jsim = hiCreateStringField(
?prompt "Independent Variable"
?name 'simulatesw_swparam_jsim
?value "TQ"
?defValue "TQ"
)

;sweep_max↓
simulatesw_from_jsim = hiCreateStringField(
?prompt "From"
?name 'simulatesw_from_jsim
?value "20"
?defValue "20"
)

;sweep_min↓
simulatesw_to_jsim = hiCreateStringField(
?prompt "To"
?name 'simulatesw_to_jsim
?value "100"
?defValue "100"
)

;sweep_step↓
simulatesw_step_jsim = hiCreateStringField(
?prompt "Step"
?name 'simulatesw_step_jsim
?value "10"
?defValue "10"
)
;表格主体↓
simulatesw_jsim_1Symbol = gensym( 'WindowForm ) 
simulatesw1_jsim = hiCreateAppForm(
?name simulatesw_jsim_1Symbol
?formTitle "simulate sweep"
?callback  "mycallbackfunc_simulatesw_jsim( hiGetCurrentForm() )"
?dontBlock t
?fields list( simulatesw_dir_jsim simulatesw_lib_jsim simulatesw_cell_jsim simulatesw_swparam_jsim simulatesw_from_jsim simulatesw_to_jsim simulatesw_step_jsim)
?unmapAfterCB t )
simulatesw1_jsim->wid_simulatesw_jsim = wid_simulatesw_jsim ;;; associate the wid with the form, via a user-
;;; defined slot
simulatesw1_jsim ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_simulatesw_jsim( simulatesw1_jsim )
let( ( wid_simulatesw_jsim getdir_simulatesw_jsim getlib_simulatesw_jsim getcell_simulatesw_jsim )
;;; pick up current form values
wid_simulatesw_jsim = simulatesw1_jsim->wid_simulatesw_jsim ;;; user specified slot linking the form
;;; to the window
getdir_simulatesw_jsim = simulatesw1_jsim->simulatesw_dir_jsim->value
getlib_simulatesw_jsim = simulatesw1_jsim->simulatesw_lib_jsim->value
getcell_simulatesw_jsim = simulatesw1_jsim->simulatesw_cell_jsim->value
getswparam_simulatesw_jsim = simulatesw1_jsim->simulatesw_swparam_jsim->value
getfrom_simulatesw_jsim = simulatesw1_jsim->simulatesw_from_jsim->value
getto_simulatesw_jsim = simulatesw1_jsim->simulatesw_to_jsim->value
getstep_simulatesw_jsim = simulatesw1_jsim->simulatesw_step_jsim->value
;print(getdir_simulatesw_jsim getfrom_simulatesw_jsim)
Generate_JSIC_simulatesw( getdir_simulatesw_jsim getswparam_simulatesw_jsim getfrom_simulatesw_jsim getto_simulatesw_jsim getstep_simulatesw_jsim)
pscan_netlist_jsim( getdir_simulatesw_jsim getlib_simulatesw_jsim getcell_simulatesw_jsim )
system("chmod +x ./JSICsim_simulatesw.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_simulatesw.sh';exec bash'")
ipcSleep(1)
ipcBeginProcess("rm JSICsim_simulatesw.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( simulatesw_window_jsim()
let( ( wf_simulatesw_jsim )
wf_simulatesw_jsim=simulatesw_form_jsim(window(1))
hiDisplayForm( wf_simulatesw_jsim )
)
)
procedure( Generate_JSIC_simulatesw( dir swparam from to step)
let( ( f )
f = outfile("./JSICsim_simulatesw.sh" "w")
c=strcat( "cd" " " dir)
d="JSICsim sim"
e=strcat( d " -p " swparam "=" from ":" to ":" step )
fprintf( f "%s\n" c )
fprintf( f "%s" e )
close(f)
)
)
;--------------------------Simulate-----------------------------------
procedure( simulate_form_jsim( wid_simulate_jsim )
let( ( simulate_jsim_dir simulate_jsim_lib simulate_jsim_cell simulate_jsim_1Symbol simulate1_jsim )
;获取当前编辑的单元信息↓
deCV_simulate_jsim = deGetEditCellView()
libName_simulate_jsim = deCV_simulate_jsim~>libName
cellName_simulate_jsim = deCV_simulate_jsim~>cellName
viewName_simulate_jsim = deCV_simulate_jsim~>viewName
dirwithcellview_simulate_jsim=strcat( "~/Cadence/designs/" cellName_simulate_jsim )

;目录↓
simulate_dir_jsim = hiCreateStringField(
?prompt "Target Directory"
?name 'simulate_dir_jsim
?value dirwithcellview_simulate_jsim
?defValue dirwithcellview_simulate_jsim
)
;库名↓
simulate_lib_jsim = hiCreateStringField(
?prompt "Library Name"
?name 'simulate_lib_jsim
?value libName_simulate_jsim
?defValue libName_simulate_jsim
)
;单元名↓
simulate_cell_jsim = hiCreateStringField(
?prompt "Cellview Name"
?name 'simulate_cell_jsim
?value cellName_simulate_jsim
?defValue cellName_simulate_jsim
)

;表格主体↓
simulate_jsim_1Symbol = gensym( 'WindowForm ) 
simulate1_jsim = hiCreateAppForm(
?name simulate_jsim_1Symbol
?formTitle "margin extract"
?callback  "mycallbackfunc_simulate_jsim( hiGetCurrentForm() )"
?dontBlock t
?fields list( simulate_dir_jsim simulate_lib_jsim simulate_cell_jsim )
?unmapAfterCB t )
simulate1_jsim->wid_simulate_jsim = wid_simulate_jsim ;;; associate the wid with the form, via a user-
;;; defined slot
simulate1_jsim ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_simulate_jsim( simulate1_jsim )
let( ( wid_simulate_jsim getdir_simulate_jsim getlib_simulate_jsim getcell_simulate_jsim )
;;; pick up current form values
wid_simulate_jsim = simulate1_jsim->wid_simulate_jsim ;;; user specified slot linking the form
;;; to the window
getdir_simulate_jsim = simulate1_jsim->simulate_dir_jsim->value
getlib_simulate_jsim = simulate1_jsim->simulate_lib_jsim->value
getcell_simulate_jsim = simulate1_jsim->simulate_cell_jsim->value
;print(getdir_simulate_jsim)
Generate_JSIC_simulate( getdir_simulate_jsim)
pscan_netlist_jsim( getdir_simulate_jsim getlib_simulate_jsim getcell_simulate_jsim )
system("chmod +x ./JSICsim_simulate.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_simulate.sh';exec bash'")
ipcSleep(1)
ipcBeginProcess("rm JSICsim_simulate.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( simulate_window_jsim()
let( ( wf_simulate_jsim )
wf_simulate_jsim=simulate_form_jsim(window(1))
hiDisplayForm( wf_simulate_jsim )
)
)
procedure( Generate_JSIC_simulate( dir )
let( ( f )
f = outfile("./JSICsim_simulate.sh" "w")
c=strcat( "cd" " " dir)
d="JSICsim sim"
fprintf( f "%s\n" c )
fprintf( f "%s" d )
close(f)
)
)
;--------------------------psui主菜单-----------------------------------
procedure( psui_form_jsim( wid_psui_jsim )
let( ( psui_jsim_dir psui_jsim_lib psui_jsim_cell psui_jsim_1Symbol psui1_jsim )
;获取当前编辑的单元信息↓
deCV_psui_jsim = deGetEditCellView()
libName_psui_jsim = deCV_psui_jsim~>libName
cellName_psui_jsim = deCV_psui_jsim~>cellName
viewName_psui_jsim = deCV_psui_jsim~>viewName
dirwithcellview_psui_jsim=strcat( "~/Cadence/designs/" cellName_psui_jsim )

;目录↓
psui_dir_jsim = hiCreateStringField(
?prompt "Target Directory"
?name 'psui_dir_jsim
?value dirwithcellview_psui_jsim
?defValue dirwithcellview_psui_jsim
)
;库名↓
psui_lib_jsim = hiCreateStringField(
?prompt "Library Name"
?name 'psui_lib_jsim
?value libName_psui_jsim
?defValue libName_psui_jsim
)
;单元名↓
psui_cell_jsim = hiCreateStringField(
?prompt "Cellview Name"
?name 'psui_cell_jsim
?value cellName_psui_jsim
?defValue cellName_psui_jsim
)
;表格主体↓
psui_jsim_1Symbol = gensym( 'WindowForm ) 
psui1_jsim = hiCreateAppForm(
?name psui_jsim_1Symbol
?formTitle "Psui Initialize"
?callback  "mycallbackfunc_psui_jsim( hiGetCurrentForm() )"
?dontBlock t
?fields list( psui_dir_jsim psui_lib_jsim psui_cell_jsim )
?unmapAfterCB t )
psui1_jsim->wid_psui_jsim = wid_psui_jsim ;;; associate the wid with the form, via a user-
;;; defined slot
psui1_jsim ;;; my return value
) ; let
) ; procedure
;点击后激活函数
procedure( mycallbackfunc_psui_jsim( psui1_jsim )
let( ( wid_psui_jsim getdir_psui_jsim getlib_psui_jsim getcell_psui_jsim )
;;; pick up current form values
wid_psui_jsim = psui1_jsim->wid_psui_jsim ;;; user specified slot linking the form
;;; to the window
getdir_psui_jsim = psui1_jsim->psui_dir_jsim->value
getlib_psui_jsim = psui1_jsim->psui_lib_jsim->value
getcell_psui_jsim = psui1_jsim->psui_cell_jsim->value
print(getdir_psui_jsim)
Generate_JSIC_psui( getdir_psui_jsim )
pscan_netlist_jsim( getdir_psui_jsim getlib_psui_jsim getcell_psui_jsim )
system("chmod +x ./JSICsim_psui.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_psui.sh';exec bash'")
ipcSleep(1)
ipcBeginProcess("rm JSICsim_psui.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口函数
procedure( psui_window_jsim()
let( ( wf_psui_jsim )
wf_psui_jsim=psui_form_jsim(window(1))
hiDisplayForm( wf_psui_jsim )
)
)
procedure( Generate_JSIC_psui( str )
let( ( f )
f = outfile("./JSICsim_psui.sh" "w")
c=strcat( "cd" " " str)
d="JSICsim wave"
fprintf( f "%s\n" c )
fprintf( f "%s" d )
close(f)
)
)

;--------------------------------------------------------------------------
;----------------------网表定向生成function---------------------------
procedure( pscan_netlist_jsim( path lib cell )
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
;---------------------打开手册选项----------------------
procedure( open_JSIMhelp()
let( (  )
Generate_JSIC_help()
system("chmod +x ./JSICsim_help.sh")
system("gnome-terminal -x bash -c 'export RUN_AFTER_BASHRC='./JSICsim_help.sh';exec bash'")
;ipcWait(run_JSIM_help)
ipcSleep(1)
ipcBeginProcess("rm JSICsim_help.sh")
)
)
procedure( Generate_JSIC_help( )
let( ( f )
f = outfile("./JSICsim_help.sh" "w")
JSIM_script_help="JSICsim -h"
fprintf( f "%s\n" JSIM_script_help )
close(f)
)
)

;菜单栏设置

margin_extract=hiCreateMenuItem(
?name 'margin_extract
?itemText "Extract"
?callback "marginex_window_jsim"
)
margin_sweep=hiCreateMenuItem(
?name 'margin_sweep
?itemText "Sweep"
?callback "marginsw_window_jsim"
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'JSIM_menu_margin
""
list(
margin_extract
margin_sweep
)
)
;设置带slider的菜单选项-前仿
JSIM_slider_Margins = hiCreateSliderMenuItem( 
?name 'JSIM_slider_Margins
?itemText "Margins"
?subMenu JSIM_menu_margin
)
;设置分割线
separator_JSIM=hiCreateSeparatorMenuItem(
?name 'spl_JSIM
)
;后仿菜单选项卡
simulate_run=hiCreateMenuItem( ;菜单栏4
?name 'simulate_run
?itemText "Run"
?callback "simulate_window_jsim" ;预留
)
simulate_sweep=hiCreateMenuItem( ;菜单栏5
?name 'simulate_sweep
?itemText "Sweep"
?callback "simulatesw_window_jsim" ;
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'JSIM_menu_sim
""
list(
simulate_run
simulate_sweep
)
)
;设置带slider的菜单选项
JSIM_slider_Simulate = hiCreateSliderMenuItem( 
?name 'JSIM_slider_Simulate
?itemText "Simulate"
?subMenu JSIM_menu_sim
)

JSIM_help= hiCreateMenuItem(
?name 'JSIM_help
?itemText "JSIM-help"
?callback "open_JSIMhelp"
)
;-------psui menu----------
JSIM_psui=hiCreateMenuItem(
?name 'JSIM_psui
?itemText "Psui"
?callback "psui_window_jsim"
)
hiCreatePulldownMenu(
'Pulldown_JSIM
"JSIMsim"
list(  JSIM_slider_Simulate JSIM_slider_Margins JSIM_psui separator_JSIM JSIM_help )
)
;添加至layout窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'Pulldown_JSIM (hiGetNumMenus (hiGetCIWindow)));
procedure(add_layout_menu_JSIM(args)
hiInsertBannerMenu((getCurrentWindow) 'Pulldown_JSIM (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("maskLayout"  nil nil 'add_layout_menu_JSIM)
;------------------------------------------------------------------------------

;添加至schematic窗口
;------------------------------------------------------------------------------
hiInsertBannerMenu((hiGetCIWindow) 'Pulldown_JSIM (hiGetNumMenus (hiGetCIWindow)));
procedure(add_schematic_menu_JSIM(args)
hiInsertBannerMenu((getCurrentWindow) 'Pulldown_JSIM (hiGetNumMenus (getCurrentWindow)));
)
deRegUserTriggers("schematic"  nil nil 'add_schematic_menu_JSIM)
;------------------------------------------------------------------------------
