// Library - yrt03_FA, Cell - fa_a, View - schematic_p
// LAST TIME SAVED: Jun 27 16:28:11 2019
// NETLIST TIME: Jun 27 16:38:15 2019
`timescale 1ps / 1ps 

module fa_a ( CO, SO, AI, BI, CI, TI );

output  CO, SO;
output [15:0] AO, BO;

input  AI, BI, CI, TI;


specify 
    specparam CDS_LIBNAME  = "yrt03_FA";
    specparam CDS_CELLNAME = "fa_a";
    specparam CDS_VIEWNAME = "schematic_p";
endspecify

jtl2j_a  I114 ( .AO(net066), .AI(net067));
jtl2j_a  I111 ( .AO(net065), .AI(net063));
jtl2j_a  I106 ( .AO(net063), .AI(net064));
jtl2j_a  I105 ( .AO(net064), .AI(net078));
jtl2j_a  I110 ( .AO(net079), .AI(net080));
jtl2j_a  I102 ( .AO(net077), .AI(net075));
jtl2j_a  I59 ( .AO(net08), .AI(net090));
jtl2j_a  I67 ( .AO(net0107), .AI(net6));
jtl2j_a  I52 ( .AO(net0109), .AI(AI));
jtl2j_a  I49 ( .AO(net020), .AI(net0109));
jtl2j_a  I50 ( .AO(net021), .AI(net020));
jtl2j_a  I51 ( .AO(net9), .AI(net021));
jtl2j_a  I39 ( .AO(net05), .AI(CI));
jtl2j_a  I38 ( .AO(net04), .AI(net05));
jtl2j_a  I44 ( .AO(net023), .AI(BI));
jtl2j_a  I45 ( .AO(net02), .AI(net023));
jtl2j_a  I35 ( .AO(net01), .AI(net04));
jtl2j_a  jtl2j01 ( .AO(net3), .AI(net5));
jtl2j_a  I32 ( .AO(net014), .AI(net015));
jtl2j_a  jtl2j04 ( .AO(net029), .AI(net07));
jtl2j_a  jtl2j03 ( .AO(net029), .AI(net033));
jtl2j_a  I31 ( .AO(net050), .AI(net014));
jtl2j_a  I33 ( .AO(net015), .AI(net016));
jtl2j_a  jtl2j00 ( .AO(net2), .AI(net1));
s2j2o_b  I85 ( .AOA(net085), .AOB(net0106),
     .AI(net090));
s2j2o_b  spl2j00 ( .AOA(net010), .AOB(net06),
     .AI(net018));
s2j2o_b  spl2j01 ( .AOA(net038), .AOB(net049),
     .AI(net017));
s2j2o_b  spl2j02 ( .AOA(net033), .AOB(net024),
     .AI(net026));
s2j3o_a  spl3j00 ( .AOC(net5), .AOB(net6),
       .AOA(net1), .AI(net7));
jtl2j_a  I88 ( .AO(net093), .AI(net0103));
jtl2j_a  jtl2j02 ( .AO(net06), .AI(net09));
xor_b  xorb0 ( .TI(net3), .AI(net07), .TO(net08),
     .BI(net09));
and_e  ande1 ( .BI(net086), .ABO(net077),
     .TI(net084),  .AI(net083));
and_e  ande0 ( .BI(net010), .ABO(net011),
     .TI(net012), .AI(net013));
jandf_a  jandfa0 ( .BI(net010), .ABO(net011),
     .TI(net012), .AI(net013));
jtl1j_a  I118 ( .AI(net071), .AO(net062));
jtl1j_a  I117 ( .AI(net069), .AO(net061));
jtl1j_a  jtl1j01 ( .AI(net035), .AO(net034));
jtl_crs22  jtlcs_2j_00 ( .BO(net049), .AO(net019),
     .BI(net012), .AI(net013));
d22_a  d22a0 ( .TO(net8), .TI(net2), .AI(net9));
jtl_crs22  I76 ( .BO(net070), .AO(net0105),
     .BI(net088), .AI(net087));
jtl_crs22  I66 ( .BO(net089), .AO(net095),
     .BI(net096), .AI(net0105));
jtl_crs22  I57 ( .BO(net096), .AO(net0107),
     .BI(net0106), .AI(net092));
jtl_crs22  jtlcs_2j_01 ( .BO(net027), .AO(net025),
     .BI(net024), .AI(net018));
jtl_crs22  jtlcs_2j_02 ( .BO(net030), .AO(net025),
     .BI(net035), .AI(net01));
jtl_crs22  jtlcs_2j_03 ( .BO(net047), .AO(net026),
     .BI(net030), .AI(net02));
jtl4j_a  jtl4j00 ( .AO(net027), .AI(net019));
jtl2j_a  I91 ( .AO(net082), .AI(net081));
jtl2j_a  I90 ( .AO(net081), .AI(net083));
jtl2j_a  jtl2j05 ( .AO(net017), .AI(net031));
jtl2j_a  I34 ( .AO(net7), .AI(net016));
jtl2j_a  I116 ( .AO(net070), .AI(net071));
jtl2j_a  I115 ( .AO(net068), .AI(net069));
jtl2j_a  I101 ( .AO(net072), .AI(net076));
jtl2j_a  I92 ( .AO(net082), .AI(net087));
jtl2j_a  I89 ( .AO(net0103), .AI(net084));
jtl2j_a  I87 ( .AO(net086), .AI(net085));
jtl2j_a  I77 ( .AO(net0104), .AI(net078));
jtl2j_a  I79 ( .AO(net080), .AI(net089));
jtl2j_a  jtl2j06 ( .AO(net034), .AI(net031));
s2j2o_b  I53 ( .AOA(net099), .AOB(net0104), .AI(net8));
s2j2o_b  I28 ( .AOA(net047), .AOB(net050), .AI(TI));
d22_a  d22a1 ( .TO(net072), .TI(net073), .AI(net011));
jtl1j_a  I96 ( .AI(net074), .AO(net073));
jtl1j_a  I68 ( .AI(net099), .AO(net095));
s2j2o_b  I82 ( .AOA(net093), .AOB(net088),
     .AI(net092));
jtl4j_a  I95 ( .AO(net074), .AI(net038));
cb_a  I98 ( .ABO(CO), .BI(net075), .AI(net076));
xor_b  xorb1 ( .TI(net068), .AI(net079), .TO(SO),
     .BI(net067));
jtl2j_a  I119 ( .AO(net061), .AI(net062));
jtl2j_a  I113 ( .AO(net066), .AI(net065));

endmodule

// Library - yrt03_FA, Cell - fa_a, View - schematic_p
// LAST TIME SAVED: Jun 27 16:28:11 2019
// NETLIST TIME: Jun 27 16:38:15 2019
`timescale 1ps / 1ps 

module fb_b( CO, SO, AI, BI, CI, TI );

output  CO, SO;
input  CO, SO;

and_e  ande0 ( .BI(net010), .ABO(net011),
     .TI(net012), .AI(net013));
jandf_a  jandfa0 ( .BI(net010), .ABO(net011),
     .TI(net012), .AI(net013));
jtl_crs22  jtlcs_2j_00 ( .BO(net049), .AO(net019),
     .BI(net012), .AI(net013));
d22_a  d22a0 ( .TO(net8), .TI(net2), .AI(net9));
jtl_crs22  I76 ( .BO(net070), .AO(net0105),
     .BI(net088), .AI(net087));

endmodule
