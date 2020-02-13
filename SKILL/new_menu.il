;2020/2/12 杨树澄
;Virtuoso外挂系列
;--------------------------------------------------------------------------
procedure( margin_form( wid );创建Margin仿真对话框
let( ( margin_dir margin_lib margin_cell margin1Symbol margin1 )
margin_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'margin_dir
?value "/home/SIMIT/yangshucheng/Cadence/lib/lib_Nb03/";预留
?defValue "directory";预留
)

margin_lib = hiCreateStringField(
?prompt "Library Name"
?name 'margin_lib
?value "ysc_test"
?defValue "lib"
)

margin_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'margin_cell
?value "cell"
?defValue "cell"
)
;创建窗口symbol
margin1Symbol = gensym( 'WindowForm )
;创建窗口主体
margin1 = hiCreateAppForm(
?name margin1Symbol
?formTitle "Calculate Margins"
?callback  "mycallbackfunc( hiGetCurrentForm() )"
?dontBlock t
?fields list( margin_dir margin_lib margin_cell )
?unmapAfterCB t )
margin1->wid = wid ;;; associate the wid with the form, via a user-
;;; defined slot
margin1 ;;; my return value
) ; let
) ; procedure

;返回功能函数，点击ok后自动开始计算margin
procedure( mycallbackfunc( margin1 )
let( ( wid getdir getlib getcell )
;;; pick up current form values
wid = margin1->wid ;;; user specified slot linking the form
;;; to the window
getdir = margin1->margin_dir->value
getlib = margin1->margin_lib->value
getcell = margin1->margin_cell->value
;;; set the window name
println( getdir )
println( getlib )
println( getcell )
CalculateMargins(getdir)
pscan_netlist( getdir getlib getcell )
system("bash run.sh")
t ;;; my return value
) ; let
) ; procedure
;打开窗口子函数
procedure( margin_window()
let( ( wf )
wf=margin_form(window(1))
hiDisplayForm( wf )
);let
);procedure

;计算margin脚本子函数
procedure( CalculateMargins( str )
let( ( f )
f = outfile("./run.sh" "w")
c=strcat( "cd" " " str)
d="python margins.py main"
fprintf( f "%s\n" c )
fprintf( f "%s" d )
close(f)
);let
);procedure

;netlist生成子函数
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

);let
);procedure
;-------------------------------以下为菜单栏设置------------------------
;菜单栏设置
menuItem_1=hiCreateMenuItem( ;菜单栏1
?name 'menu_1
?itemText "Margins"
?callback "margin_window" ;调用表格函数
)
menuItem_2=hiCreateMenuItem( ;菜单栏2
?name 'menu_2
?itemText "psui"
?callback "function_2" ;预留
)
menuItem_3=hiCreateMenuItem( ;菜单栏3
?name 'menu_3
?itemText "Timing"
?callback "function_3" ;预留
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'trSubMenuA
""
list(
menuItem_1
menuItem_2
menuItem_3
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