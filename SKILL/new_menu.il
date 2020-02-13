;表格代码区
procedure( myformfunc( wid )
let( ( margin_dir margin_lib margin_cell myform1Symbol myform1 )
margin_dir = hiCreateStringField(
?prompt "Target Directory"
?name 'margin_dir
?value "directory"
?defValue "directory"
)

margin_lib = hiCreateStringField(
?prompt "Library Name"
?name 'margin_lib
?value "lib"
?defValue "lib"
)

margin_cell = hiCreateStringField(
?prompt "Cellview Name"
?name 'margin_cell
?value "cell"
?defValue "cell"
)

myform1Symbol = gensym( 'WindowForm ) ;;; advanced version
;;; otherwise use 'WindowForm

myform1 = hiCreateAppForm(
?name myform1Symbol
?formTitle "Calculate Margins"
?callback  "mycallbackfunc( hiGetCurrentForm() )"
?dontBlock t
?fields list( margin_dir margin_lib margin_cell )
?unmapAfterCB t )
myform1->wid = wid ;;; associate the wid with the form, via a user-
;;; defined slot
myform1 ;;; my return value
) ; let
) ; procedure

procedure( mycallbackfunc( myform1 )
let( ( wid getdir getlib getcell )
;;; pick up current form values
wid = myform1->wid ;;; user specified slot linking the form
;;; to the window
getdir = myform1->margin_dir->value
getlib = myform1->margin_lib->value
getcell = myform1->margin_cell->value
;;; set the window name
println( getdir )
println( getlib )
println( getcell )
outputstr(getlib)
pscan_netlist( getdir getlib getcell )
t ;;; my return value
) ; let
) ; procedure

procedure( myform()
let( ( wf )
wf=myformfunc(window(1))
hiDisplayForm( wf )
)
)

procedure( outputstr( str )
let( ( f )
f = outfile("./test.txt" "w")
println( str f )
close(f)
)
)

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

;菜单栏设置
menuItem_1=hiCreateMenuItem( ;菜单栏1
?name 'menu_1
?itemText "Margins"
?callback "myform" ;调用表格函数
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
