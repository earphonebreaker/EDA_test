;2020/3/5 杨树澄
;JSIM菜单

;---------------------open help----------------------
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

menuItem_1=hiCreateMenuItem(
?name 'menu_1
?itemText "Reserved_1"
?callback "function_1"
)
menuItem_2=hiCreateMenuItem(
?name 'menu_2
?itemText "Reserved_2"
?callback "function_2"
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'JSIM_menuA
""
list(
menuItem_1
menuItem_2
)
)
;设置带slider的菜单选项-前仿
JSIM_slider_A = hiCreateSliderMenuItem( 
?name 'JSIM_menu_A
?itemText "Reserved_menu"
?subMenu JSIM_menuA
)
;设置分割线
separator_JSIM=hiCreateSeparatorMenuItem(
?name 'spl_JSIM
)
;后仿菜单选项卡
menuItem_4=hiCreateMenuItem( ;菜单栏4
?name 'menu_4
?itemText "Reserved_3"
?callback "function_4" ;预留
)
menuItem_5=hiCreateMenuItem( ;菜单栏5
?name 'menu_5
?itemText "Reserved_4"
?callback "function_4" ;
)

;设置下拉菜单选项
hiCreatePulldownMenu(
'JSIM_menuA
""
list(
menuItem_4
menuItem_5
)
)
;设置带slider的菜单选项
JSIM_slider_B = hiCreateSliderMenuItem( 
?name 'JSIM_menu_B
?itemText "Reserved_menu2"
?subMenu JSIM_menuA
)

JSIM_slider_C= hiCreateMenuItem(
?name 'JSIM_menu_C
?itemText "JSIM-help"
?callback "open_JSIMhelp"
)

hiCreatePulldownMenu(
'Pulldown_JSIM
"JSIMsim"
list( JSIM_slider_A JSIM_slider_B  separator_JSIM JSIM_slider_C )
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