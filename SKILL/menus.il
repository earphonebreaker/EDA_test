;表格代码区
procedure(myformfunc()
mystring1=hiCreateStringField(?name `stringfield1 ?prompt "String1")
mystring2=hiCreateStringField(?name `stringfield2 ?prompt "String2")
myfloat1=hiCreateFloatField(?name `floatfield1 ?prompt "Float1"	?defValue 6.0)
mycyclic1=hiCreateCyclicField(?name   `cyclicfield1 ?prompt "Cyclic1"  ?choices list("choice1" "choice2")    ?defValue "choice2")
myradio1=hiCreateRadioField(?name `radiofield1 ?choices `("yes" "no") ?prompt "Radio1" ?defValue "no" ?callback nil)
myspinbox1=hiCreateSpinBox(?name `spinbox1 ?prompt "SpinBox1" ?range list(-15 10) ?defValue `5 ?arrowOrientation `horizontal)
myseparatorfield1=hiCreateSeparatorField(?name `separatorfield )
myformbutton1=hiCreateFormButton(?name `formbutton1 ?buttonText "FormButton1")
mylabel1=hiCreateLabel(?name `label1 ?labelText "LabelText1")
mypointfield1=hiCreatePointField(?name `pointfield1 ?value list(1.2 1.3))
mypointlistfield1=hiCreatePointListField(?name `pointlistfield1 ?value list(`(1.2 1.3) `(2.3 3.5)))
myscalefield1=hiCreateScaleField(?name `scalefield1 ?prompt "ScaleField1" ?range `(-100 100))
Tech=techGetTechFile(geGetEditRep())
alllayer=leGetValidLayerList(Tech)
mylayercyclic1=hiCreateLayerCyclicField(Tech "select your layer:" "parseString(car(last(formname7->mylayercyclic->value)) \" ()\")"  alllayer nil `layercyclic1)
mylistfield1=hiCreateListField(?name `listfield1 ?value `abc ?prompt  "ListField" )
mylistboxfield1=hiCreateListBoxField(?name `listboxfield1 ?value list("line2") ?prompt "ListBoxField1" ?choices list("line1" "line2" "lin3"))
mymultitext1=hiCreateMLTextField(?name `multilinetext1 ?prompt "MultiLineText1" ?value "abc\ndef\nend!\n")
myform1=hiCreateAppForm(
?name `formname7
?formTitle "My Form"
;?callback `mycallbackfunc(mycallbackfunc())
?callback nil
?fields list(
mystring1
mystring2
myfloat1
mycyclic1
myradio1
myspinbox1
myseparatorfield1
myformbutton1
mylabel1
mypointfield1
mypointlistfield1
myscalefield1
mylayercyclic1
mylistfield1
mylistboxfield1
mymultitext1
);end-list
);end-create form

hiDisplayForm(`formname7)

procedure(mycallbackfunc(myform)
printnumber=myform->floatfield1->value
printf("your number is %L !" printnumber)
);end-procedure-mycallbackfunc
);end-procedure-myformfunc

;菜单栏设置
menuItem_1=hiCreateMenuItem( ;菜单栏1
?name 'menu_1
?itemText "Margins"
?callback "myformfunc" ;调用表格函数
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

