cellID=dbOpenCellViewByType("ysc_layout2" "auto_route" "layout" "maskLayout")

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(0:137.0 8.5:145.5 11.5:145.5 11.5:124.5 8.5:124.5 0:133.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(12.0:135.0 30:135.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePath(?layer "mp1" ?pts list(15.0:120 210:105.0) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(270:107.0 261.5:115.5 258.5:115.5 258.5:94.5 261.5:94.5 270:103.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(258.0:105.0 240:105.0) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(-133.0:-90 -124.5:-98.5 -124.5:-101.5 -145.5:-101.5 -145.5:-98.5 -137.0:-90))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(-135.0:-102.0 -135.0:-120) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(-146.0:-90 -146.0:-99.11269837361638 -99.11269837361638:-146.0 -90.0:-146.0 -90.0:-124.0 -124.0:-90))

rodCreatePath(?layer "mp1" ?pts list(-90:-135.0 180:-135.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(180:-146.0 189.11269837361638:-146.0 236.0:-99.11269837361638 236.0:-90.0 214.0:-90.0 180:-124.0))

rodCreatePath(?layer "mp1" ?pts list(225.0:-90 225.0:60) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(214.0:64.0 214.0:86.0 236.0:86.0 236.0:64.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -1)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 1)
rodCreatePath(?layer "mp1" ?pts list(225.0:60.0 225.0:63.0) ?width 22 ?justification "center" ?cvId  cellID)
rodCreatePath(?layer "mn0" ?pts list(225.0:87.0 225.0:90.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePath(?layer "mn0" ?pts list(225.0:90 225.0:90) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(214.0:120 214.0:129.11269837361638 200.88730162638362:116.0 210.0:116.0 210.0:94.0 236.0:120))

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(270:137.0 261.0:146.0 258.0:146.0 258.0:124.0 261.0:124.0 270:133.0))
rodCreatePath(?layer "mn0" ?pts list(258.0:135.0 240:135.0) ?width 22 ?justification "center" ?cvId  cellID)
