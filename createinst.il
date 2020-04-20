cellID=dbOpenCellViewByType("ysc_layout" "auto_route" "layout" "maskLayout")

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(0:227.0 8.5:235.5 11.5:235.5 11.5:214.5 8.5:214.5 0:223.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(12.0:225.0 30:225.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePath(?layer "mp1" ?pts list(30:225.0 180:225.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(180:236.0 189.11269837361638:236.0 236.0:189.11269837361638 236.0:180.0 214.0:180.0 180:214.0))

rodCreatePath(?layer "mp1" ?pts list(225.0:180 225.0:120) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(214.0:120 214.0:110.88730162638362 260.88730162638365:64.0 270.0:64.0 270.0:86.0 236.0:120))

rodCreatePath(?layer "mp1" ?pts list(270:75.0 870:75.0) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(900:77.0 891.5:85.5 888.5:85.5 888.5:64.5 891.5:64.5 900:73.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(888.0:75.0 870:75.0) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(0:-43.0 8.5:-34.5 11.5:-34.5 11.5:-55.5 8.5:-55.5 0:-47.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(12.0:-45.0 30:-45.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePath(?layer "mp1" ?pts list(30:-45.0 630:-45.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(630:-56.0 639.1126983736164:-56.0 686.0:-9.112698373616377 686.0:0.0 664.0:0.0 630:-34.0))

rodCreatePath(?layer "mp1" ?pts list(675.0:0 675.0:30) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(664.0:34.0 664.0:56.0 686.0:56.0 686.0:34.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -1)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 1)
rodCreatePath(?layer "mp1" ?pts list(675.0:30.0 675.0:33.0) ?width 22 ?justification "center" ?cvId  cellID)
rodCreatePath(?layer "mn0" ?pts list(675.0:56.0 675.0:60.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePath(?layer "mn0" ?pts list(675.0:60 675.0:90) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(664.0:94.0 664.0:116.0 686.0:116.0 686.0:94.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -1)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 1)
rodCreatePath(?layer "mp1" ?pts list(675.0:117.0 675.0:120.0) ?width 22 ?justification "center" ?cvId  cellID)
rodCreatePath(?layer "mn0" ?pts list(675.0:90.0 675.0:94.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(664.0:120 664.0:129.11269837361638 710.8873016263836:176.0 720.0:176.0 720.0:154.0 686.0:120))

rodCreatePath(?layer "mp1" ?pts list(720:165.0 750:165.0) ?width 22 ?justification "center" ?cvId  cellID)

rodCreatePolygon(?cvId cellID ?layer "mp1" ?pts list(750:176.0 769.5563491868081:176.0 829.5563491868082:116.0 840.0:116.0 840.0:94.0 820.4436508131919:94.0 760.4436508131918:154.0 750:154.0))

rodCreatePath(?layer "mp1" ?pts list(840:105.0 870:105.0) ?width 22 ?justification "center" ?cvId  cellID)

ref=rodCreatePolygon(?cvId cellID ?layer "mn0" ?pts list(900:107.0 891.5:115.5 888.5:115.5 888.5:94.5 891.5:94.5 900:103.0))
rodCreatePolygon(?cvId cellID ?layer "in0" ?fromObj ref ?size -0.5)
rodCreatePolygon(?cvId cellID ?layer "mp1" ?fromObj ref ?size 0.5)
rodCreatePath(?layer "mp1" ?pts list(888.0:105.0 870:105.0) ?width 22 ?justification "center" ?cvId  cellID)
